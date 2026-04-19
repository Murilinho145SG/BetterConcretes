"""Chipped-inspired chisel GUI texture (216x200 on a 256x256 canvas).

Layout:
  y=0..18   title bar (darker band)
  y=26..52  main row: input slot @(10,30) -> 5 cards @(34,62,90,118,146) 26x26 -> arrow @(176) -> output @(188,30)
  y=56..66  selected-variant label strip (darker band for readability)
  y=70..72  divider
  y=74      "Inventory" label area
  y=84..    player inventory 3x9 @(27, 84..), hotbar @(27, 142)
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 216, 200

# Chipped-inspired palette: warm gray with slight darkening in feature strips
BG         = (198, 198, 198, 255)
BG_DARK    = (164, 164, 164, 255)  # title bar / feature strips
BG_DEEP    = (132, 132, 132, 255)  # inventory strip slight contrast
BORDER_L   = (255, 255, 255, 255)
BORDER_D   = (85, 85, 85, 255)
EDGE_DEEP  = (55, 55, 55, 255)
SLOT_BG    = (139, 139, 139, 255)
CARD_BG    = (156, 156, 156, 255)
CARD_L     = (230, 230, 230, 255)
CARD_D     = (95, 95, 95, 255)
ARROW_D    = (70, 70, 70, 255)
ARROW_L    = (160, 160, 160, 255)
ACCENT     = (210, 180, 110, 255)  # warm accent line under title


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def draw_window_border(px):
    # Double-bevel MC window
    for x in range(GUI_W):
        px[x, 0] = BORDER_D
        px[x, GUI_H - 1] = BORDER_D
    for y in range(GUI_H):
        px[0, y] = BORDER_D
        px[GUI_W - 1, y] = BORDER_D
    for x in range(1, GUI_W - 1):
        px[x, 1] = BORDER_L
    for y in range(1, GUI_H - 1):
        px[1, y] = BORDER_L
    for x in range(1, GUI_W - 1):
        px[x, GUI_H - 2] = BORDER_D
    for y in range(1, GUI_H - 1):
        px[GUI_W - 2, y] = BORDER_D
    fr(px, 2, 2, GUI_W - 2, GUI_H - 2, BG)
    # corners clean
    px[0, 0] = BORDER_D
    px[GUI_W - 1, 0] = BORDER_D
    px[0, GUI_H - 1] = BORDER_D
    px[GUI_W - 1, GUI_H - 1] = BORDER_D


def draw_title_bar(px):
    # Darker band y=2..18 for the title
    fr(px, 2, 2, GUI_W - 2, 19, BG_DARK)
    # Bottom edge of title bar: dark line + light line + accent
    for x in range(4, GUI_W - 4):
        px[x, 19] = EDGE_DEEP
        px[x, 20] = ACCENT


def draw_label_strip(px):
    # Selected-variant label strip y=56..66
    fr(px, 4, 56, GUI_W - 4, 66, BG_DARK)
    for x in range(4, GUI_W - 4):
        px[x, 55] = EDGE_DEEP
        px[x, 66] = EDGE_DEEP


def draw_divider(px, y):
    for x in range(6, GUI_W - 6):
        px[x, y] = BORDER_D
        px[x, y + 1] = BORDER_L


def draw_slot(px, x, y):
    # classic MC slot: 18x18 frame, 16x16 interior, deep shadow border
    for i in range(18):
        px[x + i, y] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
    for i in range(18):
        px[x + i, y + 17] = BORDER_L
        px[x + 17, y + i] = BORDER_L
    px[x, y + 17] = EDGE_DEEP
    px[x + 17, y] = EDGE_DEEP
    fr(px, x + 1, y + 1, x + 17, y + 17, SLOT_BG)


def draw_card(px, x, y, size=26):
    # Raised button card
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
    # body
    fr(px, x + 2, y + 2, x + size - 2, y + size - 2, CARD_BG)


def draw_arrow(px, x, y):
    # Progress-style arrow, 10x9 at (x, y), pointing right
    # shaft
    fr(px, x, y + 3, x + 6, y + 6, ARROW_D)
    # arrowhead
    for i in range(4):
        fr(px, x + 6 + i, y + i + 1, x + 6 + i + 1, y + 8 - i, ARROW_D)
    # highlight on top-left
    fr(px, x, y + 3, x + 6, y + 4, ARROW_L)


def draw_inv_area_bg(px):
    # Subtle deeper strip behind inventory section
    fr(px, 4, 82, GUI_W - 4, GUI_H - 4, BG)
    # Left / right vertical accents
    for y in range(82, GUI_H - 4):
        px[3, y] = EDGE_DEEP
        px[GUI_W - 4, y] = EDGE_DEEP


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    draw_window_border(px)
    draw_title_bar(px)

    # Input slot
    draw_slot(px, 10, 30)

    # 5 cards 26x26 at x=34,62,90,118,146 (stride 28 = 26+2)
    for i in range(5):
        draw_card(px, 34 + i * 28, 28)

    # Arrow between cards area end (146+26=172) and output slot start (188)
    draw_arrow(px, 176, 30)

    # Output slot
    draw_slot(px, 188, 30)

    # Selected label strip
    draw_label_strip(px)

    # Divider below label strip
    draw_divider(px, 70)

    # Inventory slots
    for row in range(3):
        for col in range(9):
            draw_slot(px, 27 + col * 18, 84 + row * 18)
    for col in range(9):
        draw_slot(px, 27 + col * 18, 142)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H})')


if __name__ == '__main__':
    main()
