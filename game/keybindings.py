from tcod.event import KeySym as K, Modifier as M

from game.action import Wait
from game.actions import *


DIRECTIONS = {
    K.UP: (0,-1),
    K.N8: (0,-1),

    K.N9: (1,-1),

    K.RIGHT: (1,0),
    K.N6: (1,0),

    K.N3: (1,1),

    K.DOWN: (0,1),
    K.N2: (0,1),

    K.N1: (-1,1),

    K.LEFT: (-1,0),
    K.N4: (-1,0),

    K.N7: (-1,-1),
}
SAME_SQUARE = [K.PERIOD, K.N5]

def directional_actions(action: Action | MetaAction):
    k = {key: action(direction) for key,direction in DIRECTIONS.items()}
    if action != Bump:
        k |= {key: action((0,0)) for key in SAME_SQUARE}
    else:
        k |= {key: Wait() for key in SAME_SQUARE}
    return k


IN_GAME = {
    **directional_actions(Bump),

    (M.SHIFT, K.PERIOD): UseStairs(1),
    (M.SHIFT, K.COMMA): UseStairs(-1), 

    K.I: ViewInventory(),
    K.COMMA: PickupItemDispatch(),
    K.D: DropItems(),
    K.E: EquipOrUnequipItems(),
    K.A: ConsumeItems(),
    K.N: InteractWithFeatures(),
}


MENU = {
    K.UP: MoveCursor(-1),
    K.DOWN: MoveCursor(1),

    K.RETURN: Select(),

    K.ESCAPE: Exit(),
}


class SelectDirection(MetaAction, Directional):
    def execute(self, actor):
        g.state.action(self.direction)(actor)
        g.state.exit(report=False)

DIRECTION_SELECT = {
    **directional_actions(SelectDirection),
    K.ESCAPE: Exit(),
}


TEXT_INPUT = {
    **{i+97: Input('abcdefghijklmnopqrstuvwxyz'[i]) for i in range(26)},
    **{(M.SHIFT, i+97): Input('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i]) for i in range(26)},
    K.PERIOD: Input('.'),
    K.SPACE: Input(' '),
    K.BACKSPACE: Backspace(),
    K.RETURN: Select(),
}