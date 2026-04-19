"""Generate the chisel GUI texture (176x166 inside 256x256 canvas)."""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src', 'main', 'resources', 'assets', 'betterconcretes', 'textures', 'gui', 'chisel.png'
)

W, H = 176, 166

# Vanilla container palette (matches Minecraft's inventory/chest look)
BG_LIGHT    = (208, 208, 208, 255)
BG_BASE     = (198, 198, 198, 255)
BG_SHADOW   = (170, 170, 170, 255)
BORDER_DARK = ( 55,  55,  55, 255)
BORDER_MID  = (109, 109, 109, 255)
BORDER_HI   = (255, 255, 255, 255)
SLOT_DARK   = ( 55,  55,  55, 255)
SLOT_MID    = (139, 139, 139, 255)
SLOT_LIGHT  = (255, 255, 255, 255)
BUTTON_BG   = (172, 172, 172, 255)
ARROW_DIM   = ( 90,  90,  90, 255)
ARROW_MID   = (140, 140, 140, 255)
ACCENT      = (120,  80,  30, 255)   # chisel handle color for decorative stripe

img = Image.new('RGBA', (W, H), BG_BASE)
d = ImageDraw.Draw(img)
px = img.load()

# --- Subtle top-to-bottom gradient for organic feel ---
for y in range(H):
    t = y / (H - 1)
    # Brighten near top, slight darken at bottom
    brightness = 1.06 - t * 0.10
    for x in range(W):
        r, g, b, a = px[x, y]
        px[x, y] = (
            min(255, int(r * brightness)),
            min(255, int(g * brightness)),
            min(255, int(b * brightness)),
            a
        )

# --- Outer frame (vanilla-style 4-layer bevel) ---
# Layer 1: outermost dark outline
d.rectangle([0, 0, W-1, H-1], outline=BORDER_DARK)
# Layer 2: light bevel (top + left), mid bevel (bottom + right)
d.line([(1, 1), (W-2, 1)], fill=BORDER_HI)
d.line([(1, 1), (1, H-2)], fill=BORDER_HI)
d.line([(1, H-2), (W-2, H-2)], fill=BORDER_MID)
d.line([(W-2, 1), (W-2, H-2)], fill=BORDER_MID)
# Layer 3: inner subtle bright line (just top+left)
d.line([(2, 2), (W-3, 2)], fill=(228, 228, 228, 255))
d.line([(2, 2), (2, H-3)], fill=(228, 228, 228, 255))

# --- Helper: recessed slot (vanilla inventory style) ---
def draw_slot(x, y, size=18):
    # Dark inset outline (top + left darker, bot + right brighter — inset look)
    d.line([(x, y), (x+size-1, y)], fill=SLOT_DARK)           # top
    d.line([(x, y), (x, y+size-1)], fill=SLOT_DARK)           # left
    d.line([(x+1, y+size-1), (x+size-1, y+size-1)], fill=SLOT_LIGHT)  # bottom
    d.line([(x+size-1, y+1), (x+size-1, y+size-1)], fill=SLOT_LIGHT)  # right
    # Inner fill
    d.rectangle([x+1, y+1, x+size-2, y+size-2], fill=SLOT_MID)

# --- Helper: raised button (opposite bevel) ---
def draw_button(x, y, size=18):
    # Raised: top+left bright, bot+right dark
    d.rectangle([x, y, x+size-1, y+size-1], fill=BUTTON_BG)
    d.line([(x, y), (x+size-1, y)], fill=BORDER_HI)
    d.line([(x, y), (x, y+size-1)], fill=BORDER_HI)
    d.line([(x+1, y+size-1), (x+size-1, y+size-1)], fill=BORDER_DARK)
    d.line([(x+size-1, y+1), (x+size-1, y+size-1)], fill=BORDER_DARK)

# --- Title separator (decorative stripe under title) ---
# A thin 1-2px darker line around y=15 for title delineation
for x in range(6, W - 6):
    r, g, b, _ = px[x, 15]
    px[x, 15] = (int(r * 0.85), int(g * 0.85), int(b * 0.85), 255)

# --- Input & output slots ---
# Slot screen-space (20, 33) => texture top-left (19, 32)
draw_slot(19, 32)
draw_slot(142, 32)

# --- 5 variant buttons (18x18, gap 4, starting at x=38, y=30) ---
for i in range(5):
    bx = 38 + i * 22
    by = 30
    draw_button(bx, by)

# --- Decorative "▶" arrow between input slot and buttons, and buttons and output ---
# Arrow 1: from slot (37) to button start (37 is right edge of input). Very narrow space — skip.
# Instead, a vertical separator between buttons row and slots.
# Better: underline below variant buttons showing progression.
# Horizontal faint line at y=51 below buttons connecting slots visually
for x in range(38, 38 + 5*22 - 4):
    r, g, b, _ = px[x, 51]
    px[x, 51] = (int(r * 0.88), int(g * 0.88), int(b * 0.88), 255)

# --- Title region decorative chisel stripe (left of title text) ---
# Just a tiny 3px colored accent mark at top-left under the border
for dy in range(3):
    for dx in range(3):
        px[5 + dx, 5 + dy] = ACCENT

# --- Player inventory (3x9) @ screen y=84..138 => tex y=83..137 ---
for row in range(3):
    for col in range(9):
        draw_slot(7 + col * 18, 83 + row * 18)
# Hotbar @ screen y=142 => tex y=141
for col in range(9):
    draw_slot(7 + col * 18, 141)

# Divider between inventory area and top region (vanilla-style at y=82)
for x in range(3, W - 3):
    r, g, b, _ = px[x, 82]
    px[x, 82] = (int(r * 0.78), int(g * 0.78), int(b * 0.78), 255)

# --- Save into a 256x256 canvas (power-of-2 for texture atlas) ---
canvas = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
canvas.paste(img, (0, 0))

# Make sure parent dir exists
os.makedirs(os.path.dirname(OUT), exist_ok=True)
canvas.save(OUT)
print(f'Saved {OUT}')
