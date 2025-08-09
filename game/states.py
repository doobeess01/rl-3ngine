from tcod.event import KeyDown, Quit

import g

from game.action import Action, Pass
from game.state import State
from game.rendering import render_map, render_message_log
from game.components import Position, Graphic, Name, Quantity, ItemCategory, ITEM_CATEGORIES
from game.actions import ViewInventory, MoveCursor, Select, Exit
from game.text import Text
from game.entity_tools import inventory
import game.keybindings as keybindings
import game.colors as colors


class Menu(State):
    def __init__(self):
        super().__init__(keybindings.MENU)
        self.options = self.get_options()
        self.cursor = 0

    def on_event(self, event):
        action = super().on_event(event)

        match action:
            case None:
                pass
            case MoveCursor():
                self.move_cursor(action.direction)
            case Select():
                self.select()
            case Exit():
                self.exit()
            case _:
                return action
                
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


class ItemList(Menu):
    def __init__(self, title: str, action: Action = Pass, no_items_text = '[No items]'):
        self.title = title
        self.action = action
        self.no_items_text = no_items_text
        self.items = self.get_items()
        super().__init__()

    def get_options(self) -> list[tuple[Text, Action]]:
        options = []
        items = self.get_items()
        if items:
            sorted_items = {}
            # Sort items by category
            for item in items:
                category = item.components[ItemCategory]
                if sorted_items.get(category, 0):
                    sorted_items[category].append(item)
                else:
                    sorted_items[category] = [item]
            # Add options
            for i in range(max(sorted_items)):
                if sorted_items.get(i+1, 0):
                    for item in sorted_items[i+1]:
                        name = item.components[Name]
                        quantity = item.components[Quantity]
                        graphic = item.components[Graphic]
                        options.append((
                            Text(name+(f' (x{quantity})' if quantity > 1 else ''), graphic.fg, graphic.bg),
                            self.action(item)
                        ))
                        self.items.append(item)
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
                category = item.components[ItemCategory]
                previous_category = previous_item.components[ItemCategory]
                if category != previous_category or i==0:
                    line_counter += 1
                    g.console.print(0,line_counter,f'-- {ITEM_CATEGORIES[category]} --', fg=colors.PURPLE, bg=colors.BLACK)
                    line_counter += 2

                option[0].print(1,line_counter, invert=True if i==self.cursor else False)
                line_counter += 1
        else:
            g.console.print(0,2,self.no_items_text)


class Inventory(ItemList):
    def __init__(self):
        super().__init__(
            title='Inventory', 
            action=Pass, 
            no_items_text='You are carrying nothing.'
        )
    def get_items(self):
        return inventory(g.player)


class InGame(State):
    def __init__(self):
        super().__init__(keybindings.IN_GAME)

    def on_event(self, event):
        action = super().on_event(event)

        if action:
            match action:
                case ViewInventory():
                    self.enter_substate(Inventory())
                case _:
                    return action

    def on_draw(self):
        player_pos = g.player.components[Position]
        map_view_shape = (26,26)
        render_map(map_=player_pos.map_, screen_shape=map_view_shape, center=player_pos.ij)
        render_message_log((0,map_view_shape[0]+1), g.console.height-map_view_shape[0]-1)
            