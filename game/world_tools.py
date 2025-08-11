import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position
from game.queue import Queue
from game.entity_tools import spawn_creature, spawn_item, add_to_inventory, equip, enter_level
from game.message_log import MessageLog, log
from game.staircase import place_staircase


def world_init():
    g.registry = tcod.ecs.Registry()
    from game.templates import creatures, items

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog()
    g.registry[None].components[int] = 0  # Turn count
    
    log('Welcome to the testing zone!')

    map_shape = (60,60)
    map_ = generate_map(map_shape)

    g.player = spawn_creature(creatures.PLAYER, Position(5,5,map_))
    g.player_is_dead = False
    monster = spawn_creature(creatures.MONSTER, Position(50,50,map_))

    add_to_inventory(spawn_item(items.POTION_OF_HEALTH_BOOST, quantity=3), g.player)
    add_to_inventory(spawn_item(items.POTION_OF_HEALTH_REGEN, quantity=3), g.player)
    spawn_item(items.POTION_OF_HEALTH_BOOST, Position(1,1,map_), quantity=4)
    spawn_item(items.SWORD, Position(2,2,map_))
    equip(add_to_inventory(spawn_item(items.SWORD), g.player), g.player)

    map_2 = generate_map((5,5))
    place_staircase(Position(3,1,map_), Position(3,3,map_2))
    enter_level(map_)