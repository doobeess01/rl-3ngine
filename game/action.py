import g


class Action:
    '''Base class for actions that take time to execute.'''
    def __init__(self, cost=100):
        self.cost = cost

    def __call__(self, actor):
        assert actor == g.queue().front
        self.execute(actor)
        g.queue().move_front(self.cost)

    def execute(self, actor):
        pass


class MetaAction:
    '''Base class for actions that take no time to execute.'''
    def __call__(self, actor):
        self.execute(actor)

    def execute(self, actor):
        pass


class Pass(MetaAction):
    '''Action that does nothing whatsoever. Useful only as a placeholder for unimplemented features.'''
    def __init__(self, *args, **kwargs):
        pass