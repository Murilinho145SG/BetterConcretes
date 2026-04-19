"""
Texture generator v6 — CONCRETE-feel with detailed structure.

v5 preserved vanilla concrete color perfectly but was "too plain".
v6 keeps the same color fidelity (brick/panel bodies = vanilla concrete grid)
and adds meaningful structural + surface detail per variant.

Design principles:
- Majority of pixels keep vanilla concrete RGB (so it still reads as concrete).
- Structural features (mortar, frames, seams) use a stronger shift (~30 lum) to be
  clearly visible.
- Surface features (aggregate specks, chips, per-brick tonal variation) use small
  shifts (~8-15 lum) to add detail without stone-style roughness.
- Deterministic per (color, variant) RNG for stable regens.
"""
import os
import sys
import random
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA = os.path.join(ROOT, 'vanilla')
OUT = os.path.join(ROOT, 'preview_v6')
OUT_X128 = os.path.join(OUT, 'x128')
os.makedirs(OUT, exist_ok=True)
os.makedirs(OUT_X128, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']


def clamp(v):
    return max(0, min(255, int(v)))


def shift_rgb(rgb, delta):
    return (clamp(rgb[0]+delta), clamp(rgb[1]+delta), clamp(rgb[2]+delta))


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
    """Return delta values calibrated to the base color.
    Structural deltas scale with lum so dark colors don't clip to black and
    bright colors don't blow out. Returns dict of named deltas."""
    lum = 0.299*avg[0] + 0.587*avg[1] + 0.114*avg[2]
    return {
        'mortar_deep':  -int(max(20, min(55, lum * 0.20))),   # main mortar lines
        'shadow':       -int(max(12, min(32, lum * 0.12))),   # edge shadows
        'micro_dark':   -int(max(6,  min(16, lum * 0.06))),   # subtle specks
        'micro_light':   int(max(5,  min(14, (255-lum) * 0.06))),
        'highlight':     int(max(10, min(28, (255-lum) * 0.11))),
        'strong_light':  int(max(15, min(40, (255-lum) * 0.16))),
    }


# ---------------- helpers ----------------

def copy_grid(grid):
    return [row[:] for row in grid]


def set_px(grid, x, y, rgb):
    if 0 <= x < 16 and 0 <= y < 16:
        grid[y][x] = rgb


def shift_px(grid, x, y, delta):
    if 0 <= x < 16 and 0 <= y < 16:
        grid[y][x] = shift_rgb(grid[y][x], delta)


def scatter(grid, rng, count, delta, forbidden=None):
    forbidden = forbidden or set()
    placed = 0
    attempts = 0
    while placed < count and attempts < count*6:
        attempts += 1
        x = rng.randrange(16)
        y = rng.randrange(16)
        if (x, y) in forbidden:
            continue
        shift_px(grid, x, y, delta)
        placed += 1


# ---------------- VARIANTS ----------------

def make_smooth(grid, avg, rng):
    """Concrete + exposed-aggregate speckles + soft diagonal sheen.
    Gives the "polished finished concrete with fine aggregate visible" look."""
    t = tiers(avg)
    out = copy_grid(grid)

    # Aggregate dark specks (small darker stones in the mix) — ~12 pixels
    scatter(out, rng, 12, t['micro_dark'])
    # Aggregate light specks (bright minerals) — ~8 pixels
    scatter(out, rng, 8, t['micro_light'])
    # A few stronger specks — like visible aggregate chunks
    scatter(out, rng, 3, int(t['shadow']*0.8))
    scatter(out, rng, 2, int(t['highlight']*0.7))

    # Gentle diagonal sheen (polished finish gloss)
    for y in range(16):
        for x in range(16):
            diag = x + y
            if diag in (10, 11, 12):
                bump = t['micro_light'] // 2 if diag != 11 else t['micro_light']
                shift_px(out, x, y, bump)

    # Soft corner shading for a subtle 3D-ish feel
    for i in range(3):
        for j in range(3):
            if i + j <= 2:
                shift_px(out, 15-i, 15-j, t['micro_dark'])
                shift_px(out, i, j, t['micro_light']//2)
    return out


def make_polished(grid, avg, rng):
    """Concrete + 2 horizontal seams -> 3 bands (like stacked precast panels),
    with highlight/shadow edges and chamfered corners."""
    t = tiers(avg)
    out = copy_grid(grid)

    # Two seam rows: at row 5 and row 10
    for x in range(16):
        shift_px(out, x, 5, t['mortar_deep']//2)
        shift_px(out, x, 10, t['mortar_deep']//2)

    # Highlight row below each seam (top edge of lower panel catches light)
    for x in range(16):
        shift_px(out, x, 6, t['highlight'])
        shift_px(out, x, 11, t['highlight'])

    # Shadow row above each seam (underside of upper panel in shadow)
    for x in range(16):
        shift_px(out, x, 4, t['shadow']//2)
        shift_px(out, x, 9, t['shadow']//2)

    # Top bright edge (block top catches overhead light)
    for x in range(16):
        shift_px(out, x, 0, t['strong_light']//2)
    # Bottom dark edge
    for x in range(16):
        shift_px(out, x, 15, t['shadow'])

    # Chamfered corners — 2 pixels at each corner
    shift_px(out, 0, 0, t['strong_light']//2)
    shift_px(out, 1, 0, t['highlight'])
    shift_px(out, 0, 1, t['highlight'])
    shift_px(out, 15, 15, t['shadow'])
    shift_px(out, 14, 15, t['shadow']//2)
    shift_px(out, 15, 14, t['shadow']//2)

    # Subtle surface speckles for grain
    scatter(out, rng, 6, t['micro_dark'])
    scatter(out, rng, 4, t['micro_light'])
    return out


def make_chiseled(grid, avg, rng):
    """Concrete + decorative recessed panel: outer rim, inner bevel,
    central motif (plus sign), corner accents.
    Architectural precast concrete look."""
    t = tiers(avg)
    out = copy_grid(grid)

    # ---- Outer rim at (1,1)-(14,14) — the frame border
    for i in range(1, 15):
        shift_px(out, i, 1,  t['highlight'])   # top rim bright (rim catches light)
        shift_px(out, i, 14, t['shadow'])      # bottom rim dark
        shift_px(out, 1, i,  t['highlight']//2)
        shift_px(out, 14, i, t['shadow']//2)

    # ---- Inset recess rim at (2,2)-(13,13) — the inset "dig" edge
    for i in range(2, 14):
        shift_px(out, i, 2,  t['mortar_deep']//2)
        shift_px(out, i, 13, t['mortar_deep']//2)
        shift_px(out, 2, i,  t['mortar_deep']//2)
        shift_px(out, 13, i, t['mortar_deep']//2)

    # ---- Inset body (3-12, 3-12) slightly lighter (recessed plate)
    for y in range(3, 13):
        for x in range(3, 13):
            shift_px(out, x, y, t['micro_light'])

    # ---- Central plus-sign motif
    # Horizontal arm
    for x in range(6, 10):
        shift_px(out, x, 7, t['shadow']//2)
        shift_px(out, x, 8, t['shadow']//2)
    # Vertical arm
    for y in range(6, 10):
        shift_px(out, 7, y, t['shadow']//2)
        shift_px(out, 8, y, t['shadow']//2)
    # Plus center (darkest point)
    for (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)]:
        shift_px(out, x, y, t['shadow'])
    # Plus top-left highlight edges for bevel effect
    shift_px(out, 6, 7, t['highlight']//2)
    shift_px(out, 7, 6, t['highlight']//2)

    # ---- Corner accents on inset body
    for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        shift_px(out, x, y, t['shadow']//2)

    # ---- Outer border dark pixels at the block's 4 corners (bevel)
    shift_px(out, 0, 0, t['shadow'])
    shift_px(out, 15, 0, t['shadow'])
    shift_px(out, 0, 15, t['shadow'])
    shift_px(out, 15, 15, t['shadow'])

    # Small grain specks for life
    scatter(out, rng, 5, t['micro_dark'],
            forbidden={(x,y) for x in range(6,10) for y in range(6,10)})
    return out


def _fill_brick(out, x0, y0, x1, y1, avg, rng, tone_delta):
    """Fill one brick with vanilla-concrete-style body + edge highlights/shadows.
    Each brick gets a small overall tone offset (tone_delta) so bricks vary.
    Also adds a top-edge highlight and bottom-edge shadow, plus 1-2 chips."""
    t = tiers(avg)
    # Apply tone offset to whole brick body
    for y in range(y0, y1):
        for x in range(x0, x1):
            shift_px(out, x, y, tone_delta)

    # Top edge highlight (light catches top of brick)
    for x in range(x0, x1):
        shift_px(out, x, y0, t['highlight']//2)
    # Bottom edge shadow
    for x in range(x0, x1):
        shift_px(out, x, y1-1, t['shadow']//2)
    # Left edge slight highlight, right edge slight shadow
    for y in range(y0, y1):
        shift_px(out, x0, y, t['micro_light']//2)
        shift_px(out, x1-1, y, t['micro_dark']//2)

    # Small imperfections: 1-2 random darker specks (small chips)
    w = x1 - x0
    h = y1 - y0
    chip_count = 1 + rng.randrange(2)
    for _ in range(chip_count):
        cx = x0 + 1 + rng.randrange(max(1, w-2))
        cy = y0 + 1 + rng.randrange(max(1, h-2))
        shift_px(out, cx, cy, t['shadow'])
    # And a single bright aggregate speck
    if rng.random() < 0.6:
        cx = x0 + 1 + rng.randrange(max(1, w-2))
        cy = y0 + 1 + rng.randrange(max(1, h-2))
        shift_px(out, cx, cy, t['micro_light'])


def make_brick(grid, avg, rng):
    """Concrete masonry brick (CMU) running-bond layout.
    - Strong mortar lines (~-40 lum) for clear brick separation
    - Per-brick tonal variation (each brick slightly different shade)
    - Edge highlights/shadows, small chips, aggregate specks per brick"""
    t = tiers(avg)
    out = copy_grid(grid)

    # ---- Fill mortar channels first (we'll overwrite brick bodies next)
    # Horizontal mortar rows: 7 and 15
    for x in range(16):
        shift_px(out, x, 7, t['mortar_deep'])
        shift_px(out, x, 15, t['mortar_deep'])
    # Vertical mortar: col 15 (top half rows 0-6), col 7 (bottom half rows 8-14)
    for y in range(7):
        shift_px(out, 15, y, t['mortar_deep'])
    for y in range(8, 15):
        shift_px(out, 7, y, t['mortar_deep'])

    # ---- Per-brick tone offsets (small, so bricks still look matched)
    # Top brick (0-14, 0-6), bottom-left (0-6, 8-14), bottom-right (8-15, 8-14)
    bricks = [
        (0, 0, 15, 7),    # top
        (0, 8, 7, 15),    # bottom-left
        (8, 8, 16, 15),   # bottom-right
    ]
    for (x0, y0, x1, y1) in bricks:
        tone = rng.choice([-t['micro_dark']//2, 0, t['micro_light']//2, -t['micro_dark'], t['micro_light']])
        _fill_brick(out, x0, y0, x1, y1, avg, rng, tone)

    # ---- Mortar inner shadow (row below horizontal mortar gets a subtle shadow)
    for x in range(16):
        shift_px(out, x, 8, t['shadow']//3)  # below top mortar, top of lower row
    # Highlight on top of top row (row 0) to accent
    for x in range(16):
        shift_px(out, x, 0, t['micro_light']//2)

    return out


GENERATORS = {
    'smooth':   make_smooth,
    'polished': make_polished,
    'chiseled': make_chiseled,
    'brick':    make_brick,
}


def color_seed(color, variant):
    return hash((color, variant, 'v6')) & 0xFFFFFFFF


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
    total = len(colors) * len(variants)
    print(f'wrote {total} textures to {OUT}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        generate_all(colors=args)
    else:
        generate_all()
