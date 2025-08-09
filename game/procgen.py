import numpy as np

import g

from game.tiles import TILE_NAMES
from game.components import Tiles, MapShape, VisibleTiles, MemoryTiles

def generate_map(shape: tuple[int,int]):
    tiles = np.full(shape, TILE_NAMES['wall'])
    tiles[1:shape[0]-1, 1:shape[1]-1] = TILE_NAMES['floor']

    map_ = g.registry.new_entity()
    map_.components[MapShape] = shape
    map_.components[Tiles] = tiles
    map_.components[VisibleTiles] = np.zeros(shape, dtype=np.bool)
    map_.components[MemoryTiles] = np.zeros(shape, dtype=np.int8)

    return map_