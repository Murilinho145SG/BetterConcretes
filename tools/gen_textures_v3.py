"""
Procedural concrete texture generator v3.
Pattern references extracted from vanilla deepslate variants:
  - brick    -> deepslate_bricks (running bond: 1 top brick, 2 bottom bricks)
  - polished -> polished_deepslate (horizontal banding + noise)
  - chiseled -> chiseled_deepslate (symmetric carved decoration)
  - smooth   -> copper_block style (diagonal gradient + dense noise)

Input:  tools/vanilla/{color}_concrete.png  (base color sampler)
Output: tools/preview_v3/{variant}_{color}_concrete.png  (16x16)
Also writes scaled x8 previews to tools/preview_v3/x128/ for visual review.
"""
import os
import random
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA_DIR = os.path.join(ROOT, 'vanilla')
OUT_DIR = os.path.join(ROOT, 'preview_v3')
OUT_X128 = os.path.join(OUT_DIR, 'x128')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(OUT_X128, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']

VARIANTS = ['smooth', 'polished', 'chiseled', 'brick']


def sample_base_color(color_name):
    """Sample the dominant color from vanilla concrete texture."""
    path = os.path.join(VANILLA_DIR, f'{color_name}_concrete.png')
    img = Image.open(path).convert('RGB')
    px = img.load()
    # Average the center region (avoiding edges)
    rs, gs, bs = [], [], []
    for y in range(4, 12):
        for x in range(4, 12):
            r, g, b = px[x, y]
            rs.append(r); gs.append(g); bs.append(b)
    return (sum(rs)//len(rs), sum(gs)//len(gs), sum(bs)//len(bs))


def clamp(v):
    return max(0, min(255, int(v)))


def shift(rgb, delta):
    """Shift RGB by delta, preserving hue roughly."""
    return (clamp(rgb[0] + delta), clamp(rgb[1] + delta), clamp(rgb[2] + delta))


def palette(base):
    """Build 5-tier palette: highlight, light, base, shadow, dark."""
    # Darker colors need smaller deltas to stay visible; brighter need larger
    lum = 0.299*base[0] + 0.587*base[1] + 0.114*base[2]
    # Scale delta inversely to lum proximity to extremes
    d_up = int(28 + (255 - lum) * 0.12)
    d_down = int(28 + lum * 0.12)
    return {
        'highlight': shift(base, int(d_up * 1.4)),
        'light':     shift(base, int(d_up * 0.6)),
        'base':      base,
        'shadow':    shift(base, -int(d_down * 0.7)),
        'dark':      shift(base, -int(d_down * 1.4)),
    }


# ---------------- VARIANT GENERATORS ----------------

def gen_smooth(pal, rng):
    """Subtle dense noise on base color with a soft diagonal gradient (copper-inspired)."""
    img = Image.new('RGB', (16, 16), pal['base'])
    px = img.load()
    for y in range(16):
        for x in range(16):
            # Diagonal gradient bias
            g = (x + y) / 30.0  # 0..1
            r = rng.random()
            if r < 0.08 - g*0.05:
                c = pal['highlight']
            elif r < 0.20:
                c = pal['light']
            elif r < 0.72:
                c = pal['base']
            elif r < 0.88:
                c = pal['shadow']
            else:
                c = pal['dark']
            px[x, y] = c
    return img


def gen_polished(pal, rng):
    """Two horizontal bands separated by a dark line; bright top edges, subtle noise within."""
    img = Image.new('RGB', (16, 16), pal['base'])
    px = img.load()

    def fill_band(y0, y1):
        for y in range(y0, y1):
            for x in range(16):
                r = rng.random()
                # Slight brightness falloff from top of band
                rel = (y - y0) / max(1, (y1 - y0 - 1))
                if y == y0:
                    # top edge of band: brighter
                    px[x, y] = pal['light'] if r < 0.75 else pal['highlight']
                elif y == y1 - 1:
                    # bottom edge of band: darker
                    px[x, y] = pal['shadow'] if r < 0.75 else pal['dark']
                else:
                    if r < 0.12:
                        px[x, y] = pal['light']
                    elif r < 0.22:
                        px[x, y] = pal['shadow']
                    elif r < 0.27:
                        px[x, y] = pal['dark']
                    else:
                        px[x, y] = pal['base']

    fill_band(0, 7)   # top band rows 0-6
    # Row 7 = dark separator
    for x in range(16):
        px[x, 7] = pal['dark'] if rng.random() < 0.85 else pal['shadow']
    fill_band(8, 15)  # bottom band rows 8-14
    # Row 15 = dark bottom edge
    for x in range(16):
        px[x, 15] = pal['dark'] if rng.random() < 0.85 else pal['shadow']
    return img


def gen_chiseled(pal, rng):
    """Symmetric carved pattern: dark frame + vertical pillar decoration + horizontal band."""
    img = Image.new('RGB', (16, 16), pal['base'])
    px = img.load()

    # Fill body with subtle noise first
    for y in range(16):
        for x in range(16):
            r = rng.random()
            if r < 0.15:
                px[x, y] = pal['light']
            elif r < 0.25:
                px[x, y] = pal['shadow']
            else:
                px[x, y] = pal['base']

    # Dark border frame (1px)
    for i in range(16):
        px[i, 0] = pal['dark']
        px[i, 15] = pal['dark']
        px[0, i] = pal['dark']
        px[15, i] = pal['dark']

    # Inner bright rim right below border (top + left), dark below border (bottom + right)
    for i in range(1, 15):
        px[i, 1] = pal['light']
        px[1, i] = pal['light']
        px[i, 14] = pal['shadow']
        px[14, i] = pal['shadow']

    # Central horizontal band (rows 7-8) — the "chisel cut"
    for x in range(2, 14):
        px[x, 7] = pal['dark']
        px[x, 8] = pal['shadow']

    # Vertical chisel marks inside the panels
    # Top panel: rows 3-6, cols 5 and 10 get darker vertical notches
    for y in range(3, 7):
        px[5, y] = pal['shadow']
        px[10, y] = pal['shadow']
        px[6, y] = pal['dark']
        px[9, y] = pal['dark']

    # Bottom panel: mirror
    for y in range(9, 13):
        px[5, y] = pal['shadow']
        px[10, y] = pal['shadow']
        px[6, y] = pal['dark']
        px[9, y] = pal['dark']

    # Center highlight dots for interest
    px[7, 4] = pal['highlight']
    px[8, 4] = pal['highlight']
    px[7, 11] = pal['highlight']
    px[8, 11] = pal['highlight']

    return img


def _fill_brick(px, x0, y0, x1, y1, pal, rng):
    """Fill a rectangular brick with gradient + noise.

    Top-left gets highlight, bottom-right gets shadow, middle is base with noise."""
    w = x1 - x0
    h = y1 - y0
    for y in range(y0, y1):
        for x in range(x0, x1):
            # Relative position within brick
            rx = (x - x0)
            ry = (y - y0)
            r = rng.random()
            # Top edge brighter
            if ry == 0:
                c = pal['light'] if r < 0.7 else pal['highlight']
            # Bottom edge darker
            elif ry == h - 1:
                c = pal['shadow'] if r < 0.7 else pal['dark']
            # Left edge slightly lighter
            elif rx == 0 and r < 0.5:
                c = pal['light']
            # Right edge slightly darker
            elif rx == w - 1 and r < 0.5:
                c = pal['shadow']
            else:
                if r < 0.12:
                    c = pal['light']
                elif r < 0.22:
                    c = pal['shadow']
                elif r < 0.27:
                    c = pal['dark']
                else:
                    c = pal['base']
            px[x, y] = c


def gen_brick(pal, rng):
    """Running bond: 1 big brick on top (cols 0-14 rows 0-6), 2 on bottom (cols 0-6, 8-15)
    separated by mortar at row 7, row 15, col 15 (top), col 7 (bottom)."""
    img = Image.new('RGB', (16, 16), pal['base'])
    px = img.load()

    # Fill all with mortar color first
    for y in range(16):
        for x in range(16):
            px[x, y] = pal['dark'] if rng.random() < 0.7 else pal['shadow']

    # Top brick: cols 0-14, rows 0-6
    _fill_brick(px, 0, 0, 15, 7, pal, rng)
    # Bottom-left brick: cols 0-6, rows 8-14
    _fill_brick(px, 0, 8, 7, 15, pal, rng)
    # Bottom-right brick: cols 8-15, rows 8-14
    _fill_brick(px, 8, 8, 16, 15, pal, rng)

    return img


GENERATORS = {
    'smooth':   gen_smooth,
    'polished': gen_polished,
    'chiseled': gen_chiseled,
    'brick':    gen_brick,
}


def color_seed(color, variant):
    # Deterministic per (color, variant) so regenerations are stable
    h = hash((color, variant)) & 0xFFFFFFFF
    return h


def generate_all(colors=None):
    colors = colors or COLORS
    for color in colors:
        base = sample_base_color(color)
        pal = palette(base)
        for variant in VARIANTS:
            rng = random.Random(color_seed(color, variant))
            img = GENERATORS[variant](pal, rng)
            out_name = f'{variant}_{color}_concrete.png'
            img.save(os.path.join(OUT_DIR, out_name))
            # x128 nearest for visual review
            img.resize((128, 128), Image.NEAREST).save(
                os.path.join(OUT_X128, out_name.replace('.png', '_x128.png'))
            )
        print(f'  {color}: base={base} -> {len(VARIANTS)} variants')
    print(f'\nwrote {len(colors)*len(VARIANTS)} textures to {OUT_DIR}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        generate_all(sys.argv[1:])
    else:
        generate_all()
