"""Generate the chisel GUI background texture (200x186 on a 256x256 canvas).

Layout:
  Title: y=6
  Main row at y=25:
    - input slot @ (8, 25)
    - 5 variant cards @ x=30,54,78,102,126 (22x22, gap 2)
    - arrow chevron @ x=152..168
    - output slot @ (172, 25)
  Variant label: y=52 centered
  Inventory label: y=73
  Player inventory: starts (19, 84), rows y=84/102/120
  Hotbar: y=142
"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 200, 186

# Vanilla MC GUI palette
BG = (198, 198, 198, 255)
BORDER_LIGHT = (255, 255, 255, 255)
BORDER_DARK = (85, 85, 85, 255)
SLOT_BG = (139, 139, 139, 255)
SLOT_SHADOW = (55, 55, 55, 255)
TITLE_DARK = (64, 64, 64, 255)
CARD_BG = (156, 156, 156, 255)
CARD_EDGE_DARK = (85, 85, 85, 255)
CARD_EDGE_LIGHT = (220, 220, 220, 255)
ARROW_DARK = (80, 80, 80, 255)
ARROW_LIGHT = (140, 140, 140, 255)


def fill_rect(px, x0, y0, x1, y1, color):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = color


def draw_slot(px, x, y):
    """Standard MC inventory slot (18x18 outer, 16x16 inner at x+1,y+1)."""
    # top + left dark border
    for i in range(18):
        px[x + i, y] = SLOT_SHADOW
        px[x, y + i] = SLOT_SHADOW
    # bot + right light border
    for i in range(18):
        px[x + i, y + 17] = BORDER_LIGHT
        px[x + 17, y + i] = BORDER_LIGHT
    # bottom-left and top-right corners are transitions
    px[x, y + 17] = SLOT_SHADOW
    px[x + 17, y] = SLOT_SHADOW
    # 16x16 slot interior
    fill_rect(px, x + 1, y + 1, x + 17, y + 17, SLOT_BG)


def draw_card(px, x, y, w=22, h=22):
    """Variant card: beveled button, item icon sits inside at +3,+3 (16x16 icon)."""
    # outer rim dark
    for i in range(w):
        px[x + i, y] = CARD_EDGE_DARK
        px[x + i, y + h - 1] = CARD_EDGE_DARK
    for i in range(h):
        px[x, y + i] = CARD_EDGE_DARK
        px[x + w - 1, y + i] = CARD_EDGE_DARK
    # inner highlight rim (raised button effect)
    for i in range(1, w - 1):
        px[x + i, y + 1] = CARD_EDGE_LIGHT
    for i in range(1, h - 1):
        px[x + 1, y + i] = CARD_EDGE_LIGHT
    # inner shadow rim (bottom-right)
    for i in range(2, w - 1):
        px[x + i, y + h - 2] = CARD_EDGE_DARK
    for i in range(2, h - 1):
        px[x + w - 2, y + i] = CARD_EDGE_DARK
    # card body
    fill_rect(px, x + 2, y + 2, x + w - 2, y + h - 2, CARD_BG)


def draw_arrow(px, x, y):
    """Progress-style arrow pointing right, roughly 16x10 in the 152-168 area."""
    # Arrow body (horizontal bar)
    fill_rect(px, x, y, x + 10, y + 4, ARROW_DARK)
    # Arrowhead triangle
    for i in range(5):
        fill_rect(px, x + 10, y - i, x + 10 + (5 - i), y - i + 1, ARROW_DARK)
        fill_rect(px, x + 10, y + 4 + i, x + 10 + (5 - i), y + 4 + i + 1, ARROW_DARK)
    # 1px highlight on top edge
    fill_rect(px, x, y, x + 10, y + 1, ARROW_LIGHT)


def draw_window_border(px):
    """Main GUI rectangle at (0,0)-(GUI_W, GUI_H) with the classic MC 4px border."""
    # Outer border dark
    for x in range(GUI_W):
        px[x, 0] = BORDER_DARK
        px[x, GUI_H - 1] = BORDER_DARK
    for y in range(GUI_H):
        px[0, y] = BORDER_DARK
        px[GUI_W - 1, y] = BORDER_DARK
    # Inner border light (1px inside)
    for x in range(1, GUI_W - 1):
        px[x, 1] = BORDER_LIGHT
        px[x, GUI_H - 2] = BORDER_DARK
    for y in range(1, GUI_H - 1):
        px[1, y] = BORDER_LIGHT
        px[GUI_W - 2, y] = BORDER_DARK
    # Second-level highlight (classic double-bevel look)
    for x in range(2, GUI_W - 2):
        px[x, 2] = BG
    for y in range(2, GUI_H - 2):
        px[2, y] = BG
    # Fill interior
    fill_rect(px, 3, 3, GUI_W - 3, GUI_H - 3, BG)
    # Re-corner the borders cleanly
    px[0, 0] = BORDER_DARK
    px[GUI_W - 1, 0] = BORDER_DARK
    px[0, GUI_H - 1] = BORDER_DARK
    px[GUI_W - 1, GUI_H - 1] = BORDER_DARK


def draw_divider(px, y):
    """Thin horizontal separator across the inside width."""
    for x in range(7, GUI_W - 7):
        px[x, y] = BORDER_DARK
        px[x, y + 1] = BORDER_LIGHT


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    # ---- Window chrome
    draw_window_border(px)

    # ---- Input slot @ (8, 25)
    draw_slot(px, 8, 25)

    # ---- Variant cards @ 30,54,78,102,126 (22x22 each, gap 2)
    for i in range(5):
        draw_card(px, 30 + i * 24, 25)

    # ---- Arrow @ 152..168, centered vertically around y=32 (8 tall)
    draw_arrow(px, 152, 32)

    # ---- Output slot @ (172, 25)
    draw_slot(px, 172, 25)

    # ---- Divider above inventory section (y=72)
    draw_divider(px, 72)

    # ---- Player inventory 3x9 @ start (19, 84), each 18x18
    for row in range(3):
        for col in range(9):
            draw_slot(px, 19 + col * 18, 84 + row * 18)
    # ---- Hotbar 1x9 @ y=142
    for col in range(9):
        draw_slot(px, 19 + col * 18, 142)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H} on {W}x{H})')


if __name__ == '__main__':
    main()
