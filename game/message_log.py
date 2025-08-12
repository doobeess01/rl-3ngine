import g

from game.text import Text


class Message:
    def __init__(self, text: Text, count=1):
        self.text = text
        self.count = count
    def print(self, x, y, fg = None, bg = None, invert = False):
        multiple_text = f' (x{self.count})' if self.count > 1 else ''
        self.text.text += multiple_text
        self.text.print(x, y, fg, bg, invert)
        if len(multiple_text) > 0:
            self.text.text = self.text.text[:-len(multiple_text)]
    def __eq__(self, other):
        if self.text == other.text:
            return True
        return False


class MessageLog:
    def __init__(self, width=None):
        self.width = width
        self.messages: list[Message] = []
    def log(self, text: Text):
        message = Message(text)
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


def log(text: Text):
    '''Wrapper function for ease of use when interacting with the message log.'''
    g.registry[None].components[MessageLog].log(text)