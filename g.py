import tcod
import tcod.ecs

import game.state
import game.queue

console: tcod.console.Console
context: tcod.context.Context

state: game.state.State

registry: tcod.ecs.Registry = None
player: tcod.ecs.Entity = None
player_name: str = 'player'
player_is_dead: bool = False

timekeeper: tcod.ecs.Entity = None

def queue():
    try:
        return registry[None].components[game.queue.Queue]
    except TypeError:
        return