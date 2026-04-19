"""
GUI texture generator — water arrow for JEI category.
"""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(OUT, exist_ok=True)


def put(px, x, y, color, w, h):
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = color


def water_arrow_v1():
    """Solid arrow with outline and 3D shading (clean style)."""
    W, H = 24, 17
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    outline = (20, 50, 100, 255)
    dark = (40, 90, 160, 255)
    mid = (80, 150, 220, 255)
    light = (150, 210, 255, 255)
    shine = (220, 240, 255, 255)

    # ---- BODY ----
    # rectangle from x=1 to x=14, y=5 to y=11 (7 tall)
    body_x0, body_x1 = 1, 15
    body_y0, body_y1 = 5, 12

    # outline
    for x in range(body_x0, body_x1):
        put(px, x, body_y0, outline, W, H)
        put(px, x, body_y1 - 1, outline, W, H)
    for y in range(body_y0, body_y1):
        put(px, body_x0, y, outline, W, H)

    # fill
    for x in range(body_x0 + 1, body_x1):
        for y in range(body_y0 + 1, body_y1 - 1):
            put(px, x, y, mid, W, H)

    # top highlight
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y0 + 1, light, W, H)
    # shine (top)
    for x in range(body_x0 + 2, body_x1 - 1):
        put(px, x, body_y0 + 1, shine, W, H)

    # bottom shadow
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y1 - 2, dark, W, H)

    # ---- ARROW HEAD ----
    # triangle: base at x=14, tip at x=22, center y=8
    cy = 8
    tip_x = 22
    base_x = 14
    half = 7  # triangle half-height

    # draw each row
    for dy in range(-half, half + 1):
        absdy = abs(dy)
        # width proportional
        width = int(round(((half - absdy) / half) * (tip_x - base_x)))
        if width <= 0:
            continue
        y = cy + dy
        for i in range(width):
            x = base_x + i
            # outline at the edges (top and bottom row of each width, plus the "slope" pixels)
            if i == width - 1:
                put(px, x, y, outline, W, H)
            else:
                put(px, x, y, mid, W, H)

    # add explicit outline on the diagonal edges (top and bottom of the triangle)
    # top diagonal: starting at (14, 1) going down-right to (21, 8)
    top_edge = [(14, 1), (15, 2), (16, 3), (17, 4), (18, 5), (19, 6), (20, 7), (21, 8)]
    for (x, y) in top_edge:
        put(px, x, y, outline, W, H)
    bot_edge = [(14, 15), (15, 14), (16, 13), (17, 12), (18, 11), (19, 10), (20, 9), (21, 8)]
    for (x, y) in bot_edge:
        put(px, x, y, outline, W, H)

    # fill interior of triangle (above/below the edges already filled by loop)
    # top half highlights
    for dy in range(-half + 1, 0):
        absdy = abs(dy)
        width = int(round(((half - absdy) / half) * (tip_x - base_x)))
        if width <= 1:
            continue
        y = cy + dy
        # highlight row right below outline
        put(px, base_x + 1, y, light, W, H)

    # tip
    put(px, tip_x - 1, cy, shine, W, H)

    return img


def water_arrow_v2():
    """Stylized arrow — with water droplet accents and softer curves."""
    W, H = 24, 17
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    outline = (15, 40, 90, 255)
    dark = (30, 80, 150, 255)
    mid = (70, 140, 210, 255)
    light = (130, 200, 250, 255)
    shine = (210, 240, 255, 255)
    droplet = (180, 230, 255, 255)

    # body: slightly thicker, 8 tall
    body_x0, body_x1 = 2, 14
    body_y0, body_y1 = 4, 13

    # outline
    for x in range(body_x0, body_x1):
        put(px, x, body_y0, outline, W, H)
        put(px, x, body_y1 - 1, outline, W, H)
    for y in range(body_y0, body_y1):
        put(px, body_x0, y, outline, W, H)

    # fill
    for x in range(body_x0 + 1, body_x1):
        for y in range(body_y0 + 1, body_y1 - 1):
            put(px, x, y, mid, W, H)
    # top highlight band (2 rows)
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y0 + 1, light, W, H)
    for x in range(body_x0 + 2, body_x1 - 1):
        put(px, x, body_y0 + 2, shine, W, H)
    # bottom shadow band
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y1 - 2, dark, W, H)

    # head: larger triangle, base x=13, tip x=22, y centered at 8
    cy = 8
    tip_x = 22
    base_x = 13
    half = 8

    for dy in range(-half, half + 1):
        absdy = abs(dy)
        width = int(round(((half - absdy) / half) * (tip_x - base_x)))
        if width <= 0:
            continue
        y = cy + dy
        for i in range(width):
            x = base_x + i
            if i == width - 1:
                put(px, x, y, outline, W, H)
            else:
                put(px, x, y, mid, W, H)

    # fine diagonal outline on triangle edges
    top_edge = [(13, 0), (14, 1), (15, 2), (16, 3), (17, 4), (18, 5), (19, 6), (20, 7), (21, 8)]
    bot_edge = [(13, 16), (14, 15), (15, 14), (16, 13), (17, 12), (18, 11), (19, 10), (20, 9), (21, 8)]
    for (x, y) in top_edge:
        put(px, x, y, outline, W, H)
    for (x, y) in bot_edge:
        put(px, x, y, outline, W, H)

    # interior highlights — row right below top diagonal
    inner_top = [(14, 2), (15, 3), (16, 4), (17, 5), (18, 6), (19, 7)]
    for (x, y) in inner_top:
        put(px, x, y, light, W, H)
    inner_top2 = [(15, 4), (16, 5), (17, 6), (18, 7)]
    for (x, y) in inner_top2:
        put(px, x, y, shine, W, H)

    # interior shadow — row right above bottom diagonal
    inner_bot = [(14, 14), (15, 13), (16, 12), (17, 11), (18, 10), (19, 9)]
    for (x, y) in inner_bot:
        put(px, x, y, dark, W, H)

    # tip highlight
    put(px, tip_x - 1, cy, shine, W, H)

    # water droplet accents (above and below body, small sparkles)
    put(px, 4, 2, droplet, W, H)
    put(px, 7, 1, droplet, W, H)
    put(px, 5, 15, droplet, W, H)

    return img


def scaled(img, factor=16):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


def save(img, name):
    img.save(os.path.join(OUT, f"{name}.png"))
    scaled(img).save(os.path.join(OUT, f"{name}_x16.png"))


def water_arrow_v3():
    """Vanilla-ish style: grayscale with a subtle blue hint on the tip."""
    W, H = 32, 17
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    outline = (50, 50, 55, 255)
    dark = (100, 100, 105, 255)
    mid = (140, 140, 148, 255)
    light = (180, 180, 188, 255)
    shine = (210, 210, 218, 255)
    tip_blue = (120, 180, 230, 255)
    tip_blue_lt = (180, 220, 245, 255)

    # body 5 tall, 16 wide
    body_x0, body_x1 = 2, 18
    body_y0, body_y1 = 6, 12

    for x in range(body_x0, body_x1):
        put(px, x, body_y0, outline, W, H)
        put(px, x, body_y1 - 1, outline, W, H)
    for y in range(body_y0, body_y1):
        put(px, body_x0, y, outline, W, H)

    for x in range(body_x0 + 1, body_x1):
        for y in range(body_y0 + 1, body_y1 - 1):
            put(px, x, y, mid, W, H)
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y0 + 1, light, W, H)
    for x in range(body_x0 + 2, body_x1 - 1):
        put(px, x, body_y0 + 1, shine, W, H)
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y1 - 2, dark, W, H)

    cy = 8
    tip_x = 28
    base_x = 17
    half = 8

    for dy in range(-half, half + 1):
        absdy = abs(dy)
        width = int(round(((half - absdy) / half) * (tip_x - base_x)))
        if width <= 0:
            continue
        y = cy + dy
        for i in range(width):
            x = base_x + i
            if i == width - 1:
                put(px, x, y, outline, W, H)
            else:
                put(px, x, y, mid, W, H)

    top_edge = [(17, 0), (18, 1), (19, 2), (20, 3), (21, 4), (22, 5), (23, 6), (24, 7), (25, 8)]
    bot_edge = [(17, 16), (18, 15), (19, 14), (20, 13), (21, 12), (22, 11), (23, 10), (24, 9), (25, 8)]
    for (x, y) in top_edge:
        put(px, x, y, outline, W, H)
    for (x, y) in bot_edge:
        put(px, x, y, outline, W, H)

    # tip accent: blue gradient near the point (the magic flavor)
    put(px, 25, 8, tip_blue, W, H)
    put(px, 24, 8, tip_blue, W, H)
    put(px, 23, 8, tip_blue_lt, W, H)
    put(px, 24, 7, tip_blue_lt, W, H)
    put(px, 24, 9, tip_blue_lt, W, H)

    return img


def water_arrow_v4():
    """Desaturated steel-blue — larger and cleaner, no sparkles."""
    W, H = 32, 17
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    outline = (35, 55, 85, 255)
    dark = (65, 95, 135, 255)
    mid = (105, 140, 180, 255)
    light = (155, 185, 215, 255)
    shine = (200, 220, 240, 255)

    # body slightly larger, 7 tall
    body_x0, body_x1 = 2, 20
    body_y0, body_y1 = 5, 13

    for x in range(body_x0, body_x1):
        put(px, x, body_y0, outline, W, H)
        put(px, x, body_y1 - 1, outline, W, H)
    for y in range(body_y0, body_y1):
        put(px, body_x0, y, outline, W, H)

    for x in range(body_x0 + 1, body_x1):
        for y in range(body_y0 + 1, body_y1 - 1):
            put(px, x, y, mid, W, H)
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y0 + 1, light, W, H)
    for x in range(body_x0 + 2, body_x1 - 1):
        put(px, x, body_y0 + 2, shine, W, H)
    for x in range(body_x0 + 1, body_x1):
        put(px, x, body_y1 - 2, dark, W, H)

    cy = 8
    tip_x = 30
    base_x = 18
    half = 8

    for dy in range(-half, half + 1):
        absdy = abs(dy)
        width = int(round(((half - absdy) / half) * (tip_x - base_x)))
        if width <= 0:
            continue
        y = cy + dy
        for i in range(width):
            x = base_x + i
            if i == width - 1:
                put(px, x, y, outline, W, H)
            else:
                put(px, x, y, mid, W, H)

    top_edge = [(18, 0), (19, 1), (20, 2), (21, 3), (22, 4), (23, 5), (24, 6), (25, 7), (26, 8)]
    bot_edge = [(18, 16), (19, 15), (20, 14), (21, 13), (22, 12), (23, 11), (24, 10), (25, 9), (26, 8)]
    for (x, y) in top_edge:
        put(px, x, y, outline, W, H)
    for (x, y) in bot_edge:
        put(px, x, y, outline, W, H)

    # inner highlights on the head
    inner_top = [(19, 2), (20, 3), (21, 4), (22, 5), (23, 6)]
    for (x, y) in inner_top:
        put(px, x, y, light, W, H)
    inner_top2 = [(20, 4), (21, 5), (22, 6)]
    for (x, y) in inner_top2:
        put(px, x, y, shine, W, H)
    inner_bot = [(19, 14), (20, 13), (21, 12), (22, 11), (23, 10)]
    for (x, y) in inner_bot:
        put(px, x, y, dark, W, H)

    # bright tip
    put(px, tip_x - 1, cy, shine, W, H)
    put(px, tip_x - 2, cy, light, W, H)

    return img


def arrow_vanilla():
    """Plain vanilla-style arrow, matching MC's crafting table arrow look.
    Body 15w × 7h (incl outline), head triangle 6 wide × 11 tall (incl outline)."""
    W, H = 22, 15
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()

    outline = (55, 55, 55, 255)
    fill = (139, 139, 139, 255)

    cy = 7

    # ---- BODY: cols 0..14, rows 4..10 ----
    body_x_left = 0
    body_x_right = 14
    body_y_top = 4
    body_y_bot = 10

    # body interior fill first
    for x in range(body_x_left + 1, body_x_right + 1):
        for y in range(body_y_top + 1, body_y_bot):
            put(px, x, y, fill, W, H)

    # body outline (top, bottom, left)
    for x in range(body_x_left, body_x_right + 1):
        put(px, x, body_y_top, outline, W, H)
        put(px, x, body_y_bot, outline, W, H)
    for y in range(body_y_top, body_y_bot + 1):
        put(px, body_x_left, y, outline, W, H)

    # ---- HEAD: triangle from base col 15 to apex col 20 ----
    base_x = 15
    apex_x = 20
    half = 5  # half-height at base

    # interior fill (covers full triangle, will overwrite with outline next)
    for col_offset in range(0, apex_x - base_x + 1):
        x = base_x + col_offset
        h_at_col = half - col_offset
        for dy in range(-h_at_col, h_at_col + 1):
            put(px, x, cy + dy, fill, W, H)

    # diagonal outlines (top edge + bottom edge)
    for col_offset in range(0, apex_x - base_x + 1):
        x = base_x + col_offset
        h_at_col = half - col_offset
        put(px, x, cy - h_at_col, outline, W, H)
        put(px, x, cy + h_at_col, outline, W, H)

    return img


if __name__ == "__main__":
    save(water_arrow_v1(), "water_arrow_v1")
    save(water_arrow_v2(), "water_arrow_v2")
    save(water_arrow_v3(), "water_arrow_v3")
    save(water_arrow_v4(), "water_arrow_v4")
    save(arrow_vanilla(), "arrow_vanilla")
    print(f"Saved to {OUT}")
