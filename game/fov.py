import tcod
import tcod.ecs
from typing import Final
import numpy as np

from game.tiles import TILES
from game.components import Position, Graphic, Name, Tiles, VisibleTiles, MemoryTiles
from game.tags import IsGhost

def update_fov(actor: tcod.ecs.Entity, *, clear: bool = False) -> None:
    """Update the FOV of an actor."""
    map_: Final = actor.components[Position].map_
    transparency: Final = TILES["transparent"][map_.components[Tiles]]
    old_visible: Final = map_.components[VisibleTiles]
    if clear:  # Unset visibility, for before level transitions.
        map_.components[VisibleTiles][:] = False
        new_visible = map_.components[VisibleTiles]
    else:
        map_.components[VisibleTiles] = new_visible = tcod.map.compute_fov(
            transparency,
            pov=actor.components[Position].ij,
            radius=10,
            algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST,
        )
    map_.components[MemoryTiles] = np.where(new_visible, map_.components[Tiles], map_.components[MemoryTiles])

    now_invisible: Final = old_visible & ~new_visible  # Tiles which have gone out of view, should leave ghosts
    all_visible: Final = old_visible & new_visible  # Tiles visible in old and new FOV, should clear ghosts

    world: Final = actor.registry
    # Remove visible ghosts
    for entity in world.Q.all_of(components=[Position], tags=[IsGhost, map_]):
        if all_visible[entity.components[Position].ij]:
            entity.clear()
    # Add ghosts for entities going out of view
    for entity in world.Q.all_of(components=[Position, Graphic], tags=[map_]).none_of(tags=[IsGhost]):
        pos = entity.components[Position]
        if not now_invisible[pos.ij]:
            continue
        ghost = world[object()]
        ghost.tags.add(IsGhost)
        ghost.components[Position] = pos
        ghost.components[Graphic] = entity.components[Graphic]
        if Name in entity.components:
            ghost.components[Name] = entity.components[Name]
