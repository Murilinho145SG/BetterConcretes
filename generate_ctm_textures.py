"""
Generates 6 CTM (Connected Texture Mod) pattern textures per color for smooth concrete.

Pattern definitions (border = 1px darker line on edge):
  0 = no borders (fully connected)
  1 = border on bottom edge only
  2 = borders on bottom + left edges (adjacent corner)
  3 = borders on left + right edges (opposite)
  4 = borders on right + bottom + left (top open)
  5 = all 4 borders

The custom model system uses UV rotation to orient these patterns correctly per face.
"""

from PIL import Image
import os

COLORS = [
    'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink',
    'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'
]

TEXTURE_DIR = os.path.join(
    os.path.dirname(__file__),
    'src', 'main', 'resources', 'assets', 'betterconcretes', 'textures', 'block'
)

# Border darkness factor (0.0 = black, 1.0 = same as base)
BORDER_DARKEN = 0.70


def darken_color(rgb, factor=BORDER_DARKEN):
    """Darken an RGB tuple by a factor."""
    return tuple(max(0, int(c * factor)) for c in rgb[:3])


def get_base_color(img):
    """Extract the dominant color from a texture (center pixel)."""
    px = img.getpixel((8, 8))
    return px[:3] if len(px) >= 3 else (px[0], px[0], px[0])


def create_ctm_texture(base_rgb, pattern_id):
    """
    Create a 16x16 CTM texture with borders on specific edges.

    Patterns:
      0: no borders
      1: bottom
      2: bottom + left
      3: left + right
      4: right + bottom + left
      5: all borders
    """
    img = Image.new('RGBA', (16, 16), (*base_rgb, 255))
    border_rgb = darken_color(base_rgb)
    border_color = (*border_rgb, 255)

    has_top = pattern_id == 5
    has_bottom = pattern_id in (1, 2, 4, 5)
    has_left = pattern_id in (2, 3, 4, 5)
    has_right = pattern_id in (3, 4, 5)

    # Draw borders (1 pixel wide)
    if has_top:
        for x in range(16):
            img.putpixel((x, 0), border_color)

    if has_bottom:
        for x in range(16):
            img.putpixel((x, 15), border_color)

    if has_left:
        for y in range(16):
            img.putpixel((0, y), border_color)

    if has_right:
        for y in range(16):
            img.putpixel((15, y), border_color)

    return img


def main():
    os.makedirs(TEXTURE_DIR, exist_ok=True)

    generated = 0
    for color in COLORS:
        src_path = os.path.join(TEXTURE_DIR, f'smooth_{color}_concrete.png')
        if not os.path.exists(src_path):
            print(f'WARNING: {src_path} not found, skipping {color}')
            continue

        src = Image.open(src_path).convert('RGBA')
        base_rgb = get_base_color(src)

        for pattern_id in range(6):
            tex = create_ctm_texture(base_rgb, pattern_id)
            out_path = os.path.join(TEXTURE_DIR, f'smooth_{color}_concrete_ctm_{pattern_id}.png')
            tex.save(out_path)
            generated += 1

        print(f'  {color}: base=#{base_rgb[0]:02x}{base_rgb[1]:02x}{base_rgb[2]:02x} -> 6 patterns')

    print(f'\nGenerated {generated} CTM textures in {TEXTURE_DIR}')


if __name__ == '__main__':
    main()
