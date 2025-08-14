import tcod.ecs

import g

from game.procgen import generate_map
from game.components import Position, Name
from game.queue import Queue
from game.entity_tools import add_to_inventory, equip, enter_level
from game.message_log import MessageLog, log
from game.features import place_staircase, place_door
from game.action import Action
from game.controller import Controller
from game.tags import IsActor
from game.text import Text


class AdvanceTime(Action):
    def execute(self, actor):
        g.registry[None].components[int] += 1

class Timekeeper(Controller):
    def __call__(self, actor):
        return AdvanceTime()

def world_init():
    g.registry = tcod.ecs.Registry()
    from game.templates import creatures, items

    g.registry[None].components[Queue] = Queue()
    g.registry[None].components[MessageLog] = MessageLog()
    g.registry[None].components[int] = 0  # Turn count
    
    log(Text('Welcome to the testing zone! This is a ridiculously long message to test the message log\'s word wrapping capabilities.'))

    map_shape = (60,60)
    map_ = generate_map(map_shape)

    g.player = creatures.PLAYER.spawn(Position(5,5,map_))
    g.player.components[Name] = g.player_name
    g.player_is_dead = False
    g.timekeeper = g.registry.new_entity(components={Controller: Timekeeper()}, tags=[IsActor, map_])

    creatures.MONSTER.spawn(Position(50,9,map_))
    creatures.MONSTER.spawn(Position(51,9,map_))
    creatures.MONSTER.spawn(Position(52,9,map_))
    creatures.MONSTER.spawn(Position(53,9,map_))
    
    add_to_inventory(items.POTION_OF_HEALTH_BOOST.spawn(quantity=3), g.player)
    add_to_inventory(items.POTION_OF_HEALTH_REGEN.spawn(quantity=3), g.player)
    items.POTION_OF_HEALTH_BOOST.spawn(Position(1,1,map_), quantity=4)
    items.SWORD.spawn(Position(2,2,map_))
    equip(add_to_inventory(items.SWORD.spawn(), g.player), g.player)

    map_2 = generate_map((5,5))
    place_staircase(Position(3,1,map_), Position(3,3,map_2))
    place_door(Position(10,10,map_))
    enter_level(map_)