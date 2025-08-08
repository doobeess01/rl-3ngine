import tcod
import tcod.ecs

import game.state
import game.queue

console: tcod.console.Console
context: tcod.context.Context

state: game.state.State

registry: tcod.ecs.Registry

player: tcod.ecs.Entity

def queue():
    return registry[None].components[game.queue.Queue]