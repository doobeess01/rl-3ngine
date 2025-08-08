import numpy as np

import g

from game.tiles import TILE_NAMES
from game.components import Tiles, MapShape

def generate_map(shape: tuple[int,int]):
    tiles = np.full(shape, TILE_NAMES['wall'])
    tiles[1:shape[0]-1, 1:shape[1]-1] = TILE_NAMES['floor']

    return g.registry.new_entity(components={MapShape: shape, Tiles: tiles})