import g


class Action:
    def __init__(self, cost=100):
        self.cost = cost

    def __call__(self, actor):
        assert actor == g.queue().front
        self.execute(actor)
        g.queue().move_front(self.cost)

    def execute(self, actor):
        pass