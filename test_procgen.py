from pathlib import Path

import tcod
import tcod.ecs

import procgen_testing.g as g
from procgen_testing.rendering import render_map
from procgen_testing.procgen import generate_map
from game.keybindings import directional_actions

THIS_DIR = Path(__file__, "..")
FONT = THIS_DIR / 'assets/Alloy_curses_12x12.png'

CONSOLE_WIDTH = 50
CONSOLE_HEIGHT = 50
g.console = console = tcod.console.Console(50,50)

tileset = tcod.tileset.load_tilesheet(FONT, 16, 16, tcod.tileset.CHARMAP_CP437)


def fake_directional_action(direction):
    return direction[1],direction[0]

keybindings = {
    **directional_actions(fake_directional_action)
}


g.registry = tcod.ecs.Registry()


MAP_WIDTH = 100
MAP_HEIGHT = 100
map_ = generate_map((MAP_HEIGHT, MAP_WIDTH))


with tcod.context.new(console=console, tileset=tileset) as context:
    while True:
        console.clear()
        render_map(map_, screen_shape=(g.console.width,g.console.height), center = g.center)
        context.present(console)

        for event in tcod.event.wait():
            match event:
                case tcod.event.KeyDown(sym=sym) if sym in keybindings:
                    g.center[0] += keybindings[sym][0]
                    g.center[1] += keybindings[sym][1]
                case tcod.event.Quit():
                    raise SystemExit