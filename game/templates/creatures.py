import g

from game.components import Name, Graphic, Description, MaxHP, HP, UnarmedAttack

from game.controller import Controller
from game.controllers import Hostile, Wander

import game.colors as colors


def new_creature(
        name: str = 'unknown creature', 
        graphic: Graphic = None, 
        desc: str = "[No description]", 
        hp: int = 10,
        attack: int = 1,
        controller: Controller = None,
        components: dict = {}, 
        tags: set = {},
        ):
    creature = g.registry.new_entity(
        components = {Name: name, Graphic: graphic, Description: desc, MaxHP: hp, HP: hp, UnarmedAttack: attack, Controller: controller,}|components,
        tags = tags
    )

    return creature


PLAYER = new_creature(
    name='player',
    graphic=Graphic(ord('@'), (255,255,255), (0,0,0)),
    desc="You're you.",
    hp=15,
    attack=3,
)

MONSTER = new_creature(
    name='monster',
    graphic=Graphic(ord('M'), colors.GREEN, colors.BLACK),
    desc="It's a horrible monster!",
    hp=10,
    attack=3,
    controller=Hostile(),
)