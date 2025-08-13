import random

import g

from game.controller import Controller
from game.action import Wait
from game.actions import Bump, Defer
from game.tiles import TILES
from game.components import Position, Tiles
from game.tags import IsCreature
from game.travel import path_to


class Wander(Controller):
    def __call__(self, actor):
        directions = [(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1)]
        map_ = actor.components[Position].map_
        while directions:
            direction = random.choice(directions)
            directions.remove(direction)
            new_position = actor.components[Position] + direction
            blocking_entities = [e for e in actor.registry.Q.all_of(tags=[IsCreature, actor.components[Position]+direction])]
            if TILES['walk_cost'][map_.components[Tiles][new_position.ij]]>0 and not blocking_entities:
                return Bump(direction)
        return Defer()


class Hostile(Controller):
    def __call__(self, actor):
        player_pos = g.player.components[Position]
        path = path_to(actor, player_pos)
        if path:
            dest = path[0]
            action = Bump((dest.x - actor.components[Position].x, dest.y-actor.components[Position].y))
            creature = action.creature(actor)
            if creature != g.player and creature is not None:
                return Defer()
            return action
        else:
            return Wander()(actor)