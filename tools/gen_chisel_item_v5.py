"""Chisel item v5 — inspired by Chipped's diagonal chisel sprite.

Key design borrowings from Chipped:
  - Diagonal orientation (wood bottom-left -> metal top-right)
  - Flat cutting edge at tip (2-3 bright pixels perpendicular to the blade axis)
  - Non-black outlines: metal uses dark-gray (68), wood uses deep-brown (40)
  - 4-tone gradient per material

Our own twist:
  - Brass ferrule (2 rows) at the wood/metal transition — ties to the GUI brass accent
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/item/chisel.png'
)

# Palette (Chipped-inspired)
T  = (0, 0, 0, 0)

# Metal (4 tones + shine)
MO = (68, 68, 72, 255)      # metal outline
MM = (150, 150, 158, 255)   # metal mid
ML = (193, 193, 200, 255)   # metal light
MS = (255, 255, 255, 255)   # shine

# Brass (3 tones) — subtle ferrule
BD = (140, 100, 48, 255)
BB = (198, 154, 80, 255)
BL = (232, 192, 100, 255)

# Wood (4 tones)
WO = (40, 26, 14, 255)      # wood outline / deep
WD = (73, 48, 22, 255)
WM = (104, 70, 34, 255)
WL = (137, 96, 52, 255)

CODE = {
    '.': T,
    'o': MO, 'm': MM, 'l': ML, 's': MS,
    'd': BD, 'b': BB, 'r': BL,
    'q': WO, 'u': WD, 'w': WM, 'h': WL,
}

# 16x16 grid. Diagonal tool; cols grow ~1 per row moving up-right.
ART = [
    "................",   # y=0
    "..............oo",   # y=1  tip outline
    ".............osm",   # y=2  cutting edge (s=shine)
    "............oslo",   # y=3
    "...........oslmo",   # y=4
    "..........oslmo.",   # y=5  blade
    ".........ommlmo.",   # y=6
    "........ommlo...",   # y=7
    ".......odbbo....",   # y=8  brass ferrule
    "......odbro.....",   # y=9  brass
    ".....oqhwuo.....",   # y=10 handle transition
    "....oqhwuo......",   # y=11
    "...oqhwuo.......",   # y=12
    "..oqwwuo........",   # y=13
    ".oquuo..........",   # y=14
    "oquo............",   # y=15 pommel
]


def main():
    img = Image.new('RGBA', (16, 16), T)
    px = img.load()
    for y, row in enumerate(ART):
        for x, ch in enumerate(row):
            px[x, y] = CODE.get(ch, T)
    img.save(OUT)
    img.resize((256, 256), Image.NEAREST).save(
        os.path.join(os.path.dirname(__file__), 'chisel_item_v5_preview.png')
    )
    print(f'Saved {OUT}')


if __name__ == '__main__':
    main()
