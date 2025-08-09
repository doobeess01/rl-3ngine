import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position
from game.tags import IsActor
from game.queue import Queue
from game.entity_tools import spawn_creature
from game.message_log import MessageLog, log


def world_init():
    g.registry = tcod.ecs.Registry()
    from game.templates import creatures

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog()
    
    log('Welcome to the testing zone!')

    map_shape = (60,60)
    map_ = generate_map(map_shape)

    g.player = spawn_creature(creatures.PLAYER, Position(5,5,map_))
    monster = spawn_creature(creatures.MONSTER, Position(50,50,map_))
    
    enter_level(map_)


def enter_level(map_: tcod.ecs.Entity):
    for e in g.registry.Q.all_of(tags=[map_, IsActor]):
        if e != g.player:
            g.queue().add(e)
    g.queue().add(g.player)