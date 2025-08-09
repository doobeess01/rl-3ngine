import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position
from game.tags import IsActor
from game.queue import Queue
from game.entity_tools import spawn_creature, spawn_item, add_to_inventory
from game.message_log import MessageLog, log


def world_init():
    g.registry = tcod.ecs.Registry()
    from game.templates import creatures, items

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog()
    
    log('Welcome to the testing zone!')

    map_shape = (60,60)
    map_ = generate_map(map_shape)

    g.player = spawn_creature(creatures.PLAYER, Position(5,5,map_))
    g.player_is_dead = False
    monster = spawn_creature(creatures.MONSTER, Position(50,50,map_))

    add_to_inventory(spawn_item(items.POTION, quantity=3), g.player)
    spawn_item(items.POTION, Position(1,1,map_), quantity=4)
    spawn_item(items.SWORD, Position(2,2,map_))
    spawn_item(items.SWORD, Position(3,3,map_))

    enter_level(map_)


def enter_level(map_: tcod.ecs.Entity):
    g.queue().clear()
    for e in g.registry.Q.all_of(tags=[map_, IsActor]):
        if e != g.player:
            g.queue().add(e)
    g.queue().add(g.player)