import copy

import g

from game.text import Text
from game.text_tools import get_text_rows, wrap_texts, print_text_rows


class Message(Text):
    def __init__(self, string, colors, count=1):
        super().__init__(string, colors)
        self.count = count

    @property
    def string(self):
        multiple_text = f' (x{self.count})' if self.count > 1 else ''
        return super().string + multiple_text

    def __eq__(self, other):
        return super().__eq__(other)

class MessageLog:
    def __init__(self, width=None):
        self.width = width
        self.messages: list[Message] = []
    def log(self, string, colors):
        message = Message(string, colors)
        try:
            if message == self.messages[-1]:
                self.messages[-1].count += 1
                return
        except IndexError:
            pass
        self.messages.append(message)
    def render(self, position: tuple[int, int], rows: int, offset: int = 0):
        printed_messages = get_text_rows(wrap_texts(self.messages, g.console.width-2), rows, offset=offset)
        print_text_rows((printed_messages), position)

    def clear(self):
        self.messages = []


def message_log():
    return g.registry[None].components[MessageLog]


def log(text: Text):
    '''Wrapper function for ease of use when interacting with the message log.'''
    message_log().log(text.string, text.colors)