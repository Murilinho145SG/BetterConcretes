"""Compact chisel GUI (176x146, tight layout).

Fixes:
 - cards shrunk 22->20 (icon-centric, still bigger than the 18x18 slots)
 - output slot moved to x=152 with 6px right margin
 - bottom section tightened: inventory moves from y=72 to y=64
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 176, 146

BG        = (198, 198, 198, 255)
BORDER_L  = (255, 255, 255, 255)
BORDER_D  = (85, 85, 85, 255)
EDGE_DEEP = (55, 55, 55, 255)
SLOT_BG   = (139, 139, 139, 255)
CARD_BG   = (156, 156, 156, 255)
CARD_L    = (220, 220, 220, 255)
CARD_D    = (95, 95, 95, 255)
ARROW_D   = (70, 70, 70, 255)
ARROW_L   = (160, 160, 160, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def draw_vanilla_border(px):
    fr(px, 0, 0, GUI_W, GUI_H, BG)
    for i in range(GUI_W):
        px[i, 0] = BORDER_L
        px[i, GUI_H - 1] = BORDER_D
    for i in range(GUI_H):
        px[0, i] = BORDER_L
        px[GUI_W - 1, i] = BORDER_D
    px[0, GUI_H - 1] = BORDER_D
    px[GUI_W - 1, 0] = BORDER_D


def draw_slot(px, x, y):
    for i in range(18):
        px[x + i, y] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
        px[x + i, y + 17] = BORDER_L
        px[x + 17, y + i] = BORDER_L
    px[x, y + 17] = EDGE_DEEP
    px[x + 17, y] = EDGE_DEEP
    fr(px, x + 1, y + 1, x + 17, y + 17, SLOT_BG)


def draw_card(px, x, y, size=20):
    for i in range(size):
        px[x + i, y] = EDGE_DEEP
        px[x + i, y + size - 1] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
        px[x + size - 1, y + i] = EDGE_DEEP
    for i in range(1, size - 1):
        px[x + i, y + 1] = CARD_L
        px[x + 1, y + i] = CARD_L
    for i in range(2, size - 1):
        px[x + i, y + size - 2] = CARD_D
        px[x + size - 2, y + i] = CARD_D
    fr(px, x + 2, y + 2, x + size - 2, y + size - 2, CARD_BG)


def draw_arrow(px, x, y):
    # Compact arrow 10x7 at (x, y)
    fr(px, x, y + 2, x + 6, y + 5, ARROW_D)
    for i in range(3):
        fr(px, x + 6 + i, y + i, x + 6 + i + 1, y + 7 - i, ARROW_D)
    fr(px, x, y + 2, x + 6, y + 3, ARROW_L)


def draw_divider(px, y):
    for x in range(6, GUI_W - 6):
        px[x, y] = BORDER_D
        px[x, y + 1] = BORDER_L


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    draw_vanilla_border(px)

    draw_slot(px, 8, 17)

    # 5 cards 20x20 at x=30,52,74,96,118 (stride 22), y=16 to center with 18px slots at y=17
    for i in range(5):
        draw_card(px, 30 + i * 22, 16)

    # Compact arrow at x=141..151
    draw_arrow(px, 141, 20)

    # Output slot at (152, 17) — 6px margin to right edge
    draw_slot(px, 152, 17)

    # Divider between variant label area and inventory
    draw_divider(px, 50)

    # Player inventory 3x9 at (7, 64) — centered: (176-162)/2 = 7
    for row in range(3):
        for col in range(9):
            draw_slot(px, 7 + col * 18, 64 + row * 18)
    # Hotbar at (7, 122)
    for col in range(9):
        draw_slot(px, 7 + col * 18, 122)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H})')


if __name__ == '__main__':
    main()
