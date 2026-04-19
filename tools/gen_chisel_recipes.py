"""Generate 320 chisel recipe JSONs (5 variants * 4 targets * 16 colors).

Also deletes the obsolete 64 *_from_chisel.json shapeless recipes
(chisel was incorrectly being consumed — new recipes handle durability in-menu).
"""
import json
import os
import sys

RECIPE_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/data/betterconcretes/recipe'
)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']

# variant_name -> item resource id template ("{color}" placeholder)
# vanilla concrete has no prefix; mod variants have prefix_
VARIANTS = {
    'vanilla':  ('minecraft:{color}_concrete',          '{color}_concrete'),
    'smooth':   ('betterconcretes:smooth_{color}_concrete',   'smooth_{color}_concrete'),
    'chiseled': ('betterconcretes:chiseled_{color}_concrete', 'chiseled_{color}_concrete'),
    'polished': ('betterconcretes:polished_{color}_concrete', 'polished_{color}_concrete'),
    'brick':    ('betterconcretes:brick_{color}_concrete',    'brick_{color}_concrete'),
}


def recipe_json(input_id, result_id):
    return {
        'type': 'betterconcretes:chisel',
        'ingredient': {'item': input_id},
        'result': {'id': result_id},
    }


def clean_old_shapeless():
    """Remove the obsolete *_from_chisel.json shapeless recipes."""
    deleted = 0
    for name in os.listdir(RECIPE_DIR):
        if name.endswith('_from_chisel.json'):
            os.remove(os.path.join(RECIPE_DIR, name))
            deleted += 1
    print(f'deleted {deleted} old shapeless from_chisel recipes')


def generate_all():
    count = 0
    variant_names = list(VARIANTS.keys())
    for color in COLORS:
        for in_name in variant_names:
            in_id = VARIANTS[in_name][0].format(color=color)
            for out_name in variant_names:
                if in_name == out_name:
                    continue
                out_id = VARIANTS[out_name][0].format(color=color)
                out_file_piece = VARIANTS[out_name][1].format(color=color)
                in_file_piece = VARIANTS[in_name][1].format(color=color)
                # Filename: chisel_{in}_to_{out}.json
                fname = f'chisel_{in_file_piece}_to_{out_file_piece}.json'
                path = os.path.join(RECIPE_DIR, fname)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(recipe_json(in_id, out_id), f, indent=2)
                count += 1
    print(f'wrote {count} chisel recipe JSONs')


if __name__ == '__main__':
    if '--clean' in sys.argv:
        clean_old_shapeless()
    generate_all()
