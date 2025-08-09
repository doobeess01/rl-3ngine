import attrs

import g

from game.text import Text


class Message(Text):
    def __init__(self, text, fg, bg, count=1):
        super().__init__(text, fg, bg)
        self.count = count
    def print(self, x, y, fg = None, bg = None, invert = False):
        multiple_text = f' (x{self.count})' if self.count > 1 else ''
        self.text += multiple_text
        super().print(x, y, fg, bg, invert)
        if len(multiple_text) > 0:
            self.text = self.text[:-len(multiple_text)]
    def __eq__(self, other):
        if self.text == other.text and self.fg == other.fg and self.bg == other.bg:
            return True
        return False


class MessageLog:
    def __init__(self, width=None):
        self.width = width
        self.messages: list[Message] = []
    def log(self, text: str, fg: tuple[int, int, int], bg: tuple[int, int, int]):
        message = Message(text, fg, bg)
        try:
            if message == self.messages[-1]:
                self.messages[-1].count += 1
                return
        except IndexError:
            pass
        self.messages.append(message)
    def render(self, position: tuple[int, int], rows: int):
        for i, message in enumerate(self.messages[-rows:]):
            message.print(position[0], position[1]+i)
    def clear(self):
        self.messages = []


def log(text: str, colors: tuple[tuple] = ((255,255,255), (0,0,0))):
    '''Wrapper function for ease of use when interacting with the message log.'''
    g.registry[None].components[MessageLog].log(text, colors[0], colors[1])