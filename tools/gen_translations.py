"""Generate pt_br.json, pt_pt.json, fr_fr.json from the en_us schema."""
import json
import os

OUT_DIR = os.path.join(
    os.path.dirname(__file__), '..',
    'src/main/resources/assets/betterconcretes/lang'
)

COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray',
          'light_gray','cyan','purple','blue','brown','green','red','black']
VARIANTS = ['smooth','chiseled','polished','brick']

COLOR_NAMES = {
    'pt_br': ['Branco','Laranja','Magenta','Azul Claro','Amarelo','Verde-limão','Rosa','Cinza','Cinza Claro','Ciano','Roxo','Azul','Marrom','Verde','Vermelho','Preto'],
    'pt_pt': ['Branco','Laranja','Magenta','Azul-claro','Amarelo','Verde-lima','Cor-de-rosa','Cinzento','Cinzento-claro','Ciano','Roxo','Azul','Castanho','Verde','Vermelho','Preto'],
    'fr_fr': ['blanc','orange','magenta','bleu clair','jaune','vert clair','rose','gris','gris clair','cyan','violet','bleu','marron','vert','rouge','noir'],
}

BASE_NOUN = {'pt_br': 'Concreto', 'pt_pt': 'Betão', 'fr_fr': 'Béton'}
VARIANT_SUFFIX = {
    'pt_br': {'smooth': 'Liso', 'chiseled': 'Esculpido', 'polished': 'Polido'},
    'pt_pt': {'smooth': 'Liso', 'chiseled': 'Cinzelado', 'polished': 'Polido'},
    'fr_fr': {'smooth': 'lisse', 'chiseled': 'ciselé', 'polished': 'poli'},
}
BRICK_PREFIX = {'pt_br': 'Tijolos de Concreto', 'pt_pt': 'Tijolos de Betão', 'fr_fr': 'Briques de béton'}


def block_name(locale, variant, color_idx):
    color_name = COLOR_NAMES[locale][color_idx]
    if variant == 'brick':
        return f'{BRICK_PREFIX[locale]} {color_name}'
    base = BASE_NOUN[locale]
    suffix = VARIANT_SUFFIX[locale][variant]
    if locale == 'fr_fr':
        # French: "Béton {variant} {color}" — adjective after noun
        return f'{base} {suffix} {color_name}'
    # Portuguese: "Concreto {color} {variant}"
    return f'{base} {color_name} {suffix}'


TOP_LEVEL = {
    'pt_br': {
        'itemGroup.betterconcretes': 'Better Concretes',
        'betterconcretes.tab': 'Better Concretes',
        'item.betterconcretes.chisel': 'Cinzel',
        'container.betterconcretes.chisel': 'Cinzel',
        'betterconcretes.jei.water_transform': 'Transformação por Água',
        'betterconcretes.jei.chisel': 'Cinzelagem',
        'betterconcretes.variant.vanilla': 'Padrão',
        'betterconcretes.variant.smooth': 'Liso',
        'betterconcretes.variant.chiseled': 'Esculpido',
        'betterconcretes.variant.polished': 'Polido',
        'betterconcretes.variant.brick': 'Tijolo',
    },
    'pt_pt': {
        'itemGroup.betterconcretes': 'Better Concretes',
        'betterconcretes.tab': 'Better Concretes',
        'item.betterconcretes.chisel': 'Cinzel',
        'container.betterconcretes.chisel': 'Cinzel',
        'betterconcretes.jei.water_transform': 'Transformação pela Água',
        'betterconcretes.jei.chisel': 'Cinzelagem',
        'betterconcretes.variant.vanilla': 'Padrão',
        'betterconcretes.variant.smooth': 'Liso',
        'betterconcretes.variant.chiseled': 'Cinzelado',
        'betterconcretes.variant.polished': 'Polido',
        'betterconcretes.variant.brick': 'Tijolo',
    },
    'fr_fr': {
        'itemGroup.betterconcretes': 'Better Concretes',
        'betterconcretes.tab': 'Better Concretes',
        'item.betterconcretes.chisel': 'Ciseau',
        'container.betterconcretes.chisel': 'Ciseau',
        'betterconcretes.jei.water_transform': 'Transformation par eau',
        'betterconcretes.jei.chisel': 'Ciselage',
        'betterconcretes.variant.vanilla': 'Vanille',
        'betterconcretes.variant.smooth': 'Lisse',
        'betterconcretes.variant.chiseled': 'Ciselé',
        'betterconcretes.variant.polished': 'Poli',
        'betterconcretes.variant.brick': 'Brique',
    },
}


def build(locale):
    out = dict(TOP_LEVEL[locale])
    for variant in VARIANTS:
        for i, color in enumerate(COLORS):
            key = f'block.betterconcretes.{variant}_{color}_concrete'
            out[key] = block_name(locale, variant, i)
    return out


def main():
    for locale in ['pt_br', 'pt_pt', 'fr_fr']:
        path = os.path.join(OUT_DIR, f'{locale}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(build(locale), f, ensure_ascii=False, indent=2)
        print(f'wrote {path}')


if __name__ == '__main__':
    main()
