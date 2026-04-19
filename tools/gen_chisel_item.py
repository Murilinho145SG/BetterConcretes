"""Chisel item sprite — 16x16 diagonal.

v3 refinements over the prior pass:
  - brass ferrule (matches the GUI's brass accents) instead of a plain metal collar
  - longer wooden handle with a visible grain streak
  - clearer beveled cutting edge at the tip
  - crisp 1px dark outline around the whole silhouette for readability at 16px
"""
from PIL import Image
import os

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src', 'main', 'resources', 'assets', 'betterconcretes', 'textures', 'item', 'chisel.png'
)

W = H = 16
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
px = img.load()

# Outline
OUT_DARK = (28, 22, 14, 255)

# Wood palette (5 tones)
W_DEEP  = (60, 38, 18, 255)
W_DARK  = (100, 66, 34, 255)
W_BASE  = (148, 102, 60, 255)
W_LIGHT = (188, 142, 92, 255)
W_HIGH  = (218, 172, 118, 255)

# Brass palette (ferrule)
B_DARK  = (130, 92, 40, 255)
B_BASE  = (192, 148, 68, 255)
B_LIGHT = (232, 192, 100, 255)

# Metal palette (5 tones)
M_DEEP  = (50, 50, 58, 255)
M_DARK  = (92, 92, 100, 255)
M_BASE  = (150, 150, 160, 255)
M_LIGHT = (208, 208, 218, 255)
M_SHINE = (248, 248, 252, 255)


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c


# ===== HANDLE (wood, bottom-left half) =====
# Outer silhouette outline (walked along both sides of the diagonal)
handle_outline_back = [  # bottom-right side (shadow side)
    (1, 15), (2, 15), (3, 15),
    (4, 14), (5, 13), (6, 12), (7, 11), (8, 10),
]
handle_outline_front = [  # top-left side (light side)
    (0, 14), (0, 13), (1, 12), (2, 11), (3, 10), (4, 9), (5, 8),
]
# Wood body layers (from dark to light, top-left to bottom-right)
handle_dark = [
    (1, 14), (2, 13), (3, 12), (4, 11), (5, 10), (6, 9),
]
handle_base = [
    (2, 14), (3, 13), (4, 12), (5, 11), (6, 10), (7, 9),
]
handle_light = [
    (3, 14), (4, 13), (5, 12), (6, 11), (7, 10),
]
# Wood grain highlight streak (single-pixel shiny line)
handle_grain = [
    (4, 14), (5, 13), (6, 12),
]
# Pommel (butt end, darkest)
pommel = [(0, 15)]

for p in handle_outline_back: put(*p, OUT_DARK)
for p in handle_outline_front: put(*p, OUT_DARK)
for p in handle_dark: put(*p, W_DARK)
for p in handle_base: put(*p, W_BASE)
for p in handle_light: put(*p, W_LIGHT)
for p in handle_grain: put(*p, W_HIGH)
for p in pommel: put(*p, W_DEEP)

# ===== BRASS FERRULE (collar between handle and blade) =====
# 2-row brass band at the diagonal transition
ferrule_back = [(6, 10), (7, 9), (8, 8)]      # outline (shadow side)  — overwrites wood
ferrule_front = [(5, 9), (6, 8), (7, 7)]       # outline (light side)
ferrule_dark = [(6, 9), (7, 8), (8, 7)]        # dark band
ferrule_mid = [(7, 9), (8, 8), (9, 7)]         # mid band
ferrule_light = [(8, 9), (9, 8)]               # highlight spot

for p in ferrule_back: put(*p, OUT_DARK)
for p in ferrule_front: put(*p, OUT_DARK)
for p in ferrule_dark: put(*p, B_DARK)
for p in ferrule_mid: put(*p, B_BASE)
for p in ferrule_light: put(*p, B_LIGHT)

# ===== METAL SHAFT (diagonal blade) =====
# Outer outline both sides
blade_outline_back = [(9, 8), (10, 7), (11, 6), (12, 5), (13, 4)]
blade_outline_front = [(7, 6), (8, 5), (9, 4), (10, 3), (11, 2), (12, 1)]

# Core metal (dark to light bands)
blade_dark = [(8, 7), (9, 6), (10, 5), (11, 4), (12, 3), (13, 2)]
blade_base = [(9, 7), (10, 6), (11, 5), (12, 4), (13, 3)]
blade_light = [(10, 7), (11, 6), (12, 5)]

for p in blade_outline_back: put(*p, OUT_DARK)
for p in blade_outline_front: put(*p, OUT_DARK)
for p in blade_dark: put(*p, M_DARK)
for p in blade_base: put(*p, M_BASE)
for p in blade_light: put(*p, M_LIGHT)

# ===== CUTTING TIP (top-right beveled edge) =====
# The tip is angled — 2-3px beveled cutting edge that catches the light
put(13, 1, OUT_DARK)   # top edge outline
put(14, 1, OUT_DARK)
put(14, 0, OUT_DARK)
put(15, 1, OUT_DARK)
# Bright cutting edge
put(13, 0, M_SHINE)     # sharpest bit
# Bevel body
put(14, 2, M_BASE)
put(15, 2, OUT_DARK)

# A tiny sparkle on the shaft
put(12, 5, M_SHINE)

img.save(OUT)
img.resize((256, 256), Image.NEAREST).save(
    os.path.join(os.path.dirname(__file__), 'chisel_item_v3_preview.png')
)
print(f'Saved {OUT}')
