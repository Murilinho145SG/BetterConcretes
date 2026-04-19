"""Chipped-style chisel GUI (176x146).

Preserves the user's layout (cards y=23, slots y=24, inventory rows touching,
hotbar y=122) and applies a Chipped-inspired aesthetic:
  - slightly warm gray background (less cool, more "workshop wood" feel)
  - darker, moodier slot interiors
  - crisp 1px black shadow inside slot borders for depth
  - subtle gold accent line under title area
  - raised cards with a 2-tone bevel
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 176, 146

# Chipped-ish warmer palette
BG         = (192, 188, 180, 255)
BG_SHADE   = (174, 170, 163, 255)
BORDER_L   = (248, 245, 240, 255)
BORDER_D   = (82, 78, 72, 255)
EDGE_DEEP  = (38, 35, 30, 255)
SLOT_BG    = (100, 96, 90, 255)
SLOT_BG_LO = (80, 76, 72, 255)
CARD_BG    = (162, 156, 148, 255)
CARD_L     = (228, 222, 212, 255)
CARD_D     = (88, 82, 75, 255)
ARROW_D    = (60, 55, 48, 255)
ARROW_L    = (172, 162, 140, 255)
ACCENT     = (196, 162, 96, 255)   # muted gold
ACCENT_D   = (122, 98, 48, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def draw_window_border(px):
    fr(px, 0, 0, GUI_W, GUI_H, BG)
    for i in range(GUI_W):
        px[i, 0] = BORDER_L
        px[i, GUI_H - 1] = BORDER_D
    for i in range(GUI_H):
        px[0, i] = BORDER_L
        px[GUI_W - 1, i] = BORDER_D
    px[0, GUI_H - 1] = BORDER_D
    px[GUI_W - 1, 0] = BORDER_D


def draw_accent_line(px, y):
    """Subtle gold accent line across the content width — signature Chipped detail."""
    for x in range(6, GUI_W - 6):
        px[x, y] = ACCENT
    # Shadow underneath for depth
    for x in range(6, GUI_W - 6):
        px[x, y + 1] = ACCENT_D


def draw_slot(px, x, y):
    """Deeper slot with inner shadow — Chipped-style moodier interior."""
    # outer dark border (top + left)
    for i in range(18):
        px[x + i, y] = EDGE_DEEP
        px[x, y + i] = EDGE_DEEP
    # light border (bot + right)
    for i in range(18):
        px[x + i, y + 17] = BORDER_L
        px[x + 17, y + i] = BORDER_L
    px[x, y + 17] = EDGE_DEEP
    px[x + 17, y] = EDGE_DEEP
    # interior: 2-tone shading (darker at top, slightly lighter at bottom)
    fr(px, x + 1, y + 1, x + 17, y + 17, SLOT_BG)
    # Inner top/left dark shadow (1px) — gives depth
    for i in range(1, 17):
        px[x + i, y + 1] = SLOT_BG_LO
        px[x + 1, y + i] = SLOT_BG_LO


def draw_card(px, x, y, size=20):
    """Raised bevel card, warmer tone."""
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
    """Compact chevron arrow."""
    fr(px, x, y + 2, x + 5, y + 5, ARROW_D)
    for i in range(3):
        fr(px, x + 5 + i, y + i, x + 5 + i + 1, y + 7 - i, ARROW_D)
    # top highlight on shaft
    fr(px, x, y + 2, x + 5, y + 3, ARROW_L)


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()

    # Window chrome
    draw_window_border(px)

    # Subtle shaded band behind the chisel row (y=13..44)
    fr(px, 2, 13, GUI_W - 2, 44, BG_SHADE)

    # Gold accent line below chisel row — Chipped signature
    draw_accent_line(px, 46)

    # Input slot at (8, 24) — matching user's layout
    draw_slot(px, 8, 24)

    # 5 cards 20x20 at x=30,52,74,96,118 (stride 22), y=23
    for i in range(5):
        draw_card(px, 30 + i * 22, 23)

    # Arrow between last card (ends x=138) and output slot (x=152)
    draw_arrow(px, 140, 26)

    # Output slot at (152, 24)
    draw_slot(px, 152, 24)

    # Player inventory 3x9 at (7, 64) — rows touch (user's preference)
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
