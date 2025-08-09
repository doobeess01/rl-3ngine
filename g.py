import tcod
import tcod.ecs

import game.state
import game.queue

console: tcod.console.Console
context: tcod.context.Context

state: game.state.State

registry: tcod.ecs.Registry = None
player: tcod.ecs.Entity = None
player_is_dead: bool = False

def queue():
    try:
        return registry[None].components[game.queue.Queue]
    except TypeError:
        return