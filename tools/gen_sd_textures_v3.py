"""
v3: SD 1.5 + Minecraft 1.21 LoRA + img2img from vanilla init + seamless tiling.

Key changes from v2:
- Load Minecraft-1.21 LoRA (trained on vanilla 16x16 block textures)
- Use vanilla {color}_concrete.png as init image (scaled 16->512 nearest)
- img2img with moderate denoising preserves color/layout, restyles surface
- Circular padding on Conv2d makes output seamless/tileable
- Downscale 512->16 with LANCZOS (not nearest), preserving SD detail
"""
import argparse
import os
import time
from pathlib import Path

import torch
from PIL import Image


# Patch Conv2d for seamless tiling BEFORE importing diffusers
def patch_conv_for_tiling():
    init = torch.nn.Conv2d.__init__

    def __init__(self, *args, **kwargs):
        kwargs['padding_mode'] = 'circular'
        return init(self, *args, **kwargs)

    torch.nn.Conv2d.__init__ = __init__


patch_conv_for_tiling()

from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler


HERE = Path(__file__).parent
PROJECT = HERE.parent
BLOCK_DIR = PROJECT / 'src' / 'main' / 'resources' / 'assets' / 'betterconcretes' / 'textures' / 'block'
VANILLA_DIR = HERE / 'vanilla'
LORA_PATH = HERE / 'lora' / 'mc121blocks.safetensors'

COLORS = [
    'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
    'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'
]

COLOR_NAMES_LONG = {'light_blue': 'light blue', 'light_gray': 'light gray'}

# Prompt templates — plain descriptive, LoRA provides the 16x16 minecraft bias.
PROMPTS = {
    'smooth':   'smooth {color} concrete block, flat surface, minecraft texture, seamless, 16x16',
    'chiseled': 'chiseled {color} concrete block, decorative engraved pattern, minecraft texture, seamless, 16x16',
    'polished': 'polished {color} concrete block, glossy reflective surface, minecraft texture, seamless, 16x16',
    'brick':    '{color} concrete bricks, brick pattern with mortar, minecraft texture, seamless, 16x16',
}

# Denoising strength per variant — higher = more deviation from vanilla init.
# Smooth needs low (keep vanilla as-is), brick/chiseled need higher (add pattern).
DENOISING = {
    'smooth':   0.45,
    'polished': 0.55,
    'chiseled': 0.75,
    'brick':    0.72,
}

NEGATIVE = (
    'blurry, anti-aliased, gradient, 3d render, photorealistic, character, '
    'creature, person, ui, frame, border, text, watermark, multiple tiles, '
    'sheet, grid, bordered edge'
)


def make_pipeline():
    print('Loading SD 1.5 + Minecraft LoRA (fp16)...')
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        'runwayml/stable-diffusion-v1-5',
        torch_dtype=torch.float16,
        safety_checker=None,
        requires_safety_checker=False,
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to('cuda')
    pipe.enable_attention_slicing()
    pipe.vae.enable_slicing()
    merge_sgm_lora_into_pipeline(pipe, str(LORA_PATH), alpha=0.85)
    return pipe


# --- SGM (LDM) → diffusers block index mapping for SD 1.5 UNet attentions ---
SGM_UNET_ATTN_MAP = {
    'input_blocks_4_1':   'down_blocks.1.attentions.0',
    'input_blocks_5_1':   'down_blocks.1.attentions.1',
    'input_blocks_7_1':   'down_blocks.2.attentions.0',
    'input_blocks_8_1':   'down_blocks.2.attentions.1',
    'middle_block_1':     'mid_block.attentions.0',
    'output_blocks_3_1':  'up_blocks.1.attentions.0',
    'output_blocks_4_1':  'up_blocks.1.attentions.1',
    'output_blocks_5_1':  'up_blocks.1.attentions.2',
    'output_blocks_6_1':  'up_blocks.2.attentions.0',
    'output_blocks_7_1':  'up_blocks.2.attentions.1',
    'output_blocks_8_1':  'up_blocks.2.attentions.2',
    'output_blocks_9_1':  'up_blocks.3.attentions.0',
    'output_blocks_10_1': 'up_blocks.3.attentions.1',
    'output_blocks_11_1': 'up_blocks.3.attentions.2',
}


def _translate_attn_suffix(suffix: str) -> str:
    """Translate SGM's underscore-joined suffix within an attention block to diffusers dotted path.

    Known patterns to translate (all underscore→dot EXCEPT the named atoms):
      proj_in, proj_out                              → proj_in, proj_out
      transformer_blocks_0_attn1_to_q                → transformer_blocks.0.attn1.to_q
      transformer_blocks_0_attn1_to_out_0            → transformer_blocks.0.attn1.to_out.0
      transformer_blocks_0_ff_net_0_proj             → transformer_blocks.0.ff.net.0.proj
      transformer_blocks_0_ff_net_2                  → transformer_blocks.0.ff.net.2
    """
    if suffix in ('proj_in', 'proj_out'):
        return suffix
    s = suffix
    s = s.replace('transformer_blocks_', 'transformer_blocks.')
    s = s.replace('_attn1_', '.attn1.')
    s = s.replace('_attn2_', '.attn2.')
    s = s.replace('_ff_net_', '.ff.net.')
    # to_q / to_k / to_v are atomic; to_out_0 → to_out.0
    s = s.replace('to_out_0', 'to_out.0')
    # transformer_blocks.<n>_ → transformer_blocks.<n>.
    import re
    s = re.sub(r'transformer_blocks\.(\d+)_', r'transformer_blocks.\1.', s)
    s = re.sub(r'\.ff\.net\.(\d+)_', r'.ff.net.\1.', s)
    return s


def _translate_te_key(suffix: str) -> str:
    """Map kohya TE1 key to diffusers text_model path.

    Example: text_model_encoder_layers_0_mlp_fc1 → text_model.encoder.layers.0.mlp.fc1
             text_model_encoder_layers_0_self_attn_k_proj → text_model.encoder.layers.0.self_attn.k_proj
    """
    import re
    s = suffix
    s = s.replace('text_model_', 'text_model.')
    s = s.replace('encoder_layers_', 'encoder.layers.')
    s = re.sub(r'encoder\.layers\.(\d+)_', r'encoder.layers.\1.', s)
    s = s.replace('_mlp_', '.mlp.')
    s = s.replace('_self_attn_', '.self_attn.')
    s = s.replace('_layer_norm', '.layer_norm')
    s = s.replace('final_layer_norm', 'final_layer_norm')  # leave as-is
    s = s.replace('_k_proj', '.k_proj').replace('_q_proj', '.q_proj')
    s = s.replace('_v_proj', '.v_proj').replace('_out_proj', '.out_proj')
    s = s.replace('_fc1', '.fc1').replace('_fc2', '.fc2')
    return s


def merge_sgm_lora_into_pipeline(pipe, path: str, alpha: float = 1.0):
    from safetensors.torch import load_file
    state = load_file(path)

    # Group keys by base module path → collect down/up/alpha
    pairs = {}
    for key, val in state.items():
        for marker in ('.lora_down.weight', '.lora_up.weight', '.alpha'):
            if key.endswith(marker):
                base = key[:-len(marker)]
                kind = marker.strip('.').replace('.weight', '')  # 'lora_down' | 'lora_up' | 'alpha'
                pairs.setdefault(base, {})[kind] = val
                break

    merged = 0
    skipped = 0
    for base, parts in pairs.items():
        if 'lora_down' not in parts or 'lora_up' not in parts:
            continue

        # Route into UNet attention or text encoder
        if base.startswith('lora_unet_'):
            rest = base[len('lora_unet_'):]
            block_prefix = None
            suffix = None
            for p, diff_path in SGM_UNET_ATTN_MAP.items():
                if rest.startswith(p + '_'):
                    block_prefix = diff_path
                    suffix = rest[len(p) + 1:]
                    break
                if rest == p:
                    block_prefix = diff_path
                    suffix = ''
                    break
            if block_prefix is None:
                skipped += 1
                continue
            tail = _translate_attn_suffix(suffix) if suffix else ''
            full_path = block_prefix + ('.' + tail if tail else '')
            module = _walk(pipe.unet, full_path)
        elif base.startswith('lora_te1_') or base.startswith('lora_te_'):
            rest = base.split('_', 2)[2] if base.startswith('lora_te1_') else base[len('lora_te_'):]
            full_path = _translate_te_key(rest)
            module = _walk(pipe.text_encoder, full_path)
        else:
            skipped += 1
            continue

        if module is None or not hasattr(module, 'weight'):
            skipped += 1
            continue

        down = parts['lora_down'].to(module.weight.device, dtype=torch.float32)
        up = parts['lora_up'].to(module.weight.device, dtype=torch.float32)
        rank = down.shape[0]
        a = float(parts.get('alpha', rank))
        scale = alpha * (a / rank)
        if down.dim() == 4:
            delta = (up.squeeze(3).squeeze(2) @ down.squeeze(3).squeeze(2)).unsqueeze(2).unsqueeze(3)
        else:
            delta = up @ down
        try:
            with torch.no_grad():
                module.weight.data += (scale * delta).to(module.weight.dtype)
            merged += 1
        except Exception:
            skipped += 1
    print(f'  LoRA merge: {merged} merged, {skipped} skipped')


def _walk(root, dotted: str):
    obj = root
    for part in dotted.split('.'):
        if part == '':
            continue
        if part.isdigit():
            try:
                obj = obj[int(part)]
            except (IndexError, TypeError, KeyError):
                return None
        else:
            obj = getattr(obj, part, None)
            if obj is None:
                return None
    return obj


def apply_kohya_lora(pipe, path: str, alpha: float = 1.0):
    """Manually merge a kohya-format LoRA into the SD unet + text_encoder."""
    from safetensors.torch import load_file
    state = load_file(path)
    unet = pipe.unet
    text_encoder = pipe.text_encoder

    # kohya keys look like:
    #   lora_unet_down_blocks_0_attentions_0_transformer_blocks_0_attn1_to_q.lora_down.weight
    #   lora_unet_down_blocks_0_attentions_0_transformer_blocks_0_attn1_to_q.lora_up.weight
    #   lora_unet_..._alpha
    #   lora_te_text_model_encoder_layers_0_self_attn_q_proj.lora_down.weight
    merged = 0
    pairs = {}
    for key, val in state.items():
        if key.endswith('.alpha'):
            base = key[:-len('.alpha')]
            pairs.setdefault(base, {})['alpha'] = val
        elif '.lora_down.' in key:
            base = key.split('.lora_down.')[0]
            pairs.setdefault(base, {})['down'] = val
        elif '.lora_up.' in key:
            base = key.split('.lora_up.')[0]
            pairs.setdefault(base, {})['up'] = val

    for base, parts in pairs.items():
        if 'down' not in parts or 'up' not in parts:
            continue
        # Resolve to actual module
        if base.startswith('lora_unet_'):
            target = base[len('lora_unet_'):]
            module = _resolve_unet(unet, target)
        elif base.startswith('lora_te_'):
            target = base[len('lora_te_'):]
            module = _resolve_te(text_encoder, target)
        else:
            continue
        if module is None:
            continue
        down = parts['down'].to(module.weight.device, dtype=torch.float32)
        up = parts['up'].to(module.weight.device, dtype=torch.float32)
        rank = down.shape[0]
        a = float(parts.get('alpha', rank))
        scale = alpha * (a / rank)
        # Compute delta: up @ down, shapes (out, rank) @ (rank, in) = (out, in)
        if down.dim() == 4:
            # Conv lora
            delta = (up.squeeze(3).squeeze(2) @ down.squeeze(3).squeeze(2)).unsqueeze(2).unsqueeze(3)
        else:
            delta = up @ down
        with torch.no_grad():
            module.weight.data += (scale * delta).to(module.weight.dtype)
        merged += 1
    print(f'  merged {merged} LoRA pairs')


def _resolve_unet(unet, target: str):
    """Resolve a kohya-style flat dotted name to an actual nn.Module inside UNet."""
    # kohya uses underscores for block separators; try converting back.
    # Example: 'down_blocks_0_attentions_0_transformer_blocks_0_attn1_to_q'
    # becomes 'down_blocks.0.attentions.0.transformer_blocks.0.attn1.to_q'
    import re
    candidate = re.sub(r'_(\d+)_', r'.\1.', target)
    candidate = candidate.replace('_', '.')
    # Fix known segments that shouldn't be dotted
    candidate = candidate.replace('transformer.blocks', 'transformer_blocks')
    candidate = candidate.replace('time.emb.proj', 'time_emb_proj')
    candidate = candidate.replace('conv.shortcut', 'conv_shortcut')
    candidate = candidate.replace('to.q', 'to_q').replace('to.k', 'to_k')
    candidate = candidate.replace('to.v', 'to_v').replace('to.out', 'to_out')
    candidate = candidate.replace('ff.net', 'ff.net').replace('net.0.proj', 'net.0.proj')
    candidate = candidate.replace('proj.in', 'proj_in').replace('proj.out', 'proj_out')
    return _walk_attrs(unet, candidate)


def _resolve_te(text_encoder, target: str):
    import re
    candidate = re.sub(r'_(\d+)_', r'.\1.', target)
    candidate = candidate.replace('_', '.')
    candidate = candidate.replace('text.model', 'text_model')
    candidate = candidate.replace('self.attn', 'self_attn')
    candidate = candidate.replace('encoder.layers', 'encoder.layers')
    candidate = candidate.replace('final.layer.norm', 'final_layer_norm')
    candidate = candidate.replace('q.proj', 'q_proj').replace('k.proj', 'k_proj')
    candidate = candidate.replace('v.proj', 'v_proj').replace('out.proj', 'out_proj')
    candidate = candidate.replace('fc.1', 'fc1').replace('fc.2', 'fc2')
    return _walk_attrs(text_encoder, candidate)


def _walk_attrs(root, dotted: str):
    obj = root
    for part in dotted.split('.'):
        if part.isdigit():
            try:
                obj = obj[int(part)]
            except (KeyError, IndexError, TypeError):
                return None
        else:
            obj = getattr(obj, part, None)
            if obj is None:
                return None
    return obj


def load_vanilla_init(color: str, target=512) -> Image.Image:
    path = VANILLA_DIR / f'{color}_concrete.png'
    img = Image.open(path).convert('RGB')
    # Scale 16->512 with nearest so each vanilla pixel becomes a 32x32 block.
    return img.resize((target, target), Image.Resampling.NEAREST)


def generate_one(pipe, variant, color, seed):
    color_phrase = COLOR_NAMES_LONG.get(color, color)
    prompt = PROMPTS[variant].format(color=color_phrase)
    init = load_vanilla_init(color)
    gen = torch.Generator(device='cuda').manual_seed(seed)
    img = pipe(
        prompt=prompt,
        image=init,
        negative_prompt=NEGATIVE,
        strength=DENOISING[variant],
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=gen,
    ).images[0]
    return img


def downscale_lanczos(img: Image.Image, target=16) -> Image.Image:
    """Downscale with contrast preservation: boost contrast pre-downscale, then LANCZOS."""
    from PIL import ImageEnhance
    # Two-step downscale (512→128→16) preserves more detail than direct 512→16
    mid = img.resize((128, 128), Image.Resampling.LANCZOS)
    # Boost contrast to recover what the average flattens
    mid = ImageEnhance.Contrast(mid).enhance(1.4)
    mid = ImageEnhance.Sharpness(mid).enhance(1.5)
    final = mid.resize((target, target), Image.Resampling.LANCZOS)
    return final.convert('RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variants', default='smooth,chiseled,polished,brick')
    ap.add_argument('--colors', default=','.join(COLORS))
    ap.add_argument('--keep-raw', action='store_true')
    args = ap.parse_args()

    variants = [v.strip() for v in args.variants.split(',')]
    colors = [c.strip() for c in args.colors.split(',')]

    raw_dir = HERE / 'sd_raw_v3'
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
            print(f'[{count}/{total}] {variant}_{color}_concrete (strength={DENOISING[variant]})... ',
                  end='', flush=True)
            t0 = time.time()
            raw = generate_one(pipe, variant, color, seed=seed)
            if args.keep_raw:
                raw.save(raw_dir / f'{variant}_{color}_512.png')
            small = downscale_lanczos(raw, 16)
            out_path = BLOCK_DIR / f'{variant}_{color}_concrete.png'
            small.save(out_path)
            print(f'{time.time() - t0:.1f}s')
            torch.cuda.empty_cache()
    total_time = time.time() - t_start
    print(f'\nDone. {count} textures in {total_time:.0f}s ({total_time/count:.1f}s avg).')


if __name__ == '__main__':
    main()
