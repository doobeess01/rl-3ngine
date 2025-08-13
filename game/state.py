from tcod.event import Event, KeyDown, Quit, Modifier

import g

from game.action import Action


class State:
    def __init__(self, keybindings = {}):
        self.keybindings = keybindings
        self.parent = None

    def on_event(self, event: Event) -> Action:
        action = None
        match event:
            case KeyDown(sym=sym, mod=mod):
                if (Modifier.SHIFT, sym) in self.keybindings and (mod & Modifier.SHIFT):
                    action = self.keybindings[(Modifier.SHIFT, sym)]
                elif sym in self.keybindings:
                    action = self.keybindings[sym]
            case Quit():
                raise SystemExit
        return action

    def on_draw(self):
        pass

    def exit(self):
        if self.parent:
            g.state = self.parent
        else:
            raise SystemExit

    def enter_substate(self, state):
        parent = g.state
        g.state = state
        g.state.parent = parent