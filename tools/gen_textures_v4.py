"""
Texture generator v4 — uses vanilla textures as luminance masks, recolored per concrete.

Strategy: pick one vanilla block texture per variant. Extract its normalized luminance
(0..1) per pixel. Remap that luminance to a per-concrete-color gradient palette.
Result looks 100% vanilla-Minecraft style because the pattern IS vanilla; only the
hue changes.
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA = os.path.join(ROOT, 'vanilla')
REF = os.path.join(ROOT, 'reference_vanilla', 'all_blocks')
OUT = os.path.join(ROOT, 'preview_v4')
OUT_X128 = os.path.join(OUT, 'x128')
os.makedirs(OUT, exist_ok=True)
os.makedirs(OUT_X128, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']

# Which vanilla texture provides the luminance/pattern mask per variant.
MASK_SOURCES = {
    'smooth':   'copper_block.png',
    'polished': 'polished_deepslate.png',
    'chiseled': 'chiseled_stone_bricks.png',
    'brick':    'bricks.png',
}


def load_mask(path):
    """Load vanilla texture and return (lum_array, lum_min, lum_max) in 0..255."""
    img = Image.open(path).convert('RGB')
    px = img.load()
    lums = []
    for y in range(16):
        row = []
        for x in range(16):
            r, g, b = px[x, y]
            row.append(int(0.299*r + 0.587*g + 0.114*b))
        lums.append(row)
    flat = [v for r in lums for v in r]
    return lums, min(flat), max(flat)


def sample_base_color(color_name):
    path = os.path.join(VANILLA, f'{color_name}_concrete.png')
    img = Image.open(path).convert('RGB')
    px = img.load()
    rs, gs, bs = [], [], []
    for y in range(4, 12):
        for x in range(4, 12):
            r, g, b = px[x, y]
            rs.append(r); gs.append(g); bs.append(b)
    return (sum(rs)//len(rs), sum(gs)//len(gs), sum(bs)//len(bs))


def clamp(v):
    return max(0, min(255, int(v)))


def remap_color(base, t):
    """Map t in 0..1 to a color biased by `base`.
    t=0 -> very dark, t=0.5 -> base, t=1 -> very light, preserving hue of base."""
    lum_base = 0.299*base[0] + 0.587*base[1] + 0.114*base[2]
    # Amplitude scales so dark colors don't crush to pure black
    # and bright colors don't blow out to pure white.
    down = min(lum_base * 0.85, 80)
    up = min((255 - lum_base) * 0.85, 80)
    # t<0.5 -> darken, t>0.5 -> lighten, linear
    if t < 0.5:
        delta = -down * (1 - t*2)
    else:
        delta = up * (t*2 - 1)
    return (clamp(base[0]+delta), clamp(base[1]+delta), clamp(base[2]+delta))


def generate(variant, color):
    mask_path = os.path.join(REF, MASK_SOURCES[variant])
    lums, lmn, lmx = load_mask(mask_path)
    base = sample_base_color(color)
    img = Image.new('RGB', (16, 16))
    px = img.load()
    lrange = max(1, lmx - lmn)
    for y in range(16):
        for x in range(16):
            # Normalize lum to 0..1 based on this mask's actual range
            t = (lums[y][x] - lmn) / lrange
            px[x, y] = remap_color(base, t)
    return img


def generate_all(colors=None, variants=None):
    colors = colors or COLORS
    variants = variants or list(MASK_SOURCES.keys())
    for color in colors:
        for variant in variants:
            img = generate(variant, color)
            name = f'{variant}_{color}_concrete.png'
            img.save(os.path.join(OUT, name))
            img.resize((128, 128), Image.NEAREST).save(
                os.path.join(OUT_X128, name.replace('.png', '_x128.png'))
            )
    total = len(colors) * len(variants)
    print(f'wrote {total} textures to {OUT}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        generate_all(colors=args)
    else:
        generate_all()
