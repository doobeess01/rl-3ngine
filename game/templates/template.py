from tcod.ecs import Entity

import g

from game.components import Position, Graphic, Name, Description

class Template:
    def __init__(
            self,
            name: str = 'unknown creature', 
            graphic: Graphic = None, 
            desc: str = "[No description]",
            components: dict = {}, 
            tags: set = {},
            ):
        self.template = g.registry.new_entity(
            components = {
                Name: name,
                Graphic: graphic,
                Description: desc,
            }|components,
            tags = tags,
        )
    def spawn(self, position: Position = None, components: dict = {}, tags: set = {}) -> Entity:
        e = self.template.instantiate()
        if position:
            e.components[Position] = position
        e.components |= components
        e.tags |= tags

        return e