import tcod.ecs
from tcod.camera import get_camera, get_slices

import g

from game.components import Position, Graphic, Tiles, MapShape
from game.tiles import TILES

def render_map(map_: tcod.ecs.Entity, screen_shape: tuple[int, int], center: tuple[int,int]):
    camera = get_camera(screen_shape, center)
    screen_slices, map_slices = get_slices(screen_shape, map_.components[MapShape], camera)
    g.console.rgb[screen_slices] = TILES['graphic'][map_.components[Tiles][map_slices]]

    for e in g.registry.Q.all_of(tags=[map_], components=[Position, Graphic]):
        pos = e.components[Position]
        rendered_pos = pos - (camera[1], camera[0])
        graphic = e.components[Graphic]

        if 0 <= rendered_pos.x < screen_shape[1] and 0 <= rendered_pos.y < screen_shape[0]:
            g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg