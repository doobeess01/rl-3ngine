import g


class Action:
    def __call__(self, actor):
        self.execute()

    def execute(self):
        pass


class GameAction:
    def __init__(self, cost=100):
        self.cost = cost

    def __call__(self, actor):
        assert actor == g.queue().front
        self.execute(actor)
        g.queue().move_front()

    def execute(self, actor):
        pass