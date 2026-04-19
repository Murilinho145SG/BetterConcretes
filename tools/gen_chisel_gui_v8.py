"""Chisel GUI v8 — vanilla Minecraft oak plank background.

Uses the actual vanilla oak_planks.png tiled as the GUI background. Slots
appear as carved dark insets. Cards have a brass rim.
"""
import os
from PIL import Image

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'src/main/resources/assets/betterconcretes/textures/gui/chisel.png')
OAK = os.path.join(HERE, 'reference_vanilla/all_blocks/oak_planks.png')

W, H = 256, 256
GUI_W, GUI_H = 176, 146

# Oak-plank-derived palette
SHADOW_DEEP   = (35, 22, 10, 255)     # deepest shadow / frame
SHADOW_MED    = (65, 45, 24, 255)     # carved interior mid
SHADOW_LIGHT  = (90, 65, 38, 255)     # carved edge soft
HL_WOOD       = (200, 162, 112, 255)  # lit wood highlight
BRASS_L       = (220, 180, 92, 255)
BRASS_D       = (148, 108, 50, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def tile_oak_bg(dst_px):
    """Fill the GUI area with tiled oak_planks."""
    oak = Image.open(OAK).convert('RGBA')
    src = oak.load()
    for y in range(GUI_H):
        for x in range(GUI_W):
            dst_px[x, y] = src[x % 16, y % 16]


def darken(rgb, amount):
    return (max(0, rgb[0] - amount), max(0, rgb[1] - amount), max(0, rgb[2] - amount), 255)


def draw_window_border(px):
    """Dark 3px wood frame: 1px void outside, 1px deep wood, 1px bevel highlight inside."""
    for i in range(GUI_W):
        px[i, 0] = SHADOW_DEEP
        px[i, GUI_H - 1] = SHADOW_DEEP
    for i in range(GUI_H):
        px[0, i] = SHADOW_DEEP
        px[GUI_W - 1, i] = SHADOW_DEEP
    # Inner dark wood (1px in)
    for i in range(1, GUI_W - 1):
        px[i, 1] = SHADOW_MED
        px[i, GUI_H - 2] = SHADOW_MED
    for i in range(1, GUI_H - 1):
        px[1, i] = SHADOW_MED
        px[GUI_W - 2, i] = SHADOW_MED
    # Bevel highlight on top+left (2px in)
    for i in range(2, GUI_W - 2):
        old = px[i, 2]
        px[i, 2] = (min(255, old[0] + 18), min(255, old[1] + 14), min(255, old[2] + 10), 255)
    for i in range(2, GUI_H - 2):
        old = px[2, i]
        px[2, i] = (min(255, old[0] + 18), min(255, old[1] + 14), min(255, old[2] + 10), 255)


def draw_carved_slot(px, x, y):
    """Dark carved-wood slot — looks like it was routed out of the plank."""
    # Outer dark border on all 4 sides
    for i in range(18):
        px[x + i, y] = SHADOW_DEEP
        px[x + i, y + 17] = SHADOW_DEEP
        px[x, y + i] = SHADOW_DEEP
        px[x + 17, y + i] = SHADOW_DEEP
    # Inner interior: deep sunken wood
    fr(px, x + 1, y + 1, x + 17, y + 17, SHADOW_MED)
    # Soft shadow just inside (top + left) for depth
    for i in range(1, 17):
        px[x + i, y + 1] = SHADOW_DEEP
        px[x + 1, y + i] = SHADOW_DEEP
    # Soft highlight on bottom + right inside for carve depth
    for i in range(2, 17):
        px[x + i, y + 16] = SHADOW_LIGHT
        px[x + 16, y + i] = SHADOW_LIGHT


def draw_brass_card(px, x, y, size=20):
    """Brass-rimmed button sitting on the wood — raised inlay look."""
    # Outer brass-dark rim
    for i in range(size):
        px[x + i, y] = BRASS_D
        px[x + i, y + size - 1] = BRASS_D
        px[x, y + i] = BRASS_D
        px[x + size - 1, y + i] = BRASS_D
    # Inner brass highlight on top+left
    for i in range(1, size - 1):
        px[x + i, y + 1] = BRASS_L
        px[x + 1, y + i] = BRASS_L
    # Inner brass shadow on bot+right
    for i in range(2, size - 1):
        px[x + i, y + size - 2] = BRASS_D
        px[x + size - 2, y + i] = BRASS_D
    # Body: the wood showing through (lighter oak tone)
    fr(px, x + 2, y + 2, x + size - 2, y + size - 2, (178, 142, 92, 255))


def draw_arrow(px, x, y):
    """Compact brass chevron."""
    fr(px, x, y + 2, x + 5, y + 5, SHADOW_DEEP)
    for i in range(3):
        fr(px, x + 5 + i, y + i, x + 5 + i + 1, y + 7 - i, SHADOW_DEEP)
    fr(px, x, y + 2, x + 5, y + 3, BRASS_L)


def draw_brass_inlay(px, y):
    """Thin brass strip decoration."""
    for x in range(4, GUI_W - 4):
        px[x, y] = BRASS_L
        px[x, y + 1] = BRASS_D


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    # 1) Tile vanilla oak planks as BG
    tile_oak_bg(px)

    # 2) Window chrome (dark wood frame)
    draw_window_border(px)

    # 3) Brass inlay line between chisel row and inventory (y=46)
    draw_brass_inlay(px, 46)

    # 4) Carved slots
    draw_carved_slot(px, 8, 24)
    draw_carved_slot(px, 152, 24)

    # 5) Brass cards (5 variants)
    for i in range(5):
        draw_brass_card(px, 30 + i * 22, 23)

    # 6) Arrow between cards end (x=138) and output slot (x=152)
    draw_arrow(px, 140, 26)

    # 7) Inventory 3x9 @ (7, 64) rows touching
    for row in range(3):
        for col in range(9):
            draw_carved_slot(px, 7 + col * 18, 64 + row * 18)
    # 8) Hotbar @ (7, 122)
    for col in range(9):
        draw_carved_slot(px, 7 + col * 18, 122)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H}) — vanilla oak planks style')


if __name__ == '__main__':
    main()
