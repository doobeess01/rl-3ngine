import numpy as np

from tcod.bsp import BSP
from tcod.path import SimpleGraph, Pathfinder
from tcod.ecs import Registry, Entity
import random

import procgen_testing.g as g

from game.tiles import TILE_NAMES
from game.components import Tiles, MapShape, Position, Graphic
from game.features import place_door


def chance(c):
    c /= 100
    return random.random() <= c


class Room:
    def __init__(self, x,y,width,height):
        self.x1 = x
        self.y1 = y
        self.x2 = x+width
        self.y2 = y+height
        self.width = width
        self.height = height
        self.entrances = self.get_entrances()

    @property
    def border(self):
        pass

    @property
    def entrances(self):
        pass

    def dig(self, tiles):
        pass


class RectangularRoom(Room):
    def dig(self, tiles):
        tiles[self.x1+1:self.x2, self.y1+1:+self.y2] = TILE_NAMES['void']

    @property
    def border(self):
        return self.outer()

    @property
    def entrances(self):
        return self.outer(no_corners=True)

    def outer(self, no_corners=False):
        points: list[tuple[int,int]] = []
        for x in (self.x1, self.x2):
            for y in range(self.y1, self.y2+1):
                point = (x,y)
                if point not in points:
                    if (y not in [self.y1, self.y2]) if no_corners else True:
                        points.append(point)
        for y in (self.y1, self.y2):
            for x in range(self.x1, self.x2+1):
                point = (x,y)
                if point not in points:
                    if x not in [self.x1, self.x2] if no_corners else True:
                        points.append(point)
        return points
    
    
    

ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 15


registry = g.registry

Connections = ('Connections', list[Entity])
Connected = 'Connected'

def place_door(pos: Position, clrs: tuple[tuple[int,int,int],tuple[int,int,int]] = ((255,255,255),(0,0,0))):
    door = g.registry.new_entity(
        components={
            Position: pos, 
            Graphic: Graphic(ord('+'), *clrs),
        },
    )

def generate_map(shape: tuple[int,int]):
    map_ = registry.new_entity()
    tiles = np.full(shape, TILE_NAMES['wall'])

    bsp = BSP(x=2, y=2, width=shape[1]-3, height=shape[0]-3)
    bsp.split_recursive(
        depth=8,
        min_width=8,
        min_height=8,
        max_horizontal_ratio=2,
        max_vertical_ratio=2,
    )

    # In pre order, leaf nodes are visited before the nodes that connect them.
    for node in bsp.pre_order():
        if not node.children:
            # Dig room
            min_width = ROOM_MIN_SIZE
            min_height = ROOM_MIN_SIZE
            max_width = min(node.width-2, ROOM_MAX_SIZE)
            max_height = min(node.height-2, ROOM_MAX_SIZE)

            width = random.randint(min_width, max_width)
            height = random.randint(min_height, max_height)
            x = random.randint(0, node.width-width-2)
            y = random.randint(0, node.height-height-2)

            if chance(70):
                room = RectangularRoom(node.x+x+1,node.y+y+1,width,height)
                room.dig(tiles)
                registry.new_entity(components={
                    RectangularRoom: room,
                    Connections: [],
                })

    cost = np.full(tiles.shape, 2)
    for room in registry.Q.all_of(components=[RectangularRoom]):
        for coor in room.components[RectangularRoom].outer():
            cost[*coor] = 99999999

    graph = SimpleGraph(cost=cost, cardinal=1, diagonal=5)
    pf = Pathfinder(graph)

    unconnected_rooms = [None]
    while [e for e in unconnected_rooms]:
        unconnected_rooms = registry.Q.all_of(components=[RectangularRoom]).none_of(tags=[Connected])
        room: Entity = random.choice(list(unconnected_rooms))
        room.tags.add(Connected)
        room.tags.add('active')

        weights = [0,0,1,1,1,2,2,3]

        connect_to = random.sample(list(unconnected_rooms), min(len(list(unconnected_rooms)), random.choice(weights)))
        try:
            connect_to.append(random.choice(list(registry.Q.all_of(components=[RectangularRoom], tags=[Connected]).none_of(tags=['active']))))
        except IndexError:
            pass

        for connected_room in connect_to:
            pf = Pathfinder(graph)
            pf.add_root(random.choice(room.components[RectangularRoom].outer(no_corners=True)))
            path = pf.path_to(random.choice(connected_room.components[RectangularRoom].outer(no_corners=True)))
            for step in path:
                tiles[*step] = TILE_NAMES['floor']

            for step in path[1:len(path)-1]:
                cost[*step] = 1

            for endpoint in path[0], path[-1]:
                endpoint = endpoint[-1::-1]
                place_door(Position(*endpoint, map_))

            graph = SimpleGraph(cost=cost, cardinal=1, diagonal=5)

        room.tags.remove('active')
    
    map_.components[MapShape] = shape
    map_.components[Tiles] = tiles
   

    return map_