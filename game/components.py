import attrs
from tcod.ecs import Entity, callbacks
import numpy as np
from typing import Final
import g

from game.duration_effect import DurationEffect
from game.message_log import log
from game.text import Text
import game.colors as colors


@attrs.define
class Position:
    x: int
    y: int
    map_: Entity

    @property
    def ij(self):
        return self.y, self.x

    def __add__(self, other: tuple[int, int]):
        return self.__class__(self.x+other[0], self.y+other[1], self.map_)

    def __sub__(self, other: tuple[int, int]):
        return self.__class__(self.x-other[0], self.y-other[1], self.map_)

    def __hash__(self):
        return hash((self.x, self.y))


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Tiles: Final = ('Tiles', np.ndarray)
VisibleTiles: Final = ('VisibleTiles', np.ndarray)
MemoryTiles: Final = ('MemoryTiles', np.ndarray)
MapShape: Final = ('MapShape', tuple[int, int])


Name: Final = ('Name', str)
Description: Final = ('Description', str)

MaxHP: Final = ('MaxHP', int)
HP: Final = ('HP', int)
Attack: Final = ('Attack', int)

Quantity: Final = ('Quantity', int)
ItemCategory: Final = ('ItemCategory', int)
ITEM_CATEGORIES: Final = [
    'weapons',
    'armor',
    'potions',
    'scrolls',

    'equipped'  # Last slot is reserved for equipment; actually rendered first
]

EquipmentSlot: Final = ('EquipmentSlot', str)

class OnConsume:
    def __call__(self, consumed: Entity, affecting: Entity):
        self.affect(affecting)
        if consumed.components[Quantity] > 1:
            consumed.components[Quantity] -= 1
        else:
            consumed.clear()

    def affect(self, actor: Entity):
        log(Text(f'Nothing happens to {actor.components[Name]}.', colors.MSG_FAILED_ACTION))

ConsumeVerb: Final = ('ConsumeVerb', str)

class DurationEffects:
    def __init__(self):
        self.effects: list[DurationEffect] = []
    def add(self, effect: DurationEffect):
        self.effects.append(effect)
    def __call__(self, actor):
        new_effects = []
        for i, effect in enumerate(self.effects):
            if effect(actor):  # Execute effect
                new_effects.append(effect)
        self.effects = new_effects
        if self.effects:
            return True
        return False

StaircaseDirection: Final = ('StaircaseDirection', int)


class OnInteract:
    def __call__(self, feature: Entity, actor: Entity):
        pass