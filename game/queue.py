from tcod.ecs import Entity

from game.tags import Deferred


class QueueError(Exception):
    """Exception class for turn queue related errors."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class Queue:
    def __init__(self):
        self.queue: dict[int: list] = {}

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
        raise QueueError('Attempted to remove nonexistent entity from the queue')

    @property
    def front_time(self) -> int:
        try:
            return min(self.queue)
        except ValueError:
            raise QueueError('Queue is empty')

    @property
    def front_row(self) -> list:
        return self.queue[self.front_time]    
    @front_row.deleter
    def front_row(self):
        del self.queue[self.front_time]

    @property
    def front(self) -> Entity:
        return self.front_row[0]
    @front.deleter
    def front(self):
        del self.front_row[0]

    def move_front(self, time):
        if Deferred in self.front.tags:
            self.front.tags.remove(Deferred)
        new_row = self.queue.get(self.front_time+time)
        if new_row:
            new_row.append(self.front)
        else:
            self.queue[self.front_time+time] = [self.front]
        del self.front
        if not self.front_row:
            del self.front_row

    def defer_front(self):
        self.front.tags.add(Deferred)
        for time,row in self.queue.items():
            for i,actor in enumerate(row):
                if Deferred not in actor.tags:
                    self.queue[time].insert(i+1, self.front)
                    del self.front
                    return
        raise QueueError('Attempted to defer an actor after all other actors had been deferred')