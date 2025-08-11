from tcod.ecs import Entity


class QueueError(Exception):
    '''Exception class for turn queue related errors.'''


class Queue:
    def __init__(self):
        self.queue: dict = {}

    def clear(self):
        self.queue = {}
    
    def add(self, actor: Entity):
        try:
            self.queue[min(self.queue)].append(actor)
        except ValueError:
            self.queue[0] = [actor]

    def remove(self, actor: Entity):
        for row in self.queue:
            if actor in self.queue[row]:
                self.queue[row].remove(actor)
                return
        raise QueueError()

    @property
    def front(self):
        if self.queue:
            return self.queue[min(self.queue)][0]
        raise QueueError()

    def move_front(self, time):
        try:
            self.queue[min(self.queue)+time].append(self.front)
        except KeyError:
            self.queue[min(self.queue)+time] = [self.front]
        except ValueError:
            raise QueueError()
        del self.queue[min(self.queue)][0]
        if not self.queue[min(self.queue)]:
            del self.queue[min(self.queue)]