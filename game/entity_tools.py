from tcod.ecs import Entity
from typing import Iterable

from game.components import Position
from game.tags import IsCreature, IsActor

def spawn_entity(template: Entity, position: Position, components: dict = {}, tags: set = {}):
    e = template.instantiate()
    e.components |= {Position: position}|components
    e.tags |= tags
    return e

def spawn_creature(template: Entity, position: Position, components: dict = {}, tags: set = {}) -> Entity:
    creature = spawn_entity(template, position=position, components=components, tags=tags)
    creature.tags.add(IsCreature)
    creature.tags.add(IsActor)
    return creature