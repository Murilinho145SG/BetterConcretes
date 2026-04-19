"""
Asset generator for Better Concretes.

Generates textures and JSON files (blockstate, model, item model, loot table)
for variant blocks across all 16 dye colors.

Run: python generate_assets.py
"""
from __future__ import annotations

import json
import os
import random
from typing import Callable, Tuple

from PIL import Image

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "src", "main", "resources")
NS = "betterconcretes"

ASSETS = os.path.join(RES, "assets", NS)
DATA = os.path.join(RES, "data", NS)

TEX_BLOCK = os.path.join(ASSETS, "textures", "block")
BLOCKSTATE = os.path.join(ASSETS, "blockstates")
MODEL_BLOCK = os.path.join(ASSETS, "models", "block")
MODEL_ITEM = os.path.join(ASSETS, "models", "item")
LOOT = os.path.join(DATA, "loot_table", "blocks")
RECIPE = os.path.join(DATA, "recipe")
TAG_MINEABLE_PICKAXE = os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "pickaxe.json")

for d in (TEX_BLOCK, BLOCKSTATE, MODEL_BLOCK, MODEL_ITEM, LOOT, RECIPE):
    os.makedirs(d, exist_ok=True)
os.makedirs(os.path.dirname(TAG_MINEABLE_PICKAXE), exist_ok=True)


# ---------------------------------------------------------------------------
# Vanilla concrete palette (approximate hex from MC 1.21 textures)
# ---------------------------------------------------------------------------

CONCRETE_COLORS: dict[str, Tuple[int, int, int]] = {
    "white":      (207, 213, 214),
    "orange":     (224, 97, 1),
    "magenta":    (169, 48, 159),
    "light_blue": (54, 169, 217),
    "yellow":     (240, 175, 21),
    "lime":       (94, 168, 24),
    "pink":       (213, 101, 142),
    "gray":       (54, 57, 61),
    "light_gray": (125, 125, 115),
    "cyan":       (21, 119, 136),
    "purple":     (100, 31, 156),
    "blue":       (45, 47, 143),
    "brown":      (96, 59, 32),
    "green":      (73, 91, 36),
    "red":        (142, 33, 33),
    "black":      (8, 10, 15),
}

DYE_COLORS = list(CONCRETE_COLORS.keys())


# ---------------------------------------------------------------------------
# Texture helpers
# ---------------------------------------------------------------------------

def shade(color: Tuple[int, int, int], delta: int) -> Tuple[int, int, int]:
    return tuple(max(0, min(255, c + delta)) for c in color)


def add_noise(img: Image.Image, amount: int, seed: int) -> Image.Image:
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


def base_tile(color: Tuple[int, int, int], noise_amt: int, seed: int) -> Image.Image:
    img = Image.new("RGBA", (16, 16), color + (255,))
    return add_noise(img, noise_amt, seed)


# ---------------------------------------------------------------------------
# Variant texture functions — each takes (color_name, base_rgb) → Image
# ---------------------------------------------------------------------------

def tex_smooth(color_name: str, base: Tuple[int, int, int]) -> Image.Image:
    """Smooth concrete: very light noise + subtle top highlight + bottom shadow."""
    img = base_tile(base, noise_amt=2, seed=hash(("smooth", color_name)) & 0xFFFF)
    px = img.load()
    light = shade(base, 18) + (255,)
    dark = shade(base, -18) + (255,)
    for x in range(16):
        px[x, 0] = light
        px[x, 15] = dark
    return img


def tex_chiseled(color_name: str, base: Tuple[int, int, int]) -> Image.Image:
    """Chiseled concrete: framed inset square with central detail, 3D edges."""
    img = base_tile(base, noise_amt=3, seed=hash(("chiseled", color_name)) & 0xFFFF)
    px = img.load()
    light = shade(base, 25) + (255,)
    dark = shade(base, -30) + (255,)
    darker = shade(base, -55) + (255,)

    # outer bevel: top/left light, bottom/right dark
    for i in range(16):
        px[i, 0] = light
        px[0, i] = light
        px[i, 15] = dark
        px[15, i] = dark
    px[15, 0] = base + (255,)
    px[0, 15] = base + (255,)

    # inset square frame (cols/rows 3..12)
    for x in range(3, 13):
        px[x, 3] = darker
        px[x, 12] = light
    for y in range(3, 13):
        px[3, y] = darker
        px[12, y] = light
    px[3, 3] = darker
    px[12, 12] = light

    # central diamond detail
    for (x, y) in [(7, 6), (8, 6), (6, 7), (9, 7), (6, 8), (9, 8), (7, 9), (8, 9)]:
        px[x, y] = dark
    for (x, y) in [(7, 7), (8, 7), (7, 8), (8, 8)]:
        px[x, y] = light

    return img


def tex_polished(color_name: str, base: Tuple[int, int, int]) -> Image.Image:
    """Polished concrete: very uniform with strong diagonal sheen."""
    img = Image.new("RGBA", (16, 16), base + (255,))
    img = add_noise(img, amount=1, seed=hash(("polished", color_name)) & 0xFFFF)
    px = img.load()
    light = shade(base, 22) + (255,)
    light2 = shade(base, 12) + (255,)
    dark = shade(base, -18) + (255,)
    # diagonal highlight from top-left to bottom-right
    for i in range(16):
        if 0 <= i < 16:
            px[i, i] = light
        if 1 <= i < 16:
            px[i - 1, i] = light2
            px[i, i - 1] = light2
    # bottom-right shadow corner
    for x in range(11, 16):
        for y in range(11, 16):
            if (x + y) >= 24:
                px[x, y] = dark
    return img


def tex_brick(color_name: str, base: Tuple[int, int, int]) -> Image.Image:
    """Brick concrete: 3 rows of bricks with darker mortar lines."""
    img = base_tile(base, noise_amt=3, seed=hash(("brick", color_name)) & 0xFFFF)
    px = img.load()
    mortar = shade(base, -45) + (255,)
    highlight = shade(base, 18) + (255,)

    # horizontal mortar
    for x in range(16):
        px[x, 5] = mortar
        px[x, 10] = mortar
        px[x, 15] = mortar
    # vertical mortar (offset between rows)
    for y in range(0, 5):
        px[7, y] = mortar
    for y in range(6, 10):
        px[3, y] = mortar
        px[11, y] = mortar
    for y in range(11, 15):
        px[7, y] = mortar

    # subtle highlight top of each brick row
    for x in range(16):
        if px[x, 0][0] != mortar[0]:
            px[x, 0] = highlight
        if px[x, 6] != mortar:
            px[x, 6] = highlight
        if px[x, 11] != mortar:
            px[x, 11] = highlight

    return img


# ---------------------------------------------------------------------------
# JSON writers
# ---------------------------------------------------------------------------

def write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def write_blockstate(name: str) -> None:
    write_json(
        os.path.join(BLOCKSTATE, f"{name}.json"),
        {
            "variants": {
                "": {"model": f"{NS}:block/{name}"}
            }
        },
    )


def write_block_model(name: str) -> None:
    write_json(
        os.path.join(MODEL_BLOCK, f"{name}.json"),
        {
            "parent": "minecraft:block/cube_all",
            "textures": {"all": f"{NS}:block/{name}"},
        },
    )


def write_item_model(name: str) -> None:
    write_json(
        os.path.join(MODEL_ITEM, f"{name}.json"),
        {"parent": f"{NS}:block/{name}"},
    )


def write_loot_table(name: str) -> None:
    write_json(
        os.path.join(LOOT, f"{name}.json"),
        {
            "type": "minecraft:block",
            "pools": [
                {
                    "rolls": 1,
                    "bonus_rolls": 0,
                    "entries": [
                        {
                            "type": "minecraft:item",
                            "name": f"{NS}:{name}",
                        }
                    ],
                    "conditions": [
                        {"condition": "minecraft:survives_explosion"}
                    ],
                }
            ],
        },
    )


def write_chiseling_recipe(name: str, color: str) -> None:
    """Vanilla shapeless recipe: 1 chisel + 1 colored concrete = 1 variant block.
    Used as a fallback so the block is craftable even without the right-click flow.
    The chisel is preserved (handled by the chiseling event handler later).
    """
    write_json(
        os.path.join(RECIPE, f"{name}_from_chisel.json"),
        {
            "type": "minecraft:crafting_shapeless",
            "category": "building",
            "ingredients": [
                {"item": f"{NS}:chisel"},
                {"item": f"minecraft:{color}_concrete"},
            ],
            "result": {"id": f"{NS}:{name}"},
        },
    )


# ---------------------------------------------------------------------------
# Variant pipeline
# ---------------------------------------------------------------------------

VariantFn = Callable[[str, Tuple[int, int, int]], Image.Image]

VARIANTS: dict[str, VariantFn] = {
    "smooth_{color}_concrete": tex_smooth,
    "chiseled_{color}_concrete": tex_chiseled,
    "polished_{color}_concrete": tex_polished,
    "brick_{color}_concrete": tex_brick,
}


def generate_variant(name_pattern: str, tex_fn: VariantFn) -> list[str]:
    names = []
    for color, base_rgb in CONCRETE_COLORS.items():
        name = name_pattern.replace("{color}", color)
        img = tex_fn(color, base_rgb)
        img.save(os.path.join(TEX_BLOCK, f"{name}.png"))
        write_blockstate(name)
        write_block_model(name)
        write_item_model(name)
        write_loot_table(name)
        write_chiseling_recipe(name, color)
        names.append(name)
    return names


def write_pickaxe_tag(block_names: list[str]) -> None:
    write_json(
        TAG_MINEABLE_PICKAXE,
        {
            "replace": False,
            "values": [f"{NS}:{name}" for name in sorted(block_names)],
        },
    )


def generate_lang_entries() -> dict[str, str]:
    """Returns a dict of translation keys -> en_us values for all generated blocks."""
    entries: dict[str, str] = {}
    for name_pattern in VARIANTS:
        for color in DYE_COLORS:
            name = name_pattern.replace("{color}", color)
            key = f"block.{NS}.{name}"
            # human-readable: "Smooth White Concrete"
            words = name.replace("_", " ").title()
            entries[key] = words
    return entries


if __name__ == "__main__":
    all_names: list[str] = []
    for pattern, fn in VARIANTS.items():
        names = generate_variant(pattern, fn)
        print(f"  {pattern}: {len(names)} blocks")
        all_names.extend(names)
    print(f"Generated {len(all_names)} blocks across {len(VARIANTS)} variants.")

    write_pickaxe_tag(all_names)
    print(f"  pickaxe tag: {TAG_MINEABLE_PICKAXE}")

    lang = generate_lang_entries()
    print(f"Generated {len(lang)} lang entries.")
    lang_dump = os.path.join(os.path.dirname(__file__), "lang_entries.json")
    write_json(lang_dump, lang)
    print(f"  lang dump: {lang_dump}")
