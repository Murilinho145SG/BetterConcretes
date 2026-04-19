"""Generate promotional images for the CurseForge page from existing textures.

Output directory: tools/promo/
  - palette_grid.png      — 4 variants × 16 colors mosaic (big hero image)
  - variant_row_<v>.png   — one row per variant (good for inline section headers)
  - color_family_<c>.png  — one column per color (4 variants stacked)
  - chisel_hero.png       — chisel item + concrete blocks around it
  - logo_banner.png       — the existing logo centered on a concrete-tile background
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
BLOCK = os.path.join(ROOT, 'src/main/resources/assets/betterconcretes/textures/block')
ITEM = os.path.join(ROOT, 'src/main/resources/assets/betterconcretes/textures/item')
LOGO = os.path.join(ROOT, 'src/main/resources/logo.png')
OUT = os.path.join(os.path.dirname(__file__), 'promo')
os.makedirs(OUT, exist_ok=True)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']
VARIANTS = ['smooth','polished','chiseled','brick']

CELL = 64  # upscale each 16x16 texture to 64x64 for web visibility
GAP = 2
BG = (28, 24, 20, 255)


def load_block(variant, color):
    return Image.open(os.path.join(BLOCK, f'{variant}_{color}_concrete.png')).convert('RGBA')


def upscale(img, size):
    return img.resize((size, size), Image.NEAREST)


def palette_grid():
    rows = len(VARIANTS)
    cols = len(COLORS)
    w = cols * CELL + (cols + 1) * GAP
    h = rows * CELL + (rows + 1) * GAP
    out = Image.new('RGBA', (w, h), BG)
    for r, variant in enumerate(VARIANTS):
        for c, color in enumerate(COLORS):
            tile = upscale(load_block(variant, color), CELL)
            x = GAP + c * (CELL + GAP)
            y = GAP + r * (CELL + GAP)
            out.paste(tile, (x, y), tile)
    out.save(os.path.join(OUT, 'palette_grid.png'))
    print(f'palette_grid.png  {w}x{h}')


def variant_rows():
    for variant in VARIANTS:
        cols = len(COLORS)
        w = cols * CELL + (cols + 1) * GAP
        h = CELL + 2 * GAP
        out = Image.new('RGBA', (w, h), BG)
        for c, color in enumerate(COLORS):
            tile = upscale(load_block(variant, color), CELL)
            out.paste(tile, (GAP + c * (CELL + GAP), GAP), tile)
        out.save(os.path.join(OUT, f'variant_row_{variant}.png'))
        print(f'variant_row_{variant}.png  {w}x{h}')


def color_families():
    # 4 specific showcase colors (eye-catching) — one vertical strip each
    SHOWCASE = ['red', 'cyan', 'yellow', 'black']
    for color in SHOWCASE:
        rows = len(VARIANTS)
        w = CELL + 2 * GAP
        h = rows * CELL + (rows + 1) * GAP
        out = Image.new('RGBA', (w, h), BG)
        for r, variant in enumerate(VARIANTS):
            tile = upscale(load_block(variant, color), CELL)
            out.paste(tile, (GAP, GAP + r * (CELL + GAP)), tile)
        out.save(os.path.join(OUT, f'color_family_{color}.png'))
        print(f'color_family_{color}.png  {w}x{h}')


def chisel_hero():
    # Chisel item (256x256 upscale) centered on a gray-concrete tiled background
    bg_tile = upscale(load_block('polished', 'light_gray'), 64)
    # 8 tiles wide x 4 tall = 512x256
    w, h = 512, 256
    out = Image.new('RGBA', (w, h), BG)
    for y in range(0, h, 64):
        for x in range(0, w, 64):
            out.paste(bg_tile, (x, y), bg_tile)
    chisel = Image.open(os.path.join(ITEM, 'chisel.png')).convert('RGBA')
    chisel_big = upscale(chisel, 192)
    cx = (w - 192) // 2
    cy = (h - 192) // 2
    # Soft darken halo under the chisel
    halo = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(halo)
    d.ellipse((cx - 20, cy + 30, cx + 192 + 20, cy + 192 + 40), fill=(0, 0, 0, 120))
    out = Image.alpha_composite(out, halo)
    out.paste(chisel_big, (cx, cy), chisel_big)
    out.save(os.path.join(OUT, 'chisel_hero.png'))
    print(f'chisel_hero.png  {w}x{h}')


def logo_banner():
    # Compose: concrete tiled background + logo centered
    logo = Image.open(LOGO).convert('RGBA')
    # Target width 1280 (good for CurseForge header), scale logo to fit with margin
    W, H = 1280, 320
    out = Image.new('RGBA', (W, H), BG)
    bg_tile = upscale(load_block('smooth', 'gray'), 64)
    for y in range(0, H, 64):
        for x in range(0, W, 64):
            out.paste(bg_tile, (x, y), bg_tile)
    # Dim the background so the logo pops
    dim = Image.new('RGBA', (W, H), (0, 0, 0, 140))
    out = Image.alpha_composite(out, dim)
    # Resize logo keeping aspect, target width 1100
    lw, lh = logo.size
    scale = 1100 / lw
    logo_r = logo.resize((1100, int(lh * scale)), Image.LANCZOS)
    lx = (W - logo_r.width) // 2
    ly = (H - logo_r.height) // 2
    out.paste(logo_r, (lx, ly), logo_r)
    out.save(os.path.join(OUT, 'logo_banner.png'))
    print(f'logo_banner.png  {W}x{H}')


def main():
    palette_grid()
    variant_rows()
    color_families()
    chisel_hero()
    logo_banner()
    print(f'\nAll images saved to {OUT}')


if __name__ == '__main__':
    main()
