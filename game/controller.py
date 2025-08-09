import tcod.ecs

from game.action import Action, MetaAction
from game.actions import Wait

class Controller:
    def __call__(self, actor: tcod.ecs.Entity) -> Action | MetaAction:
        return Wait()