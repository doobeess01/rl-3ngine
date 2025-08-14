import g

import game.colors as colors

class Text:
    def __init__(self, raw_string, colors: tuple[tuple[int,int,int],tuple[int,int,int]] = colors.DEFAULT):    
        self.raw_string = raw_string
        self.colors = colors

    @property
    def string(self):
        return self.raw_string

    def print(self, x: int, y: int, fg: tuple[int,int,int] = None, bg: tuple[int,int,int] = None, columns: int = None, invert:bool=False):
        fg = self.colors[0] if not fg else fg
        bg = self.colors[1] if not bg else bg
        return g.console.print(x, y, self.string, width=columns, fg=bg if invert else fg,bg=fg if invert else bg)
    
    def __eq__(self, other):
        return self.raw_string == other.raw_string and self.colors == other.colors