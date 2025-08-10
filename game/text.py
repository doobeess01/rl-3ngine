import g

import game.colors as colors

class Text:
    def __init__(self, text, fg: tuple[int,int,int] = colors.WHITE, bg: tuple[int,int,int] = colors.BLACK):    
        self.text = text
        self.fg = fg
        self.bg = bg

    def print(self, x: int, y: int, fg: tuple[int,int,int] = None, bg: tuple[int,int,int] = None, invert:bool=False):
        fg = self.fg if not fg else fg
        bg = self.bg if not bg else bg
        g.console.print(x,y,self.text,fg=bg if invert else fg,bg=fg if invert else bg)