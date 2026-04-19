"""Slim chisel GUI texture (192x166, vanilla-sized on 256x256 canvas).

Vanilla-style: single-pass 3px border, flat interior, minimal chrome.

Layout:
  y=6     title "Chisel"
  y=17    main row: input @ (8,17), 5 cards 22x22 @ x=32/56/80/104/128 y=17,
                    arrow @ 152..168, output @ (170,17)
  y=43    variant label (plain text, centered)
  y=57    thin divider
  y=63    "Inventory" label
  y=72..  inventory 3x9 @ (15, 72/90/108) + hotbar @ (15, 130)
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 192, 166

# Vanilla MC palette
BG         = (198, 198, 198, 255)
BORDER_L   = (255, 255, 255, 255)
BORDER_D   = (85, 85, 85, 255)
EDGE_DEEP  = (55, 55, 55, 255)
SLOT_BG    = (139, 139, 139, 255)
CARD_BG    = (156, 156, 156, 255)
CARD_L     = (220, 220, 220, 255)
CARD_D     = (95, 95, 95, 255)
ARROW_D    = (70, 70, 70, 255)
ARROW_L    = (160, 160, 160, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def draw_vanilla_border(px):
    """Classic MC window: 3px border (dark 1, light 1, bg 1) then flat BG interior."""
    fr(px, 0, 0, GUI_W, GUI_H, BG)
    # Top/left white highlight (inner)
    for i in range(GUI_W):
        px[i, 0] = BORDER_L
    for i in range(GUI_H):
        px[0, i] = BORDER_L
    # Bottom/right dark shadow (inner)
    for i in range(GUI_W):
        px[i, GUI_H - 1] = BORDER_D
    for i in range(GUI_H):
        px[GUI_W - 1, i] = BORDER_D
    # Corner corrections
    px[0, GUI_H - 1] = BORDER_D
    px[GUI_W - 1, 0] = BORDER_D


def draw_slot(px, x, y):
    for i in range(18):
        px[x + i, y] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
    for i in range(18):
        px[x + i, y + 17] = BORDER_L
        px[x + 17, y + i] = BORDER_L
    px[x, y + 17] = EDGE_DEEP
    px[x + 17, y] = EDGE_DEEP
    fr(px, x + 1, y + 1, x + 17, y + 17, SLOT_BG)


def draw_card(px, x, y, size=22):
    # outer 1px dark rim
    for i in range(size):
        px[x + i, y] = EDGE_DEEP
        px[x + i, y + size - 1] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
        px[x + size - 1, y + i] = EDGE_DEEP
    # inner highlight (top+left)
    for i in range(1, size - 1):
        px[x + i, y + 1] = CARD_L
        px[x + 1, y + i] = CARD_L
    # inner shadow (bot+right)
    for i in range(2, size - 1):
        px[x + i, y + size - 2] = CARD_D
        px[x + size - 2, y + i] = CARD_D
    fr(px, x + 2, y + 2, x + size - 2, y + size - 2, CARD_BG)


def draw_arrow(px, x, y):
    """16px wide arrow at (x, y), center around y+4 (8 tall)."""
    fr(px, x, y + 3, x + 10, y + 6, ARROW_D)
    for i in range(4):
        fr(px, x + 10 + i, y + i + 1, x + 10 + i + 1, y + 8 - i, ARROW_D)
    # top highlight on shaft
    fr(px, x, y + 3, x + 10, y + 4, ARROW_L)


def draw_divider(px, y):
    for x in range(6, GUI_W - 6):
        px[x, y] = BORDER_D
        px[x, y + 1] = BORDER_L


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    draw_vanilla_border(px)

    # Input slot
    draw_slot(px, 8, 17)

    # 5 cards 22x22 at x=32,56,80,104,128 (stride 24 = 22+2)
    for i in range(5):
        draw_card(px, 32 + i * 24, 17)

    # Arrow at x=152..168
    draw_arrow(px, 152, 19)

    # Output slot at (170, 17)
    draw_slot(px, 170, 17)

    # Thin divider below variant label area
    draw_divider(px, 57)

    # Player inventory 3x9 at (15, 72)
    for row in range(3):
        for col in range(9):
            draw_slot(px, 15 + col * 18, 72 + row * 18)
    # Hotbar at (15, 130)
    for col in range(9):
        draw_slot(px, 15 + col * 18, 130)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H})')


if __name__ == '__main__':
    main()
