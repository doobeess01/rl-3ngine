import g


class Action:
    '''Base class for actions that take time to execute.'''
    def __init__(self, cost=100):
        self.cost = cost

    def __call__(self, actor):
        assert actor == g.queue().front
        if not self.execute(actor):
            g.queue().move_front(self.cost)

    def execute(self, actor):
        pass

class Wait(Action):
    '''Do nothing for a turn.'''
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


class PseudoAction(MetaAction):
    '''Base class for actions that have to be handled in states.py to avoid circular imports.'''
    def execute(self, actor):
        action = g.state.execute_pseudo_action(self)
        if action is not None:
            action(actor)