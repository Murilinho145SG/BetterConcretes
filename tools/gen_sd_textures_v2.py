"""
v2: pixel-art-trained model + nearest-neighbor downscale (no LANCZOS blur).

Why this works like "generating 16x16 natively":
- PublicPrompts/All-In-One-Pixel-Model produces pixel art in 512x512 where
  each "pixel" is rendered as a solid 32x32 block (or similar grid).
- Nearest-neighbor downscale 512->16 (or 256->16) samples one pixel per block,
  preserving the hard-edged pixel art the model already produced.

Memory: 4GB VRAM target (same optimizations as v1).
"""
import argparse
import os
import time
from pathlib import Path

import torch
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


HERE = Path(__file__).parent
BLOCK_DIR = HERE.parent / 'src' / 'main' / 'resources' / 'assets' / 'betterconcretes' / 'textures' / 'block'

COLOR_NAMES_LONG = {
    'light_blue': 'light blue',
    'light_gray': 'light gray',
}

COLORS = [
    'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
    'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'
]

# Prompts use the model's trigger keyword "pixelsprite" and "16bitscene"
PROMPTS = {
    'smooth':   'pixelsprite, 16bitscene, seamless tile texture of smooth {color} concrete surface, flat top-down view, clean pixel art, minecraft style, 16x16 pixels',
    'chiseled': 'pixelsprite, 16bitscene, seamless tile texture of chiseled {color} concrete, decorative carved stone pattern, flat top-down view, clean pixel art, minecraft style, 16x16 pixels',
    'polished': 'pixelsprite, 16bitscene, seamless tile texture of polished {color} concrete, smooth reflective surface, subtle highlights, clean pixel art, minecraft style, 16x16 pixels',
    'brick':    'pixelsprite, 16bitscene, seamless tile texture of {color} concrete bricks, running bond pattern with mortar lines, flat top-down view, clean pixel art, minecraft style, 16x16 pixels',
}

NEGATIVE = (
    'blurry, anti-aliased, soft edges, smooth gradient, 3d render, photorealistic, '
    'character, person, creature, ui, frame, border, text, watermark, signature, '
    'multiple tiles, sheet, grid of tiles'
)


def make_pipeline():
    print('Loading All-In-One-Pixel-Model (fp16)...')
    pipe = StableDiffusionPipeline.from_pretrained(
        'PublicPrompts/All-In-One-Pixel-Model',
        torch_dtype=torch.float16,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to('cuda')
    pipe.enable_attention_slicing()
    pipe.vae.enable_slicing()
    return pipe


def generate_one(pipe, variant, color, seed):
    color_phrase = COLOR_NAMES_LONG.get(color, color)
    prompt = PROMPTS[variant].format(color=color_phrase)
    gen = torch.Generator(device='cuda').manual_seed(seed)
    img = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=20,
        guidance_scale=8.0,
        width=512,
        height=512,
        generator=gen,
    ).images[0]
    return img


def downscale_nearest(img: Image.Image, target=16) -> Image.Image:
    """Crush 512 -> 16 with nearest neighbor. Preserves hard pixel edges."""
    return img.resize((target, target), Image.Resampling.NEAREST).convert('RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variants', default='smooth,chiseled,polished,brick')
    ap.add_argument('--colors', default=','.join(COLORS))
    ap.add_argument('--keep-raw', action='store_true')
    ap.add_argument('--steps', type=int, default=20)
    args = ap.parse_args()

    variants = [v.strip() for v in args.variants.split(',')]
    colors = [c.strip() for c in args.colors.split(',')]

    raw_dir = HERE / 'sd_raw_v2'
    if args.keep_raw:
        raw_dir.mkdir(exist_ok=True)

    pipe = make_pipeline()
    total = len(variants) * len(colors)
    count = 0
    t_start = time.time()
    for variant in variants:
        for color in colors:
            count += 1
            seed = (hash((variant, color)) & 0x7FFFFFFF) + 1
            print(f'[{count}/{total}] {variant}_{color}_concrete... ', end='', flush=True)
            t0 = time.time()
            raw = generate_one(pipe, variant, color, seed=seed)
            if args.keep_raw:
                raw.save(raw_dir / f'{variant}_{color}_512.png')
            small = downscale_nearest(raw, 16)
            out_path = BLOCK_DIR / f'{variant}_{color}_concrete.png'
            small.save(out_path)
            print(f'{time.time() - t0:.1f}s')
            # Clear VRAM between calls to avoid slowdown
            torch.cuda.empty_cache()
    total_time = time.time() - t_start
    print(f'\nDone. {count} textures in {total_time:.0f}s ({total_time/count:.1f}s avg).')


if __name__ == '__main__':
    main()
