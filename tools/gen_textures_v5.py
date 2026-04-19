"""
Texture generator v5 — CONCRETE-feel.

Key insight: vanilla concrete has lum range ~3 (almost flat color with tiny dither).
Stone textures have lum range 50-100. If our variants use high contrast like the stone
references, they stop looking like concrete and start looking like painted stone.

Strategy:
  - For each color, use the 16x16 vanilla concrete texture as the PIXEL-PATTERN BASE.
    This preserves the exact concrete grain and hue.
  - Overlay structural modifications (mortar lines, panel seams, inset frames) with
    SMALL lum shifts so the concrete feel survives.

Variants:
  - smooth:   vanilla concrete + optional diagonal sheen line (polished concrete look)
  - polished: vanilla concrete + subtle horizontal seam at mid (precast panel seam)
  - chiseled: vanilla concrete + subtle rectangular inset panel (architectural precast)
  - brick:    vanilla concrete + running-bond mortar grid (concrete masonry unit / CMU)
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA = os.path.join(ROOT, 'vanilla')
OUT = os.path.join(ROOT, 'preview_v5')
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
    """Return (pixel_grid, avg_rgb). pixel_grid[y][x] = (r,g,b) from vanilla texture."""
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


def adaptive_delta(base_rgb, direction):
    """Scale structural shift by how much room we have before clipping.
    direction: -1 for darker mortar/inset, +1 for brighter sheen.
    Returns a lum delta in range ~[5, 22].
    """
    lum = 0.299*base_rgb[0] + 0.587*base_rgb[1] + 0.114*base_rgb[2]
    if direction < 0:
        # darker — bigger shift for bright colors, smaller for dark
        return -int(max(6, min(22, lum * 0.10)))
    else:
        return int(max(5, min(18, (255 - lum) * 0.10)))


# ---------------- VARIANTS ----------------

def make_smooth(grid, avg):
    """Concrete + faint diagonal sheen (polished concrete with slight gloss bias)."""
    d_up = adaptive_delta(avg, +1)
    out = [[grid[y][x] for x in range(16)] for y in range(16)]
    # Diagonal sheen line: 2px-wide band along one anti-diagonal, gentle brighten.
    for y in range(16):
        for x in range(16):
            # distance to anti-diagonal (x + y == constant)
            diag = x + y
            if 10 <= diag <= 12:
                out[y][x] = shift_rgb(out[y][x], d_up // 2)
            elif diag == 11:
                out[y][x] = shift_rgb(out[y][x], d_up)
    return out


def make_polished(grid, avg):
    """Concrete + single subtle horizontal seam at row 8 (precast panel seam)."""
    d_dark = adaptive_delta(avg, -1)
    d_light = adaptive_delta(avg, +1)
    out = [[grid[y][x] for x in range(16)] for y in range(16)]
    # Seam row: slightly darker
    for x in range(16):
        out[8][x] = shift_rgb(out[8][x], d_dark)
    # Row right below seam: highlight edge (light reflecting off top of lower panel)
    for x in range(16):
        out[9][x] = shift_rgb(out[9][x], d_light // 2)
    # Row right above seam: shadow edge (underside of upper panel)
    for x in range(16):
        out[7][x] = shift_rgb(out[7][x], d_dark // 2)
    return out


def make_chiseled(grid, avg):
    """Concrete + recessed rectangular inset panel in the middle.
    Mimics architectural precast concrete with a decorative inset.
    Outer 2px keeps full base, inset rim is slightly darker, inset body slightly lighter."""
    d_dark = adaptive_delta(avg, -1)
    d_light = adaptive_delta(avg, +1)
    out = [[grid[y][x] for x in range(16)] for y in range(16)]
    # Inset rectangle rim at (2,2)-(13,13)
    rim = [(x, 2) for x in range(2, 14)] + \
          [(x, 13) for x in range(2, 14)] + \
          [(2, y) for y in range(2, 14)] + \
          [(13, y) for y in range(2, 14)]
    for x, y in rim:
        out[y][x] = shift_rgb(out[y][x], d_dark)
    # Inset body (3..12, 3..12) slightly lighter (the recessed "plate")
    for y in range(3, 13):
        for x in range(3, 13):
            out[y][x] = shift_rgb(out[y][x], d_light // 2)
    # Inner corner accents (4 tiny darker pixels at inset body corners — decorative)
    for cx, cy in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        out[cy][cx] = shift_rgb(out[cy][cx], d_dark // 2)
    # Subtle inner frame line (one pixel in from rim, softer)
    for x in range(3, 13):
        out[3][x] = shift_rgb(out[3][x], d_light // 3)
        out[12][x] = shift_rgb(out[12][x], d_dark // 3)
    return out


def make_brick(grid, avg):
    """Concrete + running-bond mortar lines. CMU-style concrete bricks.
    Layout follows vanilla deepslate_bricks: top brick spans cols 0-14 rows 0-6,
    bottom bricks cols 0-6 and 8-15 rows 8-14, with mortar at row 7, row 15,
    col 15 (top), col 7 (bottom)."""
    d_dark = adaptive_delta(avg, -1)
    d_light = adaptive_delta(avg, +1)
    # Mortar is slightly darker than concrete body
    d_mortar = int(d_dark * 1.2)
    out = [[grid[y][x] for x in range(16)] for y in range(16)]

    # Horizontal mortar rows
    for x in range(16):
        out[7][x] = shift_rgb(out[7][x], d_mortar)
        out[15][x] = shift_rgb(out[15][x], d_mortar)

    # Vertical mortar: col 15 on top half, col 7 on bottom half
    for y in range(7):
        out[y][15] = shift_rgb(out[y][15], d_mortar)
    for y in range(8, 15):
        out[y][7] = shift_rgb(out[y][7], d_mortar)

    # Subtle brick-top highlight (row right under horizontal mortar)
    # Gives bricks a sense of depth without going full stone-brick contrast
    for x in range(16):
        out[0][x] = shift_rgb(out[0][x], d_light // 2)
        out[8][x] = shift_rgb(out[8][x], d_light // 2)

    # Subtle brick-bottom shadow (row above horizontal mortar)
    for x in range(16):
        out[6][x] = shift_rgb(out[6][x], d_dark // 3)
        out[14][x] = shift_rgb(out[14][x], d_dark // 3)

    return out


GENERATORS = {
    'smooth':   make_smooth,
    'polished': make_polished,
    'chiseled': make_chiseled,
    'brick':    make_brick,
}


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
            out_grid = GENERATORS[variant](grid, avg)
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
