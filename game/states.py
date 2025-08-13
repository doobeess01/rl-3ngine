import copy

from tcod.event import KeyDown, KeySym as K
from tcod.ecs import Entity

import g

from game.action import Action, MetaAction, PseudoAction, Pass
from game.state import State
from game.rendering import render_map, render_message_log, render_sidebar
from game.components import Position, Graphic, Name, Quantity, ItemCategory, ITEM_CATEGORIES, EquipmentSlot, HP, MaxHP, OnConsume, DurationEffects
from game.tags import IsItem, Equipped
from game.actions import (
    BeginGame,
    MoveCursor, Select,
    Exit,
    ViewInventory, 
    PickupItem, PickupItemDispatch, 
    DropItem, DropItems, 
    EquipOrUnequipItem, EquipOrUnequipItems,
    ConsumeItem, ConsumeItems,
    InteractWithFeature, InteractWithFeatures,
)
from game.text import Text
from game.entity_tools import inventory
from game.message_log import log
from game.world_init import world_init
import game.keybindings as keybindings
import game.colors as colors


class State(State):
    '''Base state that includes pseudo-action handling.'''

    def execute_pseudo_action(self, action: PseudoAction): 
        match action:
            case BeginGame():
                g.state = PlayerNameInput()
            case ViewInventory():
                self.enter_substate(ViewInventoryMenu())
            case PickupItemDispatch():
                items = PickupItemsMenu().get_items()
                if len(items) > 1:
                    self.enter_substate(PickupItemsMenu())
                elif items:
                    return PickupItem(items[0])
                else:
                    log(Text('There is nothing to pick up here.', colors.MSG_FAILED_ACTION))
            case DropItems():
                self.enter_substate(DropItemsMenu())
            case EquipOrUnequipItems():
                self.enter_substate(EquipOrUnequipItemMenu())
            case ConsumeItems():
                self.enter_substate(ConsumeItemsMenu())
            case InteractWithFeatures():
                self.enter_substate(
                    DirectionSelect(InteractWithFeature, message=Text('Interact in which direction?', colors.MSG_DIRECTION_SELECT)), 
                )
            case MoveCursor():
                self.move_cursor(action.direction)
            case Select():
                self.select()
            case Exit():
                self.exit()
            case _:
                print(f'WARNING: Attempted to execute unimplemented PseudoAction {action.__class__.__name__}')


class Menu(State):
    def __init__(self):
        super().__init__(keybindings.MENU)
        self.options = self.get_options()
        self.cursor = 0
                
    def move_cursor(self, direction: int):
        self.cursor = len(self.options)-1 if not self.cursor+direction+1 else 0 if self.cursor+direction-1 == len(self.options)-1 else self.cursor+direction
    
    def select(self):
        action = self.options[self.cursor][1]
        action(g.player)
        if hasattr(action, 'cost'):
            g.state = InGame()
        else:
            self.options = self.get_options()
            if self.cursor >= len(self.options):
                self.cursor = len(self.options)-1
    
    def get_options(self) -> list[tuple[Text, Action]]:
        '''Return a list of (Text, Action) tuple pairs representing the options in the menu.'''
        return []
    
    def get_texts(self):
        return [option[0] for option in self.options]


class MainMenu(Menu):
    def get_options(self):
        return [
            (Text('Play', colors.MAIN_MENU), BeginGame()),
            (Text('Quit', colors.MAIN_MENU), Exit()),
        ]
    def on_draw(self):
        Text('UNTITLED RL').print(3,3)
        for i,text in enumerate(self.get_texts()):
            printed_text = copy.deepcopy(text) 
            printed_text.string = ('> ' if self.cursor == i else '  ') + text.string
            printed_text.print(1,20+i*2)


class PlayerNameInput(State):
    def __init__(self):
        super().__init__(keybindings.TEXT_INPUT)
        self.text = g.player_name
        self.confirm_prompt = False
    def on_event(self, event):
        if self.confirm_prompt:
            match event:
                case KeyDown(sym=K.Y):
                    g.player_name = self.text
                    world_init()
                    g.state = InGame()
                case KeyDown(K.N):
                    self.confirm_prompt = False
        else:
            return super().on_event(event)
    def input(self, letter: str):
        self.text += letter
    def backspace(self):
        self.text = self.text[:-1]
    def select(self):
        self.confirm_prompt = True
    def on_draw(self):
        Text(f'Name: {self.text}').print(1,1)
        Text(f'Play as {self.text}? (y/n)' if self.confirm_prompt else 'Press ENTER to confirm', colors.PROMPT).print(1,3)


def sort_items(items: list[Entity]) -> dict[int: list[Entity]]:
    '''Returns a dictionary of sorted items by ItemCategory.'''
    sorted_items = {}
    for item in items:
        category = -1 if Equipped in item.tags else item.components[ItemCategory]
        if sorted_items.get(category, 0):
            sorted_items[category].append(item)
        else:
            sorted_items[category] = [item]
    return sorted_items


class ItemList(Menu):
    def __init__(self, title: str, action: Action | MetaAction = Pass, no_items_text = '[No items]'):
        self.title = title
        self.action = action
        self.no_items_text = no_items_text
        self.items = []
        super().__init__()

    def add_option_for_item(self, item: Entity, options: list):
        name = item.components[Name]
        quantity = item.components[Quantity]
        graphic = item.components[Graphic]
        options.append((
            Text(name+(f' (x{quantity})' if quantity > 1 else '')+(' (equipped)' if Equipped in item.tags else ''), (graphic.fg, graphic.bg)),
            self.action(item)
        ))
        self.items.append(item)
        return options

    def get_options(self) -> list[tuple[Text, Action]]:
        options = []
        items = self.get_items()
        if items:
            # Sort items by category
            sorted_items = sort_items(items)

            # Add options
            for category in sorted(sorted_items.keys()):
                if category == -1:
                    sorted_equipped_items = sort_items(sorted_items[category])
                    for category in sorted(sorted_equipped_items.keys()):
                        for item in sorted_equipped_items[category]:
                            self.add_option_for_item(item, options)
                else:
                    for item in sorted_items[category]:
                        self.add_option_for_item(item, options)

        return options
    
    def get_items(self):
        return []
    
    def on_draw(self):
        fg, bg = colors.DEFAULT
        g.console.print(0,0,self.title,fg=fg,bg=bg)
        line_counter = 1
        if self.options:
            for i,option in enumerate(self.options):
                item = self.items[i]
                previous_item = self.items[i-1]
                category = -1 if Equipped in item.tags else item.components[ItemCategory]
                previous_category = -1 if Equipped in previous_item.tags else previous_item.components[ItemCategory]
                if category != previous_category or i==0:
                    line_counter += 1
                    g.console.print(0,line_counter,f'-- {ITEM_CATEGORIES[category]} --', fg=colors.PURPLE, bg=colors.BLACK)
                    line_counter += 2

                option[0].print(1,line_counter, invert=True if i==self.cursor else False)
                line_counter += 1
        else:
            g.console.print(0,2,self.no_items_text)


class ViewInventoryMenu(ItemList):
    def __init__(self):
        super().__init__(
            title='Inventory', 
            action=Pass, 
            no_items_text='You are carrying nothing.'
        )
    def get_items(self):
        return inventory(g.player)


class PickupItemsMenu(ItemList):
    def __init__(self):
        super().__init__(
            title='Pick up which?',
            action=PickupItem,
        )
    def get_items(self):
        return [e for e in g.registry.Q.all_of(tags=[g.player.components[Position], IsItem])]


class DropItemsMenu(ItemList):
    def __init__(self):
        super().__init__(
            title='Drop which?',
            action=DropItem,
            no_items_text='You are carrying nothing.'
        )
    def get_items(self):
        return inventory(g.player)


class EquipOrUnequipItemMenu(ItemList):
    def __init__(self):
        super().__init__(
            title='Equip/unequip which?',
            action=EquipOrUnequipItem,
            no_items_text='You have nothing to equip or unequip.'
        )
    def get_items(self):
        return inventory(g.player, components=[EquipmentSlot])

class ConsumeItemsMenu(ItemList):
    def __init__(self):
        super().__init__(
            title='Use which?',
            action=ConsumeItem,
            no_items_text='You have nothing to use.'
        )
    def get_items(self):
        return inventory(g.player, components=[OnConsume])


class InGame(State):
    def __init__(self):
        super().__init__(keybindings.IN_GAME)

    def on_draw(self):
        player_pos = g.player.components[Position]
        map_view_shape = (39,39)
        render_map(map_=player_pos.map_, screen_shape=map_view_shape, center=player_pos.ij)
        render_message_log((0,map_view_shape[0]+1), g.console.height-map_view_shape[0]-1)
        effect_texts = []
        if g.player.components.get(DurationEffects, 0):
            effect_texts = [effect.text for effect in g.player.components[DurationEffects].effects]
        render_sidebar((map_view_shape[1]+1,0), lines=[
            Text(g.player.components[Name]),
            Text(f'HP: {g.player.components[HP]}/{g.player.components[MaxHP]}'),
            None,
            Text(f'Turns: {g.registry[None].components[int]}'),
            None,
            *effect_texts,
        ])


class DirectionSelect(State):
    def __init__(self, action, message: Text = Text('In which direction?')):
        super().__init__(keybindings=keybindings.DIRECTION_SELECT)
        self.action = action
        self.message = message
        log(self.message)
    def exit(self, report = True):
        super().exit()
        if report:
            log(Text('Never mind.', colors.MSG_FAILED_ACTION))
    def on_draw(self):
        InGame().on_draw()


class GameOver(State):
    def on_draw(self):
        g.console.print(0,0,'Game over')