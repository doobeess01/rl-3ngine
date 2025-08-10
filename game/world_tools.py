import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position
from game.tags import IsActor, IsTimekeeper
from game.queue import Queue
from game.entity_tools import spawn_creature, spawn_item, add_to_inventory, equip
from game.message_log import MessageLog, log
from game.controller import Controller
from game.action import Action


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

    enter_level(map_)


class AdvanceTime(Action):
    def execute(self, actor):
        g.registry[None].components[int] += 1
class Timekeeper(Controller):
    def __call__(self, actor):
        return AdvanceTime()
        

def enter_level(map_: tcod.ecs.Entity):
    g.queue().clear()
    for e in g.registry.Q.all_of(tags=[map_, IsActor]).none_of(tags=[IsTimekeeper]):
        if e != g.player:
            g.queue().add(e)
    g.queue().add(g.player)
    g.queue().add(g.registry.new_entity(components={Controller: Timekeeper()}, tags=[IsActor, map_]))