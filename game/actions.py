import g

from game.action import Action
from game.components import Position, Tiles
from game.tags import IsCreature
from game.tiles import TILES


class Wait(Action):
    pass


class Directional(Action):
    def __init__(self, direction: tuple[int, int]):
        super().__init__()
        self.direction = direction
    def dest(self, actor):
        '''Return the result of applying the direction to the actor's position.'''
        return actor.components[Position] + self.direction
    def creature(self, actor):
        for e in g.registry.Q.all_of(tags=[self.dest(actor), IsCreature]): return e  # There should be only one creature occupying a tile


class Bump(Directional):
    def __init__(self, direction: tuple[int, int]):
        super().__init__(direction)
    def __call__(self, actor):
        self.execute(actor)
    def execute(self, actor):
        creature = self.creature(actor)
        if creature:
            Melee(creature)(actor)
        else:
            Move(self.direction)(actor)

class Move(Directional):
    def execute(self, actor):
        map_ = actor.components[Position].map_
        dest = self.dest(actor)
        if TILES['walk_cost'][map_.components[Tiles][dest.ij]] > 0:
            actor.components[Position] = dest

class Melee(Action):
    def __init__(self, target):
        self.target = target
        super().__init__()

    def execute(self, actor):
        pass