"""Regenerate 64 base block textures with advanced techniques:
- Value-noise 2D (hash-based, tileable) for organic smooth variation
- Bevel 3D shading on chiseled pattern
- Specular highlights on polished
- Per-brick AO shadows + top highlight on brick
"""
from PIL import Image
import math
import os

BASE = os.path.join(
    os.path.dirname(__file__), '..',
    'src', 'main', 'resources', 'assets', 'betterconcretes', 'textures', 'block'
)

COLOR_RGB = {
    'white':      (207, 213, 214),
    'orange':     (224,  97,   0),
    'magenta':    (169,  48, 159),
    'light_blue': ( 36, 137, 199),
    'yellow':     (241, 175,  21),
    'lime':       ( 94, 169,  25),
    'pink':       (213, 101, 143),
    'gray':       ( 54,  57,  61),
    'light_gray': (125, 125, 115),
    'cyan':       ( 21, 119, 136),
    'purple':     (100,  32, 156),
    'blue':       ( 45,  47, 143),
    'brown':      ( 96,  59,  32),
    'green':      ( 73,  91,  36),
    'red':        (142,  33,  33),
    'black':      ( 15,  18,  22),
}

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def shade(rgb, factor):
    return tuple(clamp(c * factor) for c in rgb)

def mix(a, b, t):
    return tuple(clamp(a[i]*(1-t) + b[i]*t) for i in range(3))

def hash2(x, y, seed):
    x %= 16; y %= 16
    h = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0

def smoothstep(t):
    return t * t * (3 - 2 * t)

def value_noise(x, y, cell_size, seed):
    fx = x / cell_size
    fy = y / cell_size
    x0 = int(fx); y0 = int(fy)
    tx = smoothstep(fx - x0)
    ty = smoothstep(fy - y0)
    cells = max(1, 16 // cell_size)
    a = hash2(x0 % cells, y0 % cells, seed)
    b = hash2((x0+1) % cells, y0 % cells, seed)
    c = hash2(x0 % cells, (y0+1) % cells, seed)
    d = hash2((x0+1) % cells, (y0+1) % cells, seed)
    top = a * (1-tx) + b * tx
    bot = c * (1-tx) + d * tx
    return top * (1-ty) + bot * ty

def fbm(x, y, seed, octaves=3):
    total = 0.0
    amp = 1.0
    max_amp = 0.0
    cell = 8
    for i in range(octaves):
        if cell < 1: break
        total += value_noise(x, y, cell, seed + i * 1337) * amp
        max_amp += amp
        amp *= 0.5
        cell //= 2
    return total / max_amp if max_amp > 0 else 0.5

def gen_smooth(base_rgb, seed):
    img = Image.new('RGBA', (16, 16), (*base_rgb, 255))
    px = img.load()
    for y in range(16):
        for x in range(16):
            n = fbm(x, y, seed, octaves=3)
            delta = (n - 0.5) * 0.16
            factor = 1.0 + delta
            shaded = shade(base_rgb, factor)
            px[x, y] = (*shaded, 255)
    return img

def gen_polished(base_rgb, seed):
    img = Image.new('RGBA', (16, 16), (*base_rgb, 255))
    px = img.load()
    for y in range(16):
        for x in range(16):
            t = (x + y) / 30.0
            factor = 1.18 - t * 0.34
            dx = x - 3
            dy = y - 3
            spec_dist = math.hypot(dx, dy)
            if spec_dist < 4:
                spec_strength = (1 - spec_dist / 4) ** 2
                factor += spec_strength * 0.22
            n = fbm(x, y, seed, octaves=2)
            factor += (n - 0.5) * 0.04
            shaded = shade(base_rgb, factor)
            px[x, y] = (*shaded, 255)
    return img

def gen_chiseled(base_rgb, seed):
    img = gen_smooth(base_rgb, seed * 31)
    px = img.load()
    darker = shade(base_rgb, 0.40)
    light = shade(base_rgb, 1.30)
    lighter = shade(base_rgb, 1.50)

    for i in range(16):
        px[i, 0] = (*lighter, 255)
        px[0, i] = (*lighter, 255)
        px[i, 15] = (*darker, 255)
        px[15, i] = (*darker, 255)

    for i in range(2, 14):
        px[i, 2] = (*darker, 255)
        px[2, i] = (*darker, 255)
        px[i, 13] = (*light, 255)
        px[13, i] = (*light, 255)

    diamond_outline = [
        (7,4,'tl'),(8,4,'tl'),
        (6,5,'tl'),(9,5,'tl'),
        (5,6,'tl'),(10,6,'tl'),
        (4,7,'tl'),(11,7,'tl'),
        (4,8,'br'),(11,8,'br'),
        (5,9,'br'),(10,9,'br'),
        (6,10,'br'),(9,10,'br'),
        (7,11,'br'),(8,11,'br'),
    ]
    diamond_fill = [
        (7,5),(8,5),
        (6,6),(7,6),(8,6),(9,6),
        (5,7),(6,7),(7,7),(8,7),(9,7),(10,7),
        (5,8),(6,8),(7,8),(8,8),(9,8),(10,8),
        (6,9),(7,9),(8,9),(9,9),
        (7,10),(8,10),
    ]
    inside = shade(base_rgb, 0.88)
    for x, y in diamond_fill:
        px[x, y] = (*inside, 255)
    for x, y, side in diamond_outline:
        if side == 'tl':
            px[x, y] = (*darker, 255)
        else:
            px[x, y] = (*light, 255)
    return img

def gen_brick(base_rgb, seed):
    img = gen_smooth(base_rgb, seed * 17)
    px = img.load()
    mortar = shade(base_rgb, 0.48)
    edge_light = shade(base_rgb, 1.22)

    mortar_rows = [3, 7, 11, 15]
    for y in mortar_rows:
        for x in range(16):
            px[x, y] = (*mortar, 255)

    def vlines(y_start, y_end, xs):
        for x in xs:
            for y in range(y_start, y_end):
                px[x % 16, y] = (*mortar, 255)
    vlines(0, 3, [0, 8])
    vlines(4, 7, [4, 12])
    vlines(8, 11, [0, 8])
    vlines(12, 15, [4, 12])

    brick_top_rows = [0, 4, 8, 12]
    for y in brick_top_rows:
        for x in range(16):
            r, g, b, _ = px[x, y]
            if (r, g, b) != mortar[:3]:
                blend = mix((r, g, b), edge_light, 0.35)
                px[x, y] = (*blend, 255)

    def darken_px(x, y, factor=0.80):
        x %= 16; y %= 16
        r, g, b, _ = px[x, y]
        px[x, y] = (clamp(r*factor), clamp(g*factor), clamp(b*factor), 255)

    corners = [
        (1, 2), (7, 2), (9, 2), (15, 2),
        (3, 6), (5, 6), (11, 6), (13, 6),
        (1, 10), (7, 10), (9, 10), (15, 10),
        (3, 14), (5, 14), (11, 14), (13, 14),
    ]
    for x, y in corners:
        darken_px(x, y, 0.85)
    return img

GENERATORS = {
    'smooth':   gen_smooth,
    'chiseled': gen_chiseled,
    'polished': gen_polished,
    'brick':    gen_brick,
}

def main():
    count = 0
    for variant, gen in GENERATORS.items():
        for color, rgb in COLOR_RGB.items():
            seed = (hash((variant, color)) & 0xFFFF) + 1
            img = gen(rgb, seed)
            path = os.path.join(BASE, f'{variant}_{color}_concrete.png')
            img.save(path)
            count += 1
    print(f'Regenerated {count} base textures with advanced shading')

if __name__ == '__main__':
    main()
