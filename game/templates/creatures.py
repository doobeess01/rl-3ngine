import g

from game.templates.template import Template
from game.components import Name, Position, Graphic, Description, MaxHP, HP, UnarmedAttack
from game.tags import IsCreature, IsActor

from game.controller import Controller
from game.controllers import Hostile, Wander

import game.colors as colors


class Creature(Template):
    def __init__(
            self,
            name: str = 'unknown creature', 
            graphic: Graphic = None, 
            desc: str = "[No description]", 
            hp: int = 10,
            attack: int = 1,
            controller: Controller = None,
            components: dict = {}, 
            tags: set = {},
            ):
        super().__init__(
            name = name,
            graphic = graphic,
            desc = desc,
            components = {
                MaxHP: hp,
                HP: hp,
                UnarmedAttack: attack,
                Controller: controller,
            }|components,
            tags = tags,
        )
        
    def spawn(self, position: Position = None, components = {}, tags = {}):
        creature = super().spawn(position, components, tags)
        creature.tags.add(IsCreature)
        creature.tags.add(IsActor)
        return creature


PLAYER = Creature(
    name='player',
    graphic=Graphic(ord('@'), (255,255,255), (0,0,0)),
    desc="You're you.",
    hp=15,
    attack=3,
)

MONSTER = Creature(
    name='monster',
    graphic=Graphic(ord('M'), colors.GREEN, colors.BLACK),
    desc="It's a horrible monster!",
    hp=10,
    attack=3,
    controller=Hostile(),
)