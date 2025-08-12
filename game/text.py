import g

import game.colors as colors

class Text:
    def __init__(self, text, colors: tuple[tuple[int,int,int],tuple[int,int,int]] = colors.DEFAULT):    
        self.text = text
        self.colors = colors

    def print(self, x: int, y: int, fg: tuple[int,int,int] = None, bg: tuple[int,int,int] = None, invert:bool=False):
        fg = self.colors[0] if not fg else fg
        bg = self.colors[1] if not bg else bg
        g.console.print(x,y,self.text,fg=bg if invert else fg,bg=fg if invert else bg)