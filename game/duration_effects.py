from game.duration_effect import DurationEffect
from game.components import HP
import game.colors as colors

class HPRegen(DurationEffect):
    def __init__(self, hp_per_turn: int, duration: int):
        super().__init__(duration, name = 'HPRegen', colors = colors.EFFECT_HPREGEN)
        self.hp_per_turn = hp_per_turn
    def affect(self, actor):
        actor.components[HP] += self.hp_per_turn