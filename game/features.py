from tcod.ecs import Entity

import g

from game.components import Position, Graphic, StaircaseDirection, OnInteract, Name
from game.tags import ConnectsTo, IsBlocking
from game.message_log import log
from game.text import Text
import game.colors as colors


def place_staircase(pos1: Position, pos2: Position):
    staircase1 = g.registry.new_entity(
        components={Position: pos1, Graphic: Graphic(ord('>'), *colors.STAIRCASE), StaircaseDirection: 1,}
    )
    staircase2 = g.registry.new_entity(
        components={Position: pos2, Graphic: Graphic(ord('<'), *colors.STAIRCASE), StaircaseDirection: -1,}
    )
    staircase1.relation_tag[ConnectsTo] = staircase2
    staircase2.relation_tag[ConnectsTo] = staircase1


class DoorInteract(OnInteract):
    def __call__(self, feature, actor):
        result = toggle_door(feature)
        log(Text(f'{actor.components[Name]} {"closes" if result else "opens"} the door.'))

def toggle_door(door: Entity):
    if IsBlocking in door.tags:
        door.tags.remove(IsBlocking)
        door.components[Graphic].ch = ord("-")
        return False
    else:
        door.tags.add(IsBlocking)
        door.components[Graphic].ch = ord("+")
        return True

def place_door(pos: Position, open = False, clrs: tuple[tuple[int,int,int],tuple[int,int,int]] = colors.DOOR):
    door = g.registry.new_entity(
        components={
            Position: pos, 
            Graphic: Graphic(ord('+'), *clrs if clrs else colors.DOOR),
            OnInteract: DoorInteract(),
        },
        tags=[IsBlocking]
    )
    if open:
        toggle_door(door)