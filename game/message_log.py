import copy

import g

from game.text import Text
from game.text_tools import get_text_rows


class Message:
    def __init__(self, text: Text, count=1):
        self.text = text
        self.count = count

    def print(self, x, y, fg = None, bg = None, columns: int = None, invert = False):
        multiple_text = f' (x{self.count})' if self.count > 1 else ''
        printed_text = copy.deepcopy(self.text)
        printed_text.string += multiple_text
        return printed_text.print(x, y, fg, bg, columns, invert)

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
    def render(self, position: tuple[int, int], rows: int, offset: int = 0):
        printed_messages = get_text_rows(self.messages, rows, offset=offset)
        for i,message in enumerate(printed_messages):
            message.print(position[0], position[1]+i)

    def clear(self):
        self.messages = []


def message_log():
    return g.registry[None].components[MessageLog]


def log(text: Text):
    '''Wrapper function for ease of use when interacting with the message log.'''
    g.registry[None].components[MessageLog].log(text)