"""
Texture generator v7 — HSL-aware concrete shader.

Changes from v6:
- All "shifts" go through HSL lightness, preserving Hue and Saturation.
  Strong colors (red/yellow/blue) no longer desaturate when darkened.
- Per-brick tone variation is symmetric (balanced ±delta choices, no double-dip).
- Chip darkness is clamped so dark concretes don't collapse to pure black.
"""
import os
import sys
import random
import colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA = os.path.join(ROOT, 'vanilla')
OUT = os.path.join(ROOT, 'preview_v7')
OUT_X128 = os.path.join(OUT, 'x128')
os.makedirs(OUT, exist_ok=True)
os.makedirs(OUT_X128, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, v))


def lshift(rgb, dL):
    """Shift lightness in HSL space. dL is delta on 0..255 scale.
    Preserves hue and saturation. Clamps L to safe range to avoid total loss."""
    r, g, b = [c/255.0 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = clamp(l + dL/255.0, 0.04, 0.96)  # never pure black / pure white
    r2, g2, b2 = colorsys.hls_to_rgb(h, new_l, s)
    return (int(round(r2*255)), int(round(g2*255)), int(round(b2*255)))


def load_base(color):
    img = Image.open(os.path.join(VANILLA, f'{color}_concrete.png')).convert('RGB')
    px = img.load()
    grid = [[px[x, y] for x in range(16)] for y in range(16)]
    flat = [grid[y][x] for y in range(16) for x in range(16)]
    avg = (
        sum(p[0] for p in flat) // 256,
        sum(p[1] for p in flat) // 256,
        sum(p[2] for p in flat) // 256,
    )
    return grid, avg


def tiers(avg):
    """Symmetric delta tiers in HSL-L units (0..255). Scales with headroom on each side."""
    lum = 0.299*avg[0] + 0.587*avg[1] + 0.114*avg[2]
    # Room to darken / lighten before hitting clamp
    room_dark = max(20, lum - 10)   # keep at least 10 lum of headroom
    room_light = max(20, 245 - lum)
    # Per-feature shift amplitudes (tuned)
    return {
        'mortar_deep':  -int(min(40, room_dark * 0.45)),
        'shadow':       -int(min(25, room_dark * 0.28)),
        'micro_dark':   -int(min(12, room_dark * 0.12)),
        'micro_light':   int(min(11, room_light * 0.11)),
        'highlight':     int(min(22, room_light * 0.24)),
        'strong_light':  int(min(32, room_light * 0.36)),
    }


# ---------------- helpers ----------------

def copy_grid(grid):
    return [row[:] for row in grid]


def set_px(grid, x, y, rgb):
    if 0 <= x < 16 and 0 <= y < 16:
        grid[y][x] = rgb


def shift_px(grid, x, y, dL):
    if 0 <= x < 16 and 0 <= y < 16:
        grid[y][x] = lshift(grid[y][x], dL)


def scatter(grid, rng, count, dL, forbidden=None):
    forbidden = forbidden or set()
    placed, attempts = 0, 0
    while placed < count and attempts < count*6:
        attempts += 1
        x, y = rng.randrange(16), rng.randrange(16)
        if (x, y) in forbidden:
            continue
        shift_px(grid, x, y, dL)
        placed += 1


# ---------------- VARIANTS ----------------

def make_smooth(grid, avg, rng):
    t = tiers(avg)
    out = copy_grid(grid)
    scatter(out, rng, 12, t['micro_dark'])
    scatter(out, rng, 8, t['micro_light'])
    scatter(out, rng, 3, int(t['shadow']*0.8))
    scatter(out, rng, 2, int(t['highlight']*0.7))
    for y in range(16):
        for x in range(16):
            diag = x + y
            if diag in (10, 11, 12):
                bump = t['micro_light']//2 if diag != 11 else t['micro_light']
                shift_px(out, x, y, bump)
    for i in range(3):
        for j in range(3):
            if i + j <= 2:
                shift_px(out, 15-i, 15-j, t['micro_dark'])
                shift_px(out, i, j, t['micro_light']//2)
    return out


def make_polished(grid, avg, rng):
    t = tiers(avg)
    out = copy_grid(grid)
    for x in range(16):
        shift_px(out, x, 5, t['mortar_deep']//2)
        shift_px(out, x, 10, t['mortar_deep']//2)
        shift_px(out, x, 6, t['highlight'])
        shift_px(out, x, 11, t['highlight'])
        shift_px(out, x, 4, t['shadow']//2)
        shift_px(out, x, 9, t['shadow']//2)
        shift_px(out, x, 0, t['strong_light']//2)
        shift_px(out, x, 15, t['shadow'])
    shift_px(out, 0, 0, t['strong_light']//2)
    shift_px(out, 1, 0, t['highlight'])
    shift_px(out, 0, 1, t['highlight'])
    shift_px(out, 15, 15, t['shadow'])
    shift_px(out, 14, 15, t['shadow']//2)
    shift_px(out, 15, 14, t['shadow']//2)
    scatter(out, rng, 6, t['micro_dark'])
    scatter(out, rng, 4, t['micro_light'])
    return out


def make_chiseled(grid, avg, rng):
    t = tiers(avg)
    out = copy_grid(grid)
    for i in range(1, 15):
        shift_px(out, i, 1,  t['highlight'])
        shift_px(out, i, 14, t['shadow'])
        shift_px(out, 1, i,  t['highlight']//2)
        shift_px(out, 14, i, t['shadow']//2)
    for i in range(2, 14):
        shift_px(out, i, 2,  t['mortar_deep']//2)
        shift_px(out, i, 13, t['mortar_deep']//2)
        shift_px(out, 2, i,  t['mortar_deep']//2)
        shift_px(out, 13, i, t['mortar_deep']//2)
    for y in range(3, 13):
        for x in range(3, 13):
            shift_px(out, x, y, t['micro_light'])
    # Central plus motif
    for x in range(6, 10):
        shift_px(out, x, 7, t['shadow']//2)
        shift_px(out, x, 8, t['shadow']//2)
    for y in range(6, 10):
        shift_px(out, 7, y, t['shadow']//2)
        shift_px(out, 8, y, t['shadow']//2)
    for (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)]:
        shift_px(out, x, y, t['shadow'])
    shift_px(out, 6, 7, t['highlight']//2)
    shift_px(out, 7, 6, t['highlight']//2)
    for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        shift_px(out, x, y, t['shadow']//2)
    for (x, y) in [(0,0),(15,0),(0,15),(15,15)]:
        shift_px(out, x, y, t['shadow'])
    scatter(out, rng, 5, t['micro_dark'],
            forbidden={(x,y) for x in range(6,10) for y in range(6,10)})
    return out


def _fill_brick(out, x0, y0, x1, y1, t, rng, tone_dL):
    for y in range(y0, y1):
        for x in range(x0, x1):
            shift_px(out, x, y, tone_dL)
    for x in range(x0, x1):
        shift_px(out, x, y0, t['highlight']//2)
        shift_px(out, x, y1-1, t['shadow']//2)
    for y in range(y0, y1):
        shift_px(out, x0, y, t['micro_light']//2)
        shift_px(out, x1-1, y, t['micro_dark']//2)
    w, h = x1 - x0, y1 - y0
    chip_count = 1 + rng.randrange(2)
    for _ in range(chip_count):
        cx = x0 + 1 + rng.randrange(max(1, w-2))
        cy = y0 + 1 + rng.randrange(max(1, h-2))
        # Chips clamped so dark colors don't collapse
        shift_px(out, cx, cy, int(t['shadow'] * 0.8))
    if rng.random() < 0.6:
        cx = x0 + 1 + rng.randrange(max(1, w-2))
        cy = y0 + 1 + rng.randrange(max(1, h-2))
        shift_px(out, cx, cy, t['micro_light'])


def make_brick(grid, avg, rng):
    t = tiers(avg)
    out = copy_grid(grid)
    # Mortar channels
    for x in range(16):
        shift_px(out, x, 7, t['mortar_deep'])
        shift_px(out, x, 15, t['mortar_deep'])
    for y in range(7):
        shift_px(out, 15, y, t['mortar_deep'])
    for y in range(8, 15):
        shift_px(out, 7, y, t['mortar_deep'])

    # Symmetric per-brick tone options: equal number of dark and light
    tone_options = [-t['micro_dark']//2, 0, t['micro_light']//2]
    bricks = [
        (0, 0, 15, 7),    # top
        (0, 8, 7, 15),    # bottom-left
        (8, 8, 16, 15),   # bottom-right
    ]
    # Shuffle tone choices to ensure variety without double-darkening
    rng.shuffle(tone_options)
    for (brick, tone) in zip(bricks, tone_options):
        x0, y0, x1, y1 = brick
        _fill_brick(out, x0, y0, x1, y1, t, rng, tone)

    for x in range(16):
        shift_px(out, x, 8, t['shadow']//3)
        shift_px(out, x, 0, t['micro_light']//2)
    return out


GENERATORS = {
    'smooth':   make_smooth,
    'polished': make_polished,
    'chiseled': make_chiseled,
    'brick':    make_brick,
}


def color_seed(color, variant):
    return hash((color, variant, 'v7')) & 0xFFFFFFFF


def grid_to_image(grid):
    img = Image.new('RGB', (16, 16))
    for y in range(16):
        for x in range(16):
            img.putpixel((x, y), grid[y][x])
    return img


def generate_all(colors=None, variants=None):
    colors = colors or COLORS
    variants = variants or list(GENERATORS.keys())
    for color in colors:
        grid, avg = load_base(color)
        for variant in variants:
            rng = random.Random(color_seed(color, variant))
            out_grid = GENERATORS[variant](grid, avg, rng)
            img = grid_to_image(out_grid)
            name = f'{variant}_{color}_concrete.png'
            img.save(os.path.join(OUT, name))
            img.resize((128, 128), Image.NEAREST).save(
                os.path.join(OUT_X128, name.replace('.png', '_x128.png'))
            )
    print(f'wrote {len(colors)*len(variants)} textures to {OUT}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        generate_all(colors=args)
    else:
        generate_all()
