"""Generate common (c:) namespace tags for the 64 mod concrete blocks + items.

Tags created:
  data/c/tags/block/concretes.json       — all 64 blocks
  data/c/tags/item/concretes.json        — all 64 items
  data/c/tags/block/{color}_concretes.json  — 16 per-color tags (4 variants each)
  data/c/tags/item/{color}_concretes.json   — idem

This lets any mod using NeoForge common tag conventions discover our blocks
without hardcoding our mod id.
"""
import json
import os

DATA = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/data'
)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']
VARIANTS = ['smooth','chiseled','polished','brick']
MOD_ID = 'betterconcretes'


def write_tag(tag_ns, kind, tag_name, values):
    """kind is 'block' or 'item'. tag_ns is the namespace of the tag (c or minecraft)."""
    path = os.path.join(DATA, tag_ns, 'tags', kind, f'{tag_name}.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'replace': False, 'values': values}, f, indent=2)


def all_mod_entries():
    return [f'{MOD_ID}:{v}_{c}_concrete' for v in VARIANTS for c in COLORS]


def per_color_entries(color):
    return [f'{MOD_ID}:{v}_{color}_concrete' for v in VARIANTS]


def main():
    all_blocks = all_mod_entries()

    # c:concretes (master tag)
    write_tag('c', 'block', 'concretes', all_blocks)
    write_tag('c', 'item', 'concretes', all_blocks)

    # c:building_blocks (decorative)
    write_tag('c', 'block', 'building_blocks', all_blocks)
    write_tag('c', 'item', 'building_blocks', all_blocks)

    # Per-color tags
    for color in COLORS:
        vals = per_color_entries(color)
        write_tag('c', 'block', f'{color}_concretes', vals)
        write_tag('c', 'item', f'{color}_concretes', vals)

    print(f'wrote: c:concretes (blocks + items), c:building_blocks, 16 per-color tags')


if __name__ == '__main__':
    main()
