import tcod
import tcod.ecs
from tcod.camera import get_camera, get_slices

from game.components import MapShape, Tiles, Position, Graphic
from game.tiles import TILES

import procgen_testing.g as g

def render_map(map_: tcod.ecs.Entity, screen_shape: tuple[int, int], center: tuple[int,int]):
    g.console.draw_frame(-1,-1,g.console.width+2, screen_shape[0]+2)
    g.console.draw_frame(-1,-1,screen_shape[1]+2, screen_shape[0]+2)
    g.console.print(screen_shape[1], screen_shape[0], '┴')

    camera = get_camera(screen_shape, center)
    console_slices, map_slices = get_slices(screen_shape, map_.components[MapShape], camera)

    g.console.rgb[console_slices] = TILES["graphic"][map_.components[Tiles][map_slices]]

    for e in g.registry.Q.all_of(tags=[map_], components=[Position, Graphic]):
        pos = e.components[Position]
        rendered_pos = pos - (camera[1], camera[0])
        graphic = e.components[Graphic]

        in_bounds = 0 <= rendered_pos.x < screen_shape[1] and 0 <= rendered_pos.y < screen_shape[0]

        if in_bounds:
            g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg