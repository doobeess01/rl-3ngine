from pathlib import Path
import tcod

import g

from game.states import InGame
from game.world_tools import world_init


CONSOLE_DIMENSIONS = (50,50)

THIS_DIR = Path(__file__, "..")
FONT = THIS_DIR / 'assets/Alloy_curses_12x12.png'


def draw():
    g.console.clear()
    g.state.on_draw()
    g.context.present(g.console)


def main():
    g.console = tcod.console.Console(*CONSOLE_DIMENSIONS)

    world_init()
    g.state = InGame()

    tileset = tcod.tileset.load_tilesheet(FONT, 16, 16, tcod.tileset.CHARMAP_CP437)
    with tcod.context.new(console=g.console, tileset=tileset) as g.context:
        while True:
            draw()

            for event in tcod.event.wait():
                g.state.on_event(event)
                pass


if __name__ == '__main__':
    main()