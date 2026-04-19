"""Wooden workbench chisel GUI (176x146).

Horizontal wood planks with grain, knots, and seams. Slots look carved/routed
into the wood. Cards look like brass-rimmed buttons set on top.
"""
import os
import random
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/gui/chisel.png'
)

W, H = 256, 256
GUI_W, GUI_H = 176, 146

# Wood palette
WOOD_HL    = (200, 162, 112, 255)   # knot-bright / grain highlight
WOOD_L     = (172, 134, 88, 255)    # plank surface light tone
WOOD_BASE  = (148, 110, 68, 255)    # plank surface mid tone
WOOD_D     = (118, 85, 50, 255)     # plank surface dark tone
WOOD_DEEP  = (82, 55, 30, 255)      # grain lines, plank seams
WOOD_SHDW  = (50, 32, 18, 255)      # slot carved interior
WOOD_VOID  = (32, 20, 12, 255)      # deepest shadow / borders

# Brass-inlay accent
BRASS_L    = (218, 178, 92, 255)
BRASS_D    = (150, 110, 50, 255)


def fr(px, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = c


def plank_color_at(rng, base_tone):
    """Sample a wood-grain color with small random variation around base_tone."""
    r, g, b, a = base_tone
    j = rng.randint(-6, 6)
    return (max(0, min(255, r + j)), max(0, min(255, g + j)), max(0, min(255, b + j - 2)), a)


def draw_plank(px, y0, y1, base_tone, rng):
    """Fill a horizontal plank with grain. base_tone = avg surface color."""
    for y in range(y0, y1):
        # Row-level brightness variation (smooth vertical grain)
        row_j = rng.randint(-4, 4)
        for x in range(GUI_W):
            # Per-pixel fine grain variation
            c = plank_color_at(rng, base_tone)
            px[x, y] = (
                max(0, min(255, c[0] + row_j)),
                max(0, min(255, c[1] + row_j)),
                max(0, min(255, c[2] + row_j)),
                255,
            )
    # Occasional horizontal grain streaks (darker 1-row strokes spanning several px)
    for _ in range(rng.randint(3, 6)):
        sy = rng.randrange(y0, y1)
        sx = rng.randrange(0, GUI_W - 20)
        length = rng.randint(10, GUI_W - sx - 2)
        for x in range(sx, sx + length):
            r, g, b, _ = px[x, sy]
            px[x, sy] = (max(0, r - 15), max(0, g - 12), max(0, b - 8), 255)


def draw_plank_seam(px, y):
    """Dark horizontal seam between two planks (2px)."""
    for x in range(GUI_W):
        px[x, y] = WOOD_VOID
        px[x, y + 1] = WOOD_DEEP


def draw_knot(px, cx, cy, rng):
    """Small oval knot in the wood — darker center ring."""
    for dy in range(-2, 3):
        for dx in range(-3, 4):
            if dx * dx // 2 + dy * dy <= 4:
                x, y = cx + dx, cy + dy
                if 1 < x < GUI_W - 1 and 1 < y < GUI_H - 1:
                    d = abs(dx) + abs(dy)
                    if d <= 1:
                        px[x, y] = WOOD_SHDW
                    elif d <= 2:
                        px[x, y] = WOOD_DEEP
                    else:
                        r, g, b, _ = px[x, y]
                        px[x, y] = (max(0, r - 20), max(0, g - 18), max(0, b - 15), 255)


def draw_window_border(px):
    """Dark wood frame around the whole GUI."""
    for i in range(GUI_W):
        px[i, 0] = WOOD_VOID
        px[i, 1] = WOOD_DEEP
        px[i, GUI_H - 1] = WOOD_VOID
        px[i, GUI_H - 2] = WOOD_DEEP
    for i in range(GUI_H):
        px[0, i] = WOOD_VOID
        px[1, i] = WOOD_DEEP
        px[GUI_W - 1, i] = WOOD_VOID
        px[GUI_W - 2, i] = WOOD_DEEP
    # Bevel highlight on inner top/left (catches light)
    for i in range(2, GUI_W - 2):
        r, g, b, _ = px[i, 2]
        px[i, 2] = (min(255, r + 20), min(255, g + 15), min(255, b + 10), 255)
    for i in range(2, GUI_H - 2):
        r, g, b, _ = px[2, i]
        px[2, i] = (min(255, r + 20), min(255, g + 15), min(255, b + 10), 255)


def draw_carved_slot(px, x, y):
    """Slot that looks carved into the wood — dark sunken interior."""
    # Outer top/left deep shadow (carved edge shadow)
    for i in range(18):
        px[x + i, y] = WOOD_VOID
        px[x, y + i] = WOOD_VOID
    # Bot/right bevel highlight (light catches the far edge of the carve)
    for i in range(18):
        r, g, b, _ = px[x + i, y + 17]
        px[x + i, y + 17] = (min(255, r + 30), min(255, g + 22), min(255, b + 14), 255)
        r, g, b, _ = px[x + 17, y + i]
        px[x + 17, y + i] = (min(255, r + 30), min(255, g + 22), min(255, b + 14), 255)
    px[x, y + 17] = WOOD_VOID
    px[x + 17, y] = WOOD_VOID
    # Interior: dark sunken wood
    fr(px, x + 1, y + 1, x + 17, y + 17, WOOD_SHDW)
    # Inner top-left darker shadow (the deepest part of the carve)
    for i in range(1, 17):
        px[x + i, y + 1] = WOOD_VOID
        px[x + 1, y + i] = WOOD_VOID


def draw_brass_card(px, x, y, size=20):
    """Raised card with brass rim — like a decorative button inlaid on wood."""
    # Outer brass dark rim
    for i in range(size):
        px[x + i, y] = BRASS_D
        px[x + i, y + size - 1] = BRASS_D
        px[x, y + i] = BRASS_D
        px[x + size - 1, y + i] = BRASS_D
    # Inner brass highlight
    for i in range(1, size - 1):
        px[x + i, y + 1] = BRASS_L
        px[x + 1, y + i] = BRASS_L
    # Inner brass shadow on bot/right
    for i in range(2, size - 1):
        px[x + i, y + size - 2] = BRASS_D
        px[x + size - 2, y + i] = BRASS_D
    # Card body — slightly lighter than the surrounding wood
    fr(px, x + 2, y + 2, x + size - 2, y + size - 2, WOOD_L)


def draw_arrow(px, x, y):
    """Compact chevron — brass-colored."""
    fr(px, x, y + 2, x + 5, y + 5, WOOD_VOID)
    for i in range(3):
        fr(px, x + 5 + i, y + i, x + 5 + i + 1, y + 7 - i, WOOD_VOID)
    # Brass highlight on shaft
    fr(px, x, y + 2, x + 5, y + 3, BRASS_L)


def draw_brass_inlay(px, y):
    """Thin brass inlay line across the GUI interior width."""
    for x in range(4, GUI_W - 4):
        px[x, y] = BRASS_L
        px[x, y + 1] = BRASS_D


def main():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = img.load()
    rng = random.Random(0xC015E1)  # deterministic

    # Fill BG with a base wood tone first
    fr(px, 0, 0, GUI_W, GUI_H, WOOD_BASE)

    # --- Draw 3 horizontal planks ---
    # Plank 1: y=0..49
    draw_plank(px, 0, 49, WOOD_BASE, rng)
    draw_plank_seam(px, 49)
    # Plank 2: y=51..97 (top of inventory area)
    draw_plank(px, 51, 97, WOOD_L, rng)
    draw_plank_seam(px, 97)
    # Plank 3: y=99..GUI_H
    draw_plank(px, 99, GUI_H, WOOD_BASE, rng)

    # Scatter a couple of knots
    draw_knot(px, 22, 40, rng)
    draw_knot(px, 138, 55, rng)
    draw_knot(px, 90, 108, rng)

    # --- Window border (dark wood frame) ---
    draw_window_border(px)

    # --- Brass inlay accent line right below chisel row ---
    draw_brass_inlay(px, 45)

    # --- Carved slots ---
    draw_carved_slot(px, 8, 24)     # input
    draw_carved_slot(px, 152, 24)   # output

    # --- 5 brass cards @ x=30,52,74,96,118, y=23 ---
    for i in range(5):
        draw_brass_card(px, 30 + i * 22, 23)

    # --- Arrow ---
    draw_arrow(px, 140, 26)

    # --- Inventory 3x9 at (7, 64) — rows touch ---
    for row in range(3):
        for col in range(9):
            draw_carved_slot(px, 7 + col * 18, 64 + row * 18)
    # Hotbar at (7, 122)
    for col in range(9):
        draw_carved_slot(px, 7 + col * 18, 122)

    img.save(OUT)
    print(f'wrote {OUT} ({GUI_W}x{GUI_H}) — wooden workbench style')


if __name__ == '__main__':
    main()
