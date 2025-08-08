import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position, Graphic
from game.queue import Queue

import game.colors as colors

def world_init():
    g.registry = tcod.ecs.Registry()

    queue = g.registry[None].components[Queue] = Queue()

    map_shape = (60,60)
    map_ = generate_map(map_shape)

    g.player = g.registry.new_entity(components={
        Position: Position(5,5,map_),
        Graphic: Graphic(ord('@'), colors.WHITE)
    })
    queue.add(g.player)