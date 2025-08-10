from game.components import OnConsume, HP, DurationEffects
from game.duration_effect import DurationEffect
from game.duration_effects import HPRegen
from game.entity_tools import give_duration_effect

class BoostHP(OnConsume):
    def __init__(self, hp: int):
        self.hp = hp
    def affect(self, actor):
        actor.components[HP] += self.hp

class RegenHP(OnConsume):
    def __init__(self, hp_per_turn: int, duration: int):
        self.hp_per_turn = hp_per_turn
        self.duration = duration
    def affect(self, actor):
        give_duration_effect(actor, HPRegen(self.hp_per_turn, self.duration))