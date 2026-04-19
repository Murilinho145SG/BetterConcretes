"""
Texture generator for Better Concretes.
Generates 16x16 PNG textures procedurally.
Run: python generate_textures.py
"""
from PIL import Image
import random
import os

OUT = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(OUT, exist_ok=True)


def add_noise(img, amount=6, seed=42):
    rng = random.Random(seed)
    px = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            n = rng.randint(-amount, amount)
            px[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
                a,
            )
    return img


def base_concrete(color=(207, 213, 214), seed=42, noise=6):
    img = Image.new("RGBA", (16, 16), color + (255,))
    return add_noise(img, noise, seed)


def shade(color, delta):
    return tuple(max(0, min(255, c + delta)) for c in color[:3]) + (255,)


def cracked_concrete():
    """Concreto rachado: base com rachaduras irregulares."""
    img = base_concrete(seed=7)
    px = img.load()
    dark = (78, 82, 83, 255)
    mid = (130, 135, 136, 255)

    cracks = [
        [(1, 2), (2, 2), (3, 3), (4, 3), (5, 4), (6, 4), (7, 5), (8, 5), (9, 6), (10, 6), (11, 7)],
        [(11, 7), (12, 8), (13, 8), (14, 9)],
        [(8, 5), (8, 6), (9, 7), (9, 8), (10, 9), (10, 10), (9, 11), (8, 12), (7, 13), (6, 13)],
        [(2, 10), (3, 10), (3, 11), (4, 12), (5, 13), (6, 13)],
        [(13, 1), (13, 2), (14, 3), (14, 4), (13, 5)],
        [(4, 14), (5, 14), (5, 15)],
    ]
    for crack in cracks:
        for (x, y) in crack:
            if 0 <= x < 16 and 0 <= y < 16:
                px[x, y] = dark
        # suavizar extremidades
        if crack:
            ex, ey = crack[0]
            if 0 <= ex < 16 and 0 <= ey < 16:
                px[ex, ey] = mid
    return img


def chiseled_concrete():
    """Concreto entalhado: padrão decorativo com profundidade simulada."""
    img = base_concrete(seed=11, noise=4)
    px = img.load()
    base = (207, 213, 214)
    light = shade(base, 20)
    dark = shade(base, -40)
    darker = shade(base, -70)

    # moldura externa (borda inset)
    for i in range(16):
        px[i, 0] = light
        px[0, i] = light
        px[i, 15] = dark
        px[15, i] = dark
    px[0, 15] = base + (255,)
    px[15, 0] = base + (255,)

    # quadrado central entalhado (4..11)
    for x in range(4, 12):
        px[x, 4] = darker
        px[x, 11] = light
    for y in range(4, 12):
        px[4, y] = darker
        px[11, y] = light
    # cantos do quadrado
    px[4, 4] = darker
    px[11, 11] = light

    # detalhe: pequeno losango no centro
    center_pixels = [(7, 6), (8, 6), (6, 7), (9, 7), (6, 8), (9, 8), (7, 9), (8, 9)]
    for (x, y) in center_pixels:
        px[x, y] = dark
    px[7, 7] = light
    px[8, 7] = light
    px[7, 8] = light
    px[8, 8] = light

    return img


def brick_concrete():
    """Concreto em padrão de tijolo, com argamassa mais escura."""
    img = base_concrete((198, 204, 205), seed=23, noise=5)
    px = img.load()
    mortar = (95, 100, 101, 255)
    mortar_hl = (145, 150, 151, 255)

    # 3 fileiras de tijolos (0-4, 5-9, 10-14), argamassa em y=4, 9, 14/15
    for x in range(16):
        px[x, 4] = mortar
        px[x, 9] = mortar
        px[x, 15] = mortar

    # fileira 1 (y 0..3): divisão em x=7
    for y in range(0, 4):
        px[7, y] = mortar
    # fileira 2 (y 5..8): divisões offset em x=3 e x=11
    for y in range(5, 9):
        px[3, y] = mortar
        px[11, y] = mortar
    # fileira 3 (y 10..14): divisão em x=7 (como fileira 1)
    for y in range(10, 15):
        px[7, y] = mortar

    # highlights topo dos tijolos (linha acima da argamassa)
    for x in range(16):
        if px[x, 5][0] < 150:
            continue
        px[x, 5] = mortar_hl if x != 3 and x != 11 else px[x, 5]
    return img


def smooth_concrete():
    """Concreto liso: base uniforme com leve variação e borda sutil."""
    img = base_concrete((215, 220, 221), seed=3, noise=3)
    px = img.load()
    edge = (180, 185, 186, 255)
    for i in range(16):
        px[i, 0] = edge
        px[0, i] = edge
    return img


def glowing_concrete():
    """Concreto luminoso: base com núcleos amarelados (como se emitisse luz)."""
    img = base_concrete((207, 213, 214), seed=19, noise=4)
    px = img.load()
    glow_core = (255, 230, 120, 255)
    glow_mid = (240, 210, 140, 255)
    glow_soft = (225, 205, 160, 255)

    spots = [(3, 3), (11, 4), (6, 9), (13, 11), (4, 12)]
    for (cx, cy) in spots:
        if 0 <= cx < 16 and 0 <= cy < 16:
            px[cx, cy] = glow_core
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 16 and 0 <= ny < 16:
                r, g, b, _ = px[nx, ny]
                # só clareia se for pixel base
                px[nx, ny] = glow_mid if (r + g + b) > 400 else glow_soft
    return img


def scaled(img, factor=16):
    return img.resize((16 * factor, 16 * factor), Image.NEAREST)


def save_pair(img, name):
    img.save(os.path.join(OUT, f"{name}.png"))
    scaled(img).save(os.path.join(OUT, f"{name}_x16.png"))


if __name__ == "__main__":
    save_pair(cracked_concrete(), "cracked_concrete")
    save_pair(chiseled_concrete(), "chiseled_concrete")
    save_pair(brick_concrete(), "brick_concrete")
    save_pair(smooth_concrete(), "smooth_concrete")
    save_pair(glowing_concrete(), "glowing_concrete")
    print(f"Textures saved to: {OUT}")
