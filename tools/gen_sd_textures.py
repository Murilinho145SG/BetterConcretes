"""
Generate 16x16 Minecraft concrete textures using Stable Diffusion + pixel-art pipeline.

Pipeline per texture:
1. SD generates 512x512 from a prompt describing the variant + color.
2. Downscale to 16x16 with LANCZOS (preserves highest-contrast pixels).
3. Quantize to a vanilla-derived palette (6 tones per color).
4. Save to src/main/resources/assets/betterconcretes/textures/block/.

Memory profile (4GB VRAM target):
- fp16 weights
- attention_slicing
- vae_slicing
- 512x512 max (768 would OOM on 1050 Ti)

Usage: python tools/gen_sd_textures.py [--variants smooth,chiseled] [--colors white,red]
"""
import argparse
import os
import sys
import time
from pathlib import Path

import torch
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler


HERE = Path(__file__).parent
BLOCK_DIR = HERE.parent / 'src' / 'main' / 'resources' / 'assets' / 'betterconcretes' / 'textures' / 'block'

COLOR_RGB = {
    'white':      (207, 213, 214),
    'orange':     (224,  97,   0),
    'magenta':    (169,  48, 159),
    'light_blue': ( 36, 137, 199),
    'yellow':     (241, 175,  21),
    'lime':       ( 94, 169,  25),
    'pink':       (213, 101, 143),
    'gray':       ( 54,  57,  61),
    'light_gray': (125, 125, 115),
    'cyan':       ( 21, 119, 136),
    'purple':     (100,  32, 156),
    'blue':       ( 45,  47, 143),
    'brown':      ( 96,  59,  32),
    'green':      ( 73,  91,  36),
    'red':        (142,  33,  33),
    'black':      ( 15,  18,  22),
}

# Prompt templates per variant, emphasizing pixel art + Minecraft style
PROMPTS = {
    'smooth':   '16x16 pixel art minecraft texture, smooth {color} concrete, tileable seamless, flat top-down, no anti-aliasing, sharp pixels, matte surface',
    'chiseled': '16x16 pixel art minecraft texture, chiseled {color} concrete block, decorative carved pattern, tileable seamless, flat top-down, sharp pixels, stone relief',
    'polished': '16x16 pixel art minecraft texture, polished {color} concrete, reflective smooth surface, subtle highlights, tileable seamless, flat top-down, sharp pixels',
    'brick':    '16x16 pixel art minecraft texture, {color} concrete bricks, running bond pattern, visible mortar lines, tileable seamless, flat top-down, sharp pixels',
}

NEGATIVE = (
    'blurry, anti-aliased, soft edges, gradient, 3d render, photorealistic, '
    'low contrast, noise, watermark, signature, text, frame, border, ui element'
)

COLOR_NAMES_LONG = {
    'light_blue': 'light blue',
    'light_gray': 'light gray',
}


def build_palette(color_rgb, n=6):
    """Build a 6-tone palette derived from the base RGB: 3 darker + 2 lighter + base."""
    factors = [0.55, 0.72, 0.88, 1.00, 1.15, 1.32]
    palette = []
    for f in factors:
        palette.append(tuple(min(255, max(0, int(c * f))) for c in color_rgb))
    return palette


def quantize_to_palette(img: Image.Image, palette_rgb) -> Image.Image:
    """Map each pixel to the nearest palette color."""
    out = Image.new('RGBA', img.size)
    src = img.convert('RGBA').load()
    dst = out.load()
    W, H = img.size
    for y in range(H):
        for x in range(W):
            r, g, b, a = src[x, y]
            # Find nearest in palette (euclidean in RGB)
            best_i = 0
            best_d = 1e9
            for i, (pr, pg, pb) in enumerate(palette_rgb):
                d = (r-pr)**2 + (g-pg)**2 + (b-pb)**2
                if d < best_d:
                    best_d = d
                    best_i = i
            pr, pg, pb = palette_rgb[best_i]
            dst[x, y] = (pr, pg, pb, 255)
    return out


def downscale_to_16(img: Image.Image) -> Image.Image:
    """Downscale to 16x16 with LANCZOS then apply slight contrast boost."""
    # First pass: blur slightly to reduce high-freq noise from SD
    small = img.resize((16, 16), Image.Resampling.LANCZOS)
    return small.convert('RGB')


def make_pipeline():
    """Build the SD pipeline with 4GB VRAM optimizations."""
    print('Loading Stable Diffusion 1.5 (fp16)...')
    pipe = StableDiffusionPipeline.from_pretrained(
        'runwayml/stable-diffusion-v1-5',
        torch_dtype=torch.float16,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to('cuda')
    pipe.enable_attention_slicing()
    pipe.enable_vae_slicing()
    return pipe


def generate_one(pipe, variant, color, seed=None):
    color_phrase = COLOR_NAMES_LONG.get(color, color)
    prompt = PROMPTS[variant].format(color=color_phrase)
    gen = torch.Generator(device='cuda')
    if seed is not None:
        gen.manual_seed(seed)
    img = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE,
        num_inference_steps=18,
        guidance_scale=7.5,
        width=512,
        height=512,
        generator=gen,
    ).images[0]
    return img


def process(raw: Image.Image, color: str) -> Image.Image:
    small = downscale_to_16(raw)
    palette = build_palette(COLOR_RGB[color])
    quantized = quantize_to_palette(small, palette)
    return quantized


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variants', default='smooth,chiseled,polished,brick',
                    help='Comma-separated subset of variants.')
    ap.add_argument('--colors', default=','.join(COLOR_RGB.keys()),
                    help='Comma-separated subset of colors.')
    ap.add_argument('--keep-raw', action='store_true',
                    help='Save the 512x512 SD output alongside (for debugging).')
    args = ap.parse_args()

    variants = [v.strip() for v in args.variants.split(',')]
    colors = [c.strip() for c in args.colors.split(',')]

    raw_dir = HERE / 'sd_raw'
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
            print(f'[{count}/{total}] {variant}_{color}_concrete (seed {seed})... ', end='', flush=True)
            t0 = time.time()
            raw = generate_one(pipe, variant, color, seed=seed)
            if args.keep_raw:
                raw.save(raw_dir / f'{variant}_{color}_512.png')
            small = process(raw, color)
            out_path = BLOCK_DIR / f'{variant}_{color}_concrete.png'
            small.save(out_path)
            print(f'{time.time() - t0:.1f}s')
    total_time = time.time() - t_start
    print(f'\nDone. {count} textures in {total_time:.0f}s ({total_time/count:.1f}s avg).')


if __name__ == '__main__':
    main()
