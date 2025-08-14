import g

import game.colors as colors

class Text:
    def __init__(self, string, colors: tuple[tuple[int,int,int],tuple[int,int,int]] = colors.DEFAULT):    
        self.string = string
        self.colors = colors

    def print(self, x: int, y: int, fg: tuple[int,int,int] = None, bg: tuple[int,int,int] = None, columns: int = None, invert:bool=False):
        fg = self.colors[0] if not fg else fg
        bg = self.colors[1] if not bg else bg
        return g.console.print(x, y, self.string, width=columns, fg=bg if invert else fg,bg=fg if invert else bg)