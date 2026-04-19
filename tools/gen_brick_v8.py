"""
Brick generator v8 — matches user's hand-made brick.png style.

Analysis of user's brick.png (dark navy-gray, lum range 29-49):
  - mortar HSL L=13.4 (flat, ~uniform)
  - body HSL L=17.5 (majority of pixels, near-uniform)
  - top highlight row HSL L=19.5 (5 L-units above body)
  - shadow/transition row just above mortar: ~3 L-units below body
  - body speckles: scattered BRIGHTER pixels (+1 to +3 L), no dark chips
  - no per-brick tone variation

Deltas translated to 0..255 scale:
  - mortar:         -26 L (L body 44 -> L mortar 34 = -10, scaled to 0..255 = -10*2.55 ≈ -26)
  - top highlight:  +13 L (body 44 -> highlight 50 = +6 scaled -> ~+15)
  - shadow row:     -10 L (body 44 -> row6 40 = -4 scaled -> ~-10)
  - speckle bright: +8 L
  - speckle dim:    -4 L (very few)

Layout (running bond):
  top brick:    cols 0-14, rows 0-6 (mortar at col 15 row 7)
  bottom-left:  cols 0-6, rows 8-14 (mortar at col 7 row 15)
  bottom-right: cols 8-15, rows 8-14
"""
import os
import sys
import random
import colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
VANILLA = os.path.join(ROOT, 'vanilla')
OUT = os.path.join(ROOT, 'preview_v8')
OUT_X128 = os.path.join(OUT, 'x128')
os.makedirs(OUT, exist_ok=True)
os.makedirs(OUT_X128, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']

# Tuned to match user reference. Values are HSL-L deltas (0..255 scale).
DELTA = {
    'mortar':       -26,
    'highlight':    +13,
    'shadow':       -10,
    'speckle_hi':    +8,
    'speckle_lo':    -5,
}

BRICKS = [
    (0, 0, 15, 7),    # top brick
    (0, 8, 7, 15),    # bottom-left
    (8, 8, 16, 15),   # bottom-right
]


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, v))


def lshift(rgb, dL):
    r, g, b = [c/255.0 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = clamp(l + dL/255.0, 0.04, 0.96)
    r2, g2, b2 = colorsys.hls_to_rgb(h, new_l, s)
    return (int(round(r2*255)), int(round(g2*255)), int(round(b2*255)))


def load_base(color):
    img = Image.open(os.path.join(VANILLA, f'{color}_concrete.png')).convert('RGB')
    px = img.load()
    return [[px[x, y] for x in range(16)] for y in range(16)]


def shift_px(grid, x, y, dL):
    if 0 <= x < 16 and 0 <= y < 16:
        grid[y][x] = lshift(grid[y][x], dL)


def make_brick(base_grid, rng):
    out = [row[:] for row in base_grid]

    # 1. Horizontal mortar rows (7 and 15)
    for x in range(16):
        shift_px(out, x, 7, DELTA['mortar'])
        shift_px(out, x, 15, DELTA['mortar'])

    # 2. Vertical mortar: col 15 on top half, col 7 on bottom half
    for y in range(7):
        shift_px(out, 15, y, DELTA['mortar'])
    for y in range(8, 15):
        shift_px(out, 7, y, DELTA['mortar'])

    # 3. Top highlight row for each brick (row 0 and row 8)
    # Row 0: cols 0-14 (col 15 is already mortar)
    for x in range(15):
        shift_px(out, x, 0, DELTA['highlight'])
    # Row 8: cols 0-6 (left brick) and cols 8-15 (right brick); col 7 is mortar
    for x in list(range(7)) + list(range(8, 16)):
        shift_px(out, x, 8, DELTA['highlight'])

    # 4. Shadow/transition row above each mortar row (rows 6 and 14)
    for x in range(15):
        shift_px(out, x, 6, DELTA['shadow'])
    for x in list(range(7)) + list(range(8, 16)):
        shift_px(out, x, 14, DELTA['shadow'])

    # 5. Body speckles: scatter BRIGHT specks in each brick interior
    # Density matches user reference: ~2-3 bright specks per brick body
    for (x0, y0, x1, y1) in BRICKS:
        # Interior = excluding top highlight row, bottom shadow row, and edge columns
        interior_x = list(range(x0, x1))
        # For brick body speckles, use rows between top+1 and bottom-1
        interior_y = list(range(y0 + 1, y1 - 1))
        cells = [(x, y) for y in interior_y for x in interior_x]
        rng.shuffle(cells)
        # 3 bright speckles
        for i in range(min(3, len(cells))):
            x, y = cells[i]
            shift_px(out, x, y, DELTA['speckle_hi'])
        # 1 dim speckle
        if len(cells) > 3:
            x, y = cells[3]
            shift_px(out, x, y, DELTA['speckle_lo'])

    return out


def grid_to_image(grid):
    img = Image.new('RGB', (16, 16))
    for y in range(16):
        for x in range(16):
            img.putpixel((x, y), grid[y][x])
    return img


def generate(colors=None):
    colors = colors or COLORS
    for color in colors:
        grid = load_base(color)
        rng = random.Random(hash((color, 'brick', 'v8')) & 0xFFFFFFFF)
        out = make_brick(grid, rng)
        img = grid_to_image(out)
        name = f'brick_{color}_concrete.png'
        img.save(os.path.join(OUT, name))
        img.resize((128, 128), Image.NEAREST).save(
            os.path.join(OUT_X128, name.replace('.png', '_x128.png'))
        )
    print(f'wrote {len(colors)} brick textures to {OUT}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        generate(args)
    else:
        generate()
