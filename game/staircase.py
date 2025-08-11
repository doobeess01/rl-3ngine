import g

from game.components import Position, Graphic, StaircaseDirection
from game.tags import ConnectsTo

from game.colors import STAIRCASE

def place_staircase(pos1: Position, pos2: Position):
    staircase1 = g.registry.new_entity(
        components={Position: pos1, Graphic: Graphic(ord('>'), *STAIRCASE), StaircaseDirection: 1,}
    )
    staircase2 = g.registry.new_entity(
        components={Position: pos2, Graphic: Graphic(ord('<'), *STAIRCASE), StaircaseDirection: -1,}
    )
    staircase1.relation_tag[ConnectsTo] = staircase2
    staircase2.relation_tag[ConnectsTo] = staircase1