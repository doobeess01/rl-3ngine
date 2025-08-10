from game.text import Text
import game.colors as colors

class DurationEffect:
    def __init__(self, duration: int, name = '???', colors: tuple[tuple[int,int,int],tuple[int,int,int]] = colors.DEFAULT):
        self.duration = duration
        self.name = name
        self.colors = colors
    def __call__(self, actor):
        self.affect(actor)
        self.duration -= 1
        if self.duration:
            return True
        return False
    def affect(self, actor):
        pass
    @property
    def text(self):
        return Text(f'{self.name} ({self.duration})', *self.colors)