from tcod.ecs import Entity

import g

from game.action import Action, MetaAction
from game.components import Position, Name, Tiles, UnarmedAttack, HP, OnConsume, ConsumeVerb, StaircaseDirection
from game.tags import IsCreature, CarriedBy, Equipped, ConnectsTo
from game.tiles import TILES
from game.message_log import log
from game.entity_tools import add_to_inventory, drop, equip

import game.colors as colors


class Directional(Action):
    def __init__(self, direction: tuple[int, int]):
        super().__init__()
        self.direction = direction
    def dest(self, actor):
        '''Return the result of applying the direction to the actor's position.'''
        return actor.components[Position] + self.direction
    def creature(self, actor):
        for e in g.registry.Q.all_of(tags=[self.dest(actor), IsCreature]): return e  # There should be only one creature occupying a tile


class Bump(MetaAction, Directional):
    def __init__(self, direction: tuple[int, int]):
        super().__init__(direction)
    def execute(self, actor):
        creature = self.creature(actor)
        if creature:
            Melee(creature)(actor)
        else:
            Move(self.direction)(actor)

class Move(Directional):
    def execute(self, actor):
        map_ = actor.components[Position].map_
        dest = self.dest(actor)
        if TILES['walk_cost'][map_.components[Tiles][dest.ij]] > 0:
            actor.components[Position] = dest


class Melee(Action):
    def __init__(self, target):
        self.target = target
        super().__init__()

    def execute(self, actor):
        damage = actor.components[UnarmedAttack]
        message_color = colors.MSG_ATTACK if actor != g.player else colors.DEFAULT
        log(f'{actor.components[Name]} attacks {self.target.components[Name]} for {damage} damage!', message_color)
        self.target.components[HP] -= damage


class ItemAction(Action):
    def __init__(self, item: Entity, cost=100):
        super().__init__(cost=cost)
        self.item = item

class PickupItem(ItemAction):
    def execute(self, actor):
        log(f'{actor.components[Name]} picks up the {self.item.components[Name]}')
        add_to_inventory(self.item, actor)

class DropItem(ItemAction):
    def execute(self, actor):
        log(f'{self.item.relation_tag[CarriedBy].components[Name]} drops the {self.item.components[Name]}')
        drop(self.item)

class EquipOrUnequipItem(ItemAction):
    def execute(self, actor):
        if Equipped in self.item.tags:
            self.item.tags.remove(Equipped)
            log(f'You unequip the {self.item.components[Name]}.')
        else:
            equip(self.item, actor)
            log(f'You equip the {self.item.components[Name]}.')

class ConsumeItem(ItemAction):
    def execute(self, actor):
        on_consume = self.item.components[OnConsume]
        log(f'You {self.item.components[ConsumeVerb]} the {self.item.components[Name]}.')
        on_consume(self.item, actor)


class UseStairs(Action):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
    def execute(self, actor):
        from game.entity_tools import enter_level
        staircase = [e for e in g.registry.Q.all_of(components=[StaircaseDirection], tags=[actor.components[Position]]) if e.components[StaircaseDirection] == self.direction]
        if staircase:
            actor.components[Position] = staircase[0].relation_tag[ConnectsTo].components[Position]
            enter_level(actor.components[Position].map_)
            log(f'You {"descend" if self.direction == 1 else "ascend"}.')
        else:
            log(f'There is no {"down" if self.direction == 1 else "up"} staircase here.')


# Pseudo-actions handled in states.py

class ViewInventory:
    pass

class MoveCursor:
    def __init__(self, direction: int):
        self.direction = direction

class Select:
    pass

class Exit:
    pass

class PickupItemDispatch:
    pass

class DropItems:
    pass

class EquipOrUnequipItems:
    pass

class ConsumeItems:
    pass