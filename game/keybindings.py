from tcod.event import KeySym as K

from game.actions import *

IN_GAME = {
    K.UP: Bump((0,-1)),
    K.N8: Bump((0,-1)),

    K.N9: Bump((1,-1)),

    K.RIGHT: Bump((1,0)),
    K.N6: Bump((1,0)),

    K.N3: Bump((1,1)),

    K.DOWN: Bump((0,1)),
    K.N2: Bump((0,1)),

    K.N1: Bump((-1,1)),

    K.LEFT: Bump((-1,0)),
    K.N4: Bump((-1,0)),

    K.N7: Bump((-1,-1)),

    K.PERIOD: Wait(),
    K.N5: Wait(),

    K.I: ViewInventory(),
    K.COMMA: PickupItemDispatch(),
    K.D: DropItems(),
    K.E: EquipOrUnequipItems(),
    K.A: ConsumeItems(),
}

MENU = {
    K.UP: MoveCursor(-1),
    K.DOWN: MoveCursor(1),

    K.RETURN: Select(),

    K.ESCAPE: Exit(),
}