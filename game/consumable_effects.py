from game.components import OnConsume, HP

class HealthBoost(OnConsume):
    def __init__(self, hp: int):
        self.hp = hp
    def affect(self, actor):
        actor.components[HP] += self.hp