from tcod.ecs import Entity

import g

from game.controller import Controller
from game.action import Action, MetaAction, PseudoAction
from game.components import Position, Name, Tiles, Attack, HP, OnConsume, ConsumeVerb, StaircaseDirection, OnInteract
from game.tags import IsCreature, CarriedBy, Equipped, ConnectsTo, IsBlocking
from game.tiles import TILES
from game.message_log import log
from game.entity_tools import add_to_inventory, drop, equip
from game.text import Text

import game.colors as colors


class Defer:
    '''Wait until the next non-deffered entity has taken an action.
    
    Useful if an actor wants to move into the position of another entity.'''
    def __call__(self, actor):
        assert actor == g.queue().front
        g.queue().defer_front()


class Directional(Action):
    def __init__(self, direction: tuple[int, int]):
        super().__init__()
        self.direction = direction
    def dest(self, actor):
        '''Return the result of applying the direction to the actor's position.'''
        return actor.components[Position] + self.direction
    def creature(self, actor):
        for e in g.registry.Q.all_of(tags=[self.dest(actor), IsCreature]): return e  # There should be only one creature occupying a tile
    def blocking_feature(self, actor):
        for e in g.registry.Q.all_of(tags=[self.dest(actor), IsBlocking], components=[OnInteract]): return e


class Bump(MetaAction, Directional):
    def __init__(self, direction: tuple[int, int]):
        super().__init__(direction)
    def execute(self, actor):
        creature = self.creature(actor)
        blocking_feature = self.blocking_feature(actor)
        if creature:
            Melee(creature)(actor)
        elif blocking_feature:
            InteractWithFeature(self.direction)(actor)
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
        damage = actor.components[Attack]
        message_color = colors.MSG_ATTACK if actor != g.player else colors.DEFAULT
        log(Text(f'{actor.components[Name]} attacks {self.target.components[Name]} for {damage} damage!', message_color))
        self.target.components[HP] -= damage


class ItemAction(Action):
    def __init__(self, item: Entity, cost=100):
        super().__init__(cost=cost)
        self.item = item

class PickupItem(ItemAction):
    def execute(self, actor):
        log(Text(f'{actor.components[Name]} picks up the {self.item.components[Name]}'))
        add_to_inventory(self.item, actor)

class DropItem(ItemAction):
    def execute(self, actor):
        log(Text(f'{self.item.relation_tag[CarriedBy].components[Name]} drops the {self.item.components[Name]}'))
        drop(self.item)

class EquipOrUnequipItem(ItemAction):
    def execute(self, actor):
        if Equipped in self.item.tags:
            self.item.tags.remove(Equipped)
            log(Text(f'{actor.components[Name]} unequips the {self.item.components[Name]}.'))
        else:
            equip(self.item, actor)
            log(Text(f'{actor.components[Name]} equips the {self.item.components[Name]}.'))

class ConsumeItem(ItemAction):
    def execute(self, actor):
        on_consume = self.item.components[OnConsume]
        log(Text(f'{actor.components[Name]} {self.item.components[ConsumeVerb]}s the {self.item.components[Name]}.'))
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
            log(Text(f'{actor.components[Name]} {"descends" if self.direction == 1 else "ascends"}.'))
        else:
            log(Text(f'There is no {"down" if self.direction == 1 else "up"} staircase here.'))
            return True

class InteractWithFeature(Directional):
    def execute(self, actor):
        for feature in g.registry.Q.all_of(tags=[self.dest(actor)], components=[OnInteract]):
            feature.components[OnInteract](feature, actor)
            return 
        else:
            log(Text('There is nothing to interact with there.', colors.MSG_FAILED_ACTION))
            return True


class Input(MetaAction):
    def __init__(self, string: str):
        self.string = string
    def execute(self, actor):
        g.state.input(self.string)
class Backspace(MetaAction):
    def execute(self, actor):
        g.state.backspace()

# Pseudo-actions handled in states.py


class ViewInventory(PseudoAction):
    pass

class MoveCursor(PseudoAction):
    def __init__(self, direction: int):
        self.direction = direction

class Select(PseudoAction):
    pass

class Exit(PseudoAction):
    pass

class PickupItemDispatch(PseudoAction):
    pass

class DropItems(PseudoAction):
    pass

class EquipOrUnequipItems(PseudoAction):
    pass

class ConsumeItems(PseudoAction):
    pass

class InteractWithFeatures(PseudoAction):
    pass

class BeginGame(PseudoAction):
    pass