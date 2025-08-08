"""Tiles database."""

from __future__ import annotations

from typing import Final

import numpy as np
import tcod.console

import game.colors as colors

TILES = np.asarray(
    [
        ("void", (ord(" "), colors.BLACK, colors.BLACK), 0, True),
        ("wall", (ord("#"), colors.WHITE, colors.BLACK), 0, False),
        ("window", (ord('#'), colors.LIGHT_BLUE, colors.BLACK), 0, False),
        ("floor", (ord("."), colors.WHITE, colors.BLACK), 1, True),
    ],
    dtype=[
        ("name", object),
        ("graphic", tcod.console.rgb_graphic),
        ("walk_cost", np.int8),
        ("transparent", np.bool),
    ],
)

TILES.flags.writeable = False
TILE_NAMES: Final = {tile["name"]: i for i, tile in enumerate(TILES)}