"""Regenerate 96 CTM textures from current smooth_{color}_concrete base."""
from PIL import Image
import os

BASE = os.path.join(
    os.path.dirname(__file__), '..',
    'src', 'main', 'resources', 'assets', 'betterconcretes', 'textures', 'block'
)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']

PATTERN_EDGES = {0:0b0000, 1:0b0010, 2:0b0011, 3:0b0101, 4:0b0111, 5:0b1111}

def darker(px, factor=0.55):
    r, g, b, a = px
    return (int(r*factor), int(g*factor), int(b*factor), a)

def draw_edges(img, edges):
    w, h = img.size
    px = img.load()
    if edges & 0b1000:
        for x in range(w): px[x, 0] = darker(px[x, 0])
    if edges & 0b0100:
        for y in range(h): px[w-1, y] = darker(px[w-1, y])
    if edges & 0b0010:
        for x in range(w): px[x, h-1] = darker(px[x, h-1])
    if edges & 0b0001:
        for y in range(h): px[0, y] = darker(px[0, y])

def main():
    count = 0
    for color in COLORS:
        base = Image.open(os.path.join(BASE, f'smooth_{color}_concrete.png')).convert('RGBA')
        for pattern, edges in PATTERN_EDGES.items():
            v = base.copy()
            draw_edges(v, edges)
            v.save(os.path.join(BASE, f'smooth_{color}_concrete_ctm_{pattern}.png'))
            count += 1
    print(f'Regenerated {count} CTM textures')

if __name__ == '__main__':
    main()
