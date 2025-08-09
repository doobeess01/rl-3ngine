from tcod.ecs import Entity, callbacks
from typing import Iterable

import g

from game.components import Position, Name, HP, MaxHP
from game.tags import IsCreature, IsActor
from game.message_log import log
import game.colors as colors

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

def kill(actor: Entity):
    g.queue().remove(actor)
    log(f'{actor.components[Name]} dies!', colors.MSG_DEATH)
    actor.clear()


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

@callbacks.register_component_changed(component=HP)
def on_hp_change(entity: Entity, old: int | None, new: int | None):
    if new is not None:
        if new < 1:
            kill(entity)
        elif new > entity.components[MaxHP]:
            entity.components[HP] = entity.components[MaxHP]