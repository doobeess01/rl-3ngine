from tcod.ecs import Entity, callbacks, IsA
from typing import Iterable

import g

from game.components import Position, Name, HP, MaxHP, Quantity, EquipmentSlot, DurationEffects
from game.tags import IsCreature, IsActor, IsStackable, CarriedBy, Equipped, IsTimekeeper
from game.controller import Controller
from game.action import Action
from game.message_log import log
from game.duration_effect import DurationEffect
from game.text import Text
import game.colors as colors



# Creature tools

def kill(actor: Entity):
    log(Text(f'{actor.components[Name]} dies!', colors.MSG_DEATH))
    if actor == g.player:
        g.player_is_dead = True
        g.queue().clear()
        g.queue().add(g.player)
        log(Text('Press SPACE to accept your fate...', colors.MSG_DEATH))
    else:
        g.queue().remove(actor)
        actor.clear()

def give_duration_effect(actor: Entity, effect: DurationEffect):
    if not actor.components.get(DurationEffects, 0):
        actor.components[DurationEffects] = DurationEffects()
    actor.components[DurationEffects].add(effect)


# Item tools

def inventory(entity: Entity):
    '''
    Return the inventory of an entity (all items with the IsIn relation to it)
    '''
    return g.registry.Q.all_of(relations=[(CarriedBy, entity)])

def add_to_inventory(item: Entity, actor: Entity):
    '''
    Add an item to an entity's inventory. This modifies the entities' CarriedBy relation.
    '''
    stackable_inventory = list(inventory(actor).all_of(tags=[IsStackable]))
    for other_item in stackable_inventory:
        if other_item.relation_tag[IsA] == item.relation_tag[IsA]:
            other_item.components[Quantity] += item.components[Quantity]
            item.clear()
            return other_item
    item.relation_tag[CarriedBy] = actor
    if item.components.get(Position, 0):
        del item.components[Position]
    return item

def drop(item: Entity):
    position = item.relation_tag[CarriedBy].components[Position]
    quantity = item.components[Quantity]
    if Equipped in item.tags:
        item.tags.remove(Equipped)
    for e in g.registry.Q.all_of(tags=[position, IsStackable], relations=[(IsA, item.relation_tag[IsA])]):
        # If there is an identical stackable item on the same square, add to its quantity
        e.components[Quantity] += quantity
        item.clear()
        return e
    else:
        item.components[Position] = position
        del item.relation_tag[CarriedBy]
        return item

def equip(item: Entity, actor: Entity):
    slot = item.components[EquipmentSlot]
    for equipped_item in list(inventory(actor).all_of(components=[EquipmentSlot], tags=[Equipped])):
        if slot == equipped_item.components[EquipmentSlot]:
            equipped_item.tags.remove(Equipped)
    item.tags.add(Equipped)


def enter_level(map_: Entity):
    if g.queue().queue:
        if g.queue().front == g.timekeeper:
            g.timekeeper.components[Controller](g.timekeeper)(g.timekeeper)
    g.queue().clear()
    for e in g.registry.Q.all_of(tags=[map_, IsActor]):
        if e not in (g.player,g.timekeeper):
            g.queue().add(e)
    g.queue().add(g.player)
    g.queue().add(g.timekeeper)


@callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    '''Set Position and map_ tags for easy lookup by-position and by-map.'''
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

@callbacks.register_component_changed(component=int)
def on_time_advance(entity: Entity, old: int | None, new: int | None) -> None:
    assert entity == entity.registry[None]  # Only the registry should have a time component
    if old:
        for e in g.registry.Q.all_of(components=[DurationEffects]):
            if not e.components[DurationEffects](e):
                del e.components[DurationEffects]