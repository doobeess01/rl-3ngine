import attrs
from tcod.ecs import Entity, callbacks
import numpy as np
from typing import Final


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

    def __iter__(self):
        return (self.x, self.y)
    
@callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    '''Aesthetically pleasing means of finding entity at any given coordinate.'''
    if old == new:
        return
    if old:
        entity.tags.remove(old)
        entity.tags.remove(old.map_)
    if new:
        entity.tags.add(new)
        entity.tags.add(new.map_)


@attrs.define
class Graphic:
    ch: int
    fg: tuple[int, int, int]
    bg: tuple[int, int, int] = (0,0,0)


Tiles: Final = ('Tiles', np.ndarray)
MapShape: Final = ('MapShape', tuple[int, int])