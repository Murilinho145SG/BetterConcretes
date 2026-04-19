"""Generate the JEI chisel category background texture (100x30 with carved slots).

Output: assets/betterconcretes/textures/gui/jei/chisel_category.png
Layout: input slot @ (0, 6) -> arrow @ (28, 10) -> output slot @ (76, 6)
Uses the same oak-plank + brass aesthetic as the chisel GUI.
"""
import os
from PIL import Image

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, '..', 'src/main/resources/assets/betterconcretes/textures/gui/jei')
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, 'chisel_category.png')
OAK = os.path.join(HERE, 'reference_vanilla/all_blocks/oak_planks.png')

CAT_W, CAT_H = 100, 30

SHADOW_DEEP   = (35, 22, 10, 255)
SHADOW_MED    = (65, 45, 24, 255)
SHADOW_LIGHT  = (90, 65, 38, 255)
BRASS_L       = (220, 180, 92, 255)
BRASS_D       = (148, 108, 50, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def tile_oak(dst_px):
    oak = Image.open(OAK).convert('RGBA')
    src = oak.load()
    for y in range(CAT_H):
        for x in range(CAT_W):
            dst_px[x, y] = src[x % 16, y % 16]


def draw_carved_slot(px, x, y):
    for i in range(18):
        px[x + i, y] = SHADOW_DEEP
        px[x + i, y + 17] = SHADOW_DEEP
        px[x, y + i] = SHADOW_DEEP
        px[x + 17, y + i] = SHADOW_DEEP
    fr(px, x + 1, y + 1, x + 17, y + 17, SHADOW_MED)
    for i in range(1, 17):
        px[x + i, y + 1] = SHADOW_DEEP
        px[x + 1, y + i] = SHADOW_DEEP
    for i in range(2, 17):
        px[x + i, y + 16] = SHADOW_LIGHT
        px[x + 16, y + i] = SHADOW_LIGHT


def draw_arrow(px, x, y):
    # 16-wide brass arrow pointing right
    fr(px, x, y + 3, x + 11, y + 6, SHADOW_DEEP)
    for i in range(4):
        fr(px, x + 11 + i, y + i + 1, x + 11 + i + 1, y + 8 - i, SHADOW_DEEP)
    fr(px, x, y + 3, x + 11, y + 4, BRASS_L)


def main():
    img = Image.new('RGBA', (CAT_W, CAT_H), (0, 0, 0, 0))
    px = img.load()

    tile_oak(px)

    # Input slot at (0, 6)
    draw_carved_slot(px, 0, 6)
    # Arrow at (24, 9) -- 16 wide
    draw_arrow(px, 24, 9)
    # Output slot at (82, 6)
    draw_carved_slot(px, 82, 6)

    img.save(OUT)
    print(f'wrote {OUT} ({CAT_W}x{CAT_H})')


if __name__ == '__main__':
    main()
