from tcod.ecs import IsA

import g

from game.templates.template import Template
from game.components import Position, Graphic, ItemCategory, EquipmentSlot, OnConsume, ConsumeVerb, Quantity
from game.tags import IsStackable, IsItem
from game.consumable_effects import BoostHP, RegenHP

import game.colors as colors


class Item(Template):
    def __init__(
            self,
            name: str = 'unknown', 
            desc: str = "[No description]", 
            graphic: Graphic = None, 
            category: int = None,
            stackable: bool = True,
            components: dict = {}, 
            tags: set = {},
            ):
        super().__init__(
            name = name,
            desc = desc,
            graphic = graphic,
            components = {
                ItemCategory: category,
            }|components,
            tags = tags,
        )
        self.template.tags.add(IsItem)
        if stackable:
            self.template.tags.add(IsStackable)
    def spawn(self, position: Position = None, quantity: int = 1, components: dict = {}, tags: set = {}):
        if quantity:
            if position:
                for e in g.registry.Q.all_of(tags=[position, IsStackable], relations=[(IsA, self.template)]):
                    # If there is an identical stackable item on the same square, add to its quantity
                    e.components[Quantity] += quantity
                    return e
            else:
                return super().spawn(position, components|{Quantity: quantity}, tags)


class Consumable(Item):
    def __init__(
            self,
            name: str = 'unnamed consumable',
            desc: str = '[No description]',
            graphic: Graphic = Graphic(ord('?'), colors.WHITE, colors.BLACK),
            category: int = 2,
            on_consume: OnConsume = OnConsume(),
            consume_verb: str = 'consume',
            components: dict = {},
            tags: set = {},
            ):  
        super().__init__(
            name = name,
            desc = desc,
            graphic = graphic,
            category = category,
            components = {OnConsume: on_consume, ConsumeVerb: consume_verb}|components,
            tags = tags,
        )

class Potion(Consumable):
    def __init__(
            self,
            name: str = 'unnamed potion',
            desc: str = '[No description]',
            on_consume: OnConsume = OnConsume(),
            colors: tuple[tuple[int,int,int],tuple[int,int,int]] = (colors.LIGHT_BLUE, colors.BLACK),
            components: dict = {},
            tags: set = {},
            ):
        super().__init__(
            name = name,
            desc = desc,
            graphic = Graphic(ord('!'), *colors),
            on_consume = on_consume,
            consume_verb = 'drink',
            components = components,
            tags = tags
        )


SWORD = Item(
    category = 0,
    name = 'sword',
    graphic = Graphic(ord('/'), colors.DARK_PURPLE, colors.BLACK),
    desc = 'a sword.',
    stackable=False,
    components = {EquipmentSlot: 'weapon'},
)

POTION_OF_HEALTH_BOOST = Potion(
    name = 'potion of health boost',
    desc = 'A potion. Restores a small amount of HP when consumed.',
    on_consume = BoostHP(5),
)

POTION_OF_HEALTH_REGEN = Potion(
    name = 'potion of health regeneration',
    desc = 'A potion. Restores a small amount of HP when consumed.',
    on_consume = RegenHP(2, 5),
)

SCROLL = Item(
    category = 3,
    name = 'scroll',
    graphic = Graphic(ord('?'), colors.LIGHT_BLUE, colors.BLACK),
    desc = 'A scroll.',
)