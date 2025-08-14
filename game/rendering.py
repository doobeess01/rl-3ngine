import tcod.ecs
from tcod.camera import get_camera, get_slices
import numpy as np

import g

from game.fov import update_fov
from game.components import Position, Graphic, Tiles, MapShape, VisibleTiles, MemoryTiles
from game.tags import IsGhost, IsItem, IsCreature
from game.tiles import TILES
from game.message_log import MessageLog
from game.text import Text


def render_map(map_: tcod.ecs.Entity, screen_shape: tuple[int, int], center: tuple[int,int]):
    g.console.draw_frame(-1,-1,g.console.width+2, screen_shape[0]+2)
    g.console.draw_frame(-1,-1,screen_shape[1]+2, screen_shape[0]+2)
    g.console.print(screen_shape[1], screen_shape[0], '┴')

    update_fov(g.player)

    camera = get_camera(screen_shape, center)
    console_slices, map_slices = get_slices(screen_shape, map_.components[MapShape], camera)

    visible = map_.components[VisibleTiles][map_slices]
    not_visible = ~visible

    light_tiles = map_.components[Tiles][map_slices]
    dark_tiles = map_.components[MemoryTiles][map_slices]

    g.console.rgb[console_slices] = TILES["graphic"][np.where(visible, light_tiles, dark_tiles)]

    rendered_priority: dict[Position, int] = {}
    for e in g.registry.Q.all_of(tags=[map_], components=[Position, Graphic]):
        pos = e.components[Position]
        rendered_pos = pos - (camera[1], camera[0])
        graphic = e.components[Graphic]

        if IsGhost not in e.tags:
            render_order = 1
            if IsItem in e.tags:
                render_order = 2
            if IsCreature in e.tags:
                render_order = 3
            if g.player == e:
                render_order = 4
            if rendered_priority.get(rendered_pos, 0) >= render_order:
                continue  # Do not render over a more important entity
            rendered_priority[rendered_pos] = render_order

        in_bounds = 0 <= rendered_pos.x < screen_shape[1] and 0 <= rendered_pos.y < screen_shape[0]

        rendered = False
        if in_bounds:
            offset = (0 if camera[1] > 0 else camera[1], 0 if camera[0] > 0 else camera[0])

            rendered = visible[(rendered_pos+offset).ij] != (IsGhost in e.tags) 

        if in_bounds and rendered:
            g.console.rgb[["ch", "fg"]][rendered_pos.ij] = graphic.ch, graphic.fg

    g.console.rgb["fg"][console_slices][not_visible] //= 2
    g.console.rgb["bg"][console_slices][not_visible] //= 2


def render_message_log(position: tuple[int,int], rows: int):
    g.registry[None].components[MessageLog].render(position, rows)


def render_sidebar(position: tuple[int,int], lines: list[Text | None]):
    for i,text in enumerate(lines):
        if text:
            text.print(position[0],position[1]+i)