import g

from game.components import Graphic, Name, Description, ItemCategory, EquipmentSlot, OnConsume, ConsumeVerb
from game.tags import IsStackable, IsItem
from game.consumable_effects import BoostHP, RegenHP

import game.colors as colors

def new_item(
        category: int = None,
        name: str = 'unknown', 
        desc: str = "[No description]", 
        graphic: Graphic = None, 
        stackable: bool = True,
        components: dict = {}, 
        tags: set = {},
        ):

    item = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc, ItemCategory: category,}|components,
        tags = tags,
    )
    item.tags.add(IsItem)
    if stackable:
        item.tags.add(IsStackable)
    return item

def new_consumable(
        name: str = 'unnamed consumable',
        desc: str = '[No description]',
        graphic: Graphic = Graphic(ord('?'), colors.WHITE, colors.BLACK),
        on_consume: OnConsume = OnConsume(),
        consume_verb: str = 'consume',
        components: dict = {},
        tags: set = {},
        ):  
    return new_item(
        name = name,
        desc = desc,
        graphic = graphic,
        category = 2,
        components = {OnConsume: on_consume, ConsumeVerb: consume_verb}|components,
        tags = tags,
    )

def new_potion(
        name: str = 'unnamed potion',
        desc: str = '[No description]',
        colors: tuple[tuple[int,int,int],tuple[int,int,int]] = (colors.LIGHT_BLUE, colors.BLACK),
        on_consume: OnConsume = OnConsume(),
        components: dict = {},
        tags: set = {},
        ):
    return new_consumable(
        name = name,
        desc = desc,
        graphic = Graphic(ord('!'), *colors),
        on_consume = on_consume,
        consume_verb = 'drink',
        components = components,
        tags = tags
    )


SWORD = new_item(
    category = 0,
    name = 'sword',
    graphic = Graphic(ord('/'), colors.DARK_PURPLE, colors.BLACK),
    desc = 'a sword.',
    stackable=False,
    components = {EquipmentSlot: 'weapon'},
)

POTION_OF_HEALTH_BOOST = new_potion(
    name = 'potion of health boost',
    desc = 'A potion. Restores a small amount of HP when consumed.',
    on_consume = BoostHP(5),
)
POTION_OF_HEALTH_REGEN = new_potion(
    name = 'potion of health regeneration',
    desc = 'A potion. Restores a small amount of HP when consumed.',
    on_consume = RegenHP(2, 5),
)

SCROLL = new_item(
    category = 3,
    name = 'scroll',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'A scroll.',
)