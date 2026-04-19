"""Chisel item sprite v4 — vertical, real-chisel silhouette.

Anatomy (top to bottom):
  y=0-5  steel blade with flat cutting edge at top
  y=6-7  brass ferrule (wider than blade — ring collar)
  y=8-13 wooden handle
  y=14-15 pommel (rounded darker grip end)

Designed pixel-by-pixel with explicit color table for tight control.
"""
import os
from PIL import Image

OUT = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/textures/item/chisel.png'
)

# Palette
T  = (0, 0, 0, 0)
O  = (22, 18, 12, 255)       # outline (near-black)

# Steel
S_SHINE = (250, 250, 252, 255)
S_LIGHT = (208, 208, 218, 255)
S_MID   = (160, 160, 168, 255)
S_DARK  = (108, 108, 118, 255)
S_SHDW  = (70, 70, 80, 255)

# Brass
B_LIGHT = (232, 194, 100, 255)
B_MID   = (196, 150, 72, 255)
B_DARK  = (138, 98, 42, 255)

# Wood
W_HIGH  = (214, 168, 110, 255)
W_LIGHT = (178, 132, 82, 255)
W_MID   = (146, 100, 58, 255)
W_DARK  = (100, 66, 36, 255)
W_DEEP  = (62, 38, 20, 255)

CODE = {
    '.': T,
    'O': O,
    '1': S_SHINE, '2': S_LIGHT, '3': S_MID, '4': S_DARK, '5': S_SHDW,
    'A': B_LIGHT, 'B': B_MID, 'C': B_DARK,
    'h': W_HIGH, 'w': W_LIGHT, 'm': W_MID, 'd': W_DARK, 'g': W_DEEP,
}

# Centered around cols 5-10 (6 wide), ferrule extends to cols 4-11 (8 wide)
ART = [
    "......OOOO......",   # y=0 flat cutting edge top
    ".....O112O......",   # y=1 sharp edge (1=shine, 2=light)
    ".....O223O......",   # y=2 bevel
    ".....O234O......",   # y=3 shaft
    ".....O235O......",   # y=4 shaft
    ".....O235O......",   # y=5 shaft
    "....OABBBCO.....",   # y=6 ferrule top
    "....OABBCCO.....",   # y=7 ferrule bot
    ".....OhwmdO.....",   # y=8 handle top (highlight left, dark right)
    ".....OwwmmO.....",   # y=9
    ".....OwwmmO.....",   # y=10
    ".....OwmmdO.....",   # y=11
    ".....OwmddO.....",   # y=12 handle darkens
    ".....OmddgO.....",   # y=13
    "......OggO......",   # y=14 pommel narrows
    ".......OO.......",   # y=15 pommel tip
]


def main():
    img = Image.new('RGBA', (16, 16), T)
    px = img.load()
    for y, row in enumerate(ART):
        for x, ch in enumerate(row):
            px[x, y] = CODE.get(ch, T)
    img.save(OUT)
    img.resize((256, 256), Image.NEAREST).save(
        os.path.join(os.path.dirname(__file__), 'chisel_item_v4_preview.png')
    )
    print(f'Saved {OUT}')


if __name__ == '__main__':
    main()
