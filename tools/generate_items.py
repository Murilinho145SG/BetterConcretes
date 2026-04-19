"""
Item art test: magic sword + magic amulet, 16x16.
"""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(OUT, exist_ok=True)


def new_img():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def put(px, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        px[x, y] = color


def line(px, x0, y0, x1, y1, color):
    """Bresenham line for pixel-perfect diagonals."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        put(px, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def magic_sword():
    img = new_img()
    px = img.load()

    # Paleta — lâmina ciano mágica
    b_tip = (240, 255, 255, 255)
    b_hi = (170, 230, 255, 255)
    b_mid = (70, 160, 230, 255)
    b_lo = (30, 90, 170, 255)
    b_dk = (15, 45, 100, 255)

    rune = (255, 220, 80, 255)
    rune_glow = (255, 245, 180, 255)

    # Guarda dourada com gema
    g_lo = (110, 70, 15, 255)
    g_mid = (200, 150, 40, 255)
    g_hi = (255, 220, 100, 255)

    # Punho (couro escuro + fio)
    h_dk = (25, 18, 30, 255)
    h_mid = (60, 45, 70, 255)
    h_hi = (110, 85, 130, 255)

    # Pomo — gema roxa
    p_dk = (60, 20, 90, 255)
    p_mid = (150, 60, 200, 255)
    p_hi = (220, 150, 240, 255)
    p_glow = (255, 220, 255, 255)

    # ---- LÂMINA ----
    # Eixo central da lâmina (diagonal anti-aliased por Bresenham)
    center = [(7, 9), (8, 8), (9, 7), (10, 6), (11, 5), (12, 4), (13, 3), (14, 2)]

    # Lado escuro (abaixo/esquerda) — lo
    for (x, y) in center:
        put(px, x - 1, y, b_lo)
    # Centro — mid
    for (x, y) in center:
        put(px, x, y, b_mid)
    # Lado claro (acima/direita) — hi
    for (x, y) in center:
        put(px, x, y - 1, b_hi)
    # Borda escura extrema
    for (x, y) in center:
        put(px, x - 1, y + 1, b_dk)

    # Ponta da lâmina brilhante
    put(px, 14, 1, b_tip)
    put(px, 15, 1, b_hi)
    put(px, 15, 0, b_tip)
    put(px, 14, 0, b_hi)
    put(px, 13, 2, b_tip)

    # Runa brilhante no meio da lâmina
    put(px, 10, 6, rune)
    put(px, 11, 5, rune_glow)
    put(px, 9, 7, rune)

    # ---- GUARDA (cross-guard) ----
    # Formato curvado: canto inferior-esquerdo, atravessando diagonalmente
    # Base da guarda na transição lâmina→punho (posição ~6,10)
    guard_pixels = [
        (4, 11, g_lo), (5, 11, g_mid), (6, 10, g_hi), (7, 10, g_mid),
        (5, 12, g_lo), (6, 11, g_hi), (7, 11, g_mid), (8, 10, g_hi),
        (4, 12, g_mid), (3, 12, g_lo),
        (8, 9, g_hi), (9, 9, g_mid),
    ]
    for (x, y, c) in guard_pixels:
        put(px, x, y, c)
    # Gema central da guarda
    put(px, 6, 11, (255, 80, 80, 255))  # vermelho
    put(px, 7, 10, (255, 180, 180, 255))  # highlight

    # ---- PUNHO ----
    hilt_pixels = [
        (3, 13, h_dk), (4, 13, h_mid), (5, 13, h_hi),
        (2, 14, h_dk), (3, 14, h_mid), (4, 14, h_hi),
        (2, 13, h_mid),
    ]
    for (x, y, c) in hilt_pixels:
        put(px, x, y, c)

    # ---- POMO / GEMA ----
    put(px, 1, 15, p_dk)
    put(px, 2, 15, p_mid)
    put(px, 1, 14, p_mid)
    put(px, 0, 15, p_dk)
    put(px, 2, 14, p_hi)
    # sparkle
    put(px, 3, 15, p_glow)

    return img


def magic_amulet():
    img = new_img()
    px = img.load()

    # Moldura dourada
    g_dk = (110, 70, 15, 255)
    g_mid = (200, 150, 40, 255)
    g_hi = (255, 220, 100, 255)
    g_glow = (255, 245, 180, 255)

    # Gema central (cristal ciano mágico)
    c_dk = (15, 50, 100, 255)
    c_mid = (60, 150, 220, 255)
    c_hi = (180, 235, 255, 255)
    c_core = (255, 255, 255, 255)

    # Corrente
    ch_dk = (80, 65, 25, 255)
    ch_hi = (220, 180, 60, 255)

    rune = (255, 100, 200, 255)  # runas magenta

    # ---- CORRENTE (topo) ----
    chain = [(6, 0, ch_hi), (7, 0, ch_dk), (8, 0, ch_hi), (9, 0, ch_dk),
             (6, 1, ch_dk), (9, 1, ch_hi),
             (7, 1, g_mid), (8, 1, g_hi)]
    for (x, y, c) in chain:
        put(px, x, y, c)

    # ---- MOLDURA CIRCULAR (aro do amuleto) ----
    # Círculo aproximado de raio 5-6 centrado em (7.5, 9)
    frame_outer = [
        (5, 3), (6, 2), (7, 2), (8, 2), (9, 2), (10, 3),
        (4, 4), (11, 4),
        (3, 5), (12, 5),
        (3, 6), (12, 6),
        (2, 7), (13, 7),
        (2, 8), (13, 8),
        (2, 9), (13, 9),
        (2, 10), (13, 10),
        (3, 11), (12, 11),
        (3, 12), (12, 12),
        (4, 13), (11, 13),
        (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14),
    ]
    for (x, y) in frame_outer:
        put(px, x, y, g_mid)

    # Highlights (topo e esquerda do círculo)
    highlights = [(6, 2), (7, 2), (5, 3), (4, 4), (3, 5), (2, 7), (2, 8)]
    for (x, y) in highlights:
        put(px, x, y, g_hi)
    put(px, 7, 2, g_glow)

    # Shadows (baixo e direita)
    shadows = [(10, 14), (9, 14), (12, 12), (13, 10), (13, 9)]
    for (x, y) in shadows:
        put(px, x, y, g_dk)

    # ---- GEMA CENTRAL (cristal) ----
    gem = [
        (7, 5), (8, 5),
        (6, 6), (7, 6), (8, 6), (9, 6),
        (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
        (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
        (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9),
        (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10),
        (6, 11), (7, 11), (8, 11), (9, 11),
        (7, 12), (8, 12),
    ]
    for (x, y) in gem:
        put(px, x, y, c_mid)

    # Sombras da gema (base/direita)
    gem_shadow = [(9, 9), (9, 10), (10, 9), (10, 10), (8, 11), (9, 11), (7, 12), (8, 12), (6, 11)]
    for (x, y) in gem_shadow:
        put(px, x, y, c_dk)

    # Highlights da gema (topo/esquerda — reflexo)
    gem_hi = [(7, 5), (6, 6), (5, 7), (5, 8), (6, 7)]
    for (x, y) in gem_hi:
        put(px, x, y, c_hi)
    # núcleo de luz
    put(px, 6, 6, c_core)
    put(px, 7, 6, c_hi)

    # Facetas (linhas de corte do cristal)
    put(px, 7, 8, c_hi)
    put(px, 8, 9, c_dk)

    # ---- RUNAS FLUTUANTES ----
    # pequenos pontos mágicos ao redor
    runes = [(1, 6), (14, 6), (0, 9), (15, 9), (4, 2), (11, 2)]
    for (x, y) in runes:
        put(px, x, y, rune)

    return img


def scaled(img, factor=16):
    return img.resize((16 * factor, 16 * factor), Image.NEAREST)


def save(img, name):
    img.save(os.path.join(OUT, f"{name}.png"))
    scaled(img).save(os.path.join(OUT, f"{name}_x16.png"))


if __name__ == "__main__":
    save(magic_sword(), "magic_sword")
    save(magic_amulet(), "magic_amulet")
    print(f"Saved to {OUT}")
