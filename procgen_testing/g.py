import tcod
import tcod.ecs

console: tcod.console.Console
center: tuple[int,int] = [0,0]

registry: tcod.ecs.Registry = None