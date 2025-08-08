from tcod.event import KeyDown, Quit

import g

from game.state import State
from game.rendering import render_map
from game.components import Position
import game.keybindings as keybindings


class InGame(State):
    def __init__(self):
        super().__init__(keybindings.IN_GAME)

    def on_event(self, event):
        action = super().on_event(event)

        if action:
            match action:
                # Any actions that deal with states will be executed here

                case _:
                    action(g.player)

    def on_draw(self):
        player_pos = g.player.components[Position]
        map_view_shape = (39,39)
        render_map(map_=player_pos.map_, screen_shape=map_view_shape, center=player_pos.ij)
            