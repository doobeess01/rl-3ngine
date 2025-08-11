import tcod.ecs

from game.action import Action, MetaAction, Wait


class Controller:
    def __call__(self, actor: tcod.ecs.Entity) -> Action | MetaAction:
        return Wait()