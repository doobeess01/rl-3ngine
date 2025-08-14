import numpy as np

import procgen_testing.g as g

from game.tiles import TILE_NAMES
from game.components import Tiles, MapShape

def generate_map(shape: tuple[int,int]):
    tiles = np.full(shape, TILE_NAMES['wall'])
    tiles[1:shape[0]-1, 1:shape[1]-1] = TILE_NAMES['floor']
    tiles[2:3, 10:shape[1]-1] = TILE_NAMES['wall']
    tiles[4:5, 10:shape[1]-1] = TILE_NAMES['wall']

    map_ = g.registry.new_entity()
    map_.components[MapShape] = shape
    map_.components[Tiles] = tiles

    return map_