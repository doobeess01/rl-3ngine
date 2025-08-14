from copy import deepcopy

from game.text import Text

def wrap_texts(texts: list[Text | None], max_length: int):
    wrapped_texts = deepcopy(texts)
    index = 0   
    while index < len(wrapped_texts):
        if wrapped_texts[index]:
            if len(wrapped_texts[index].string) > max_length:
                new_text = ''
                split_text = wrapped_texts[index].string.split()
                while len(' '.join(split_text)) > max_length:
                    new_text = split_text.pop(-1) + ' ' + new_text
                wrapped_texts[index].raw_string = ' '.join(split_text)
                wrapped_texts.insert(index + 1, Text(new_text, wrapped_texts[index].colors))
        index += 1
    return wrapped_texts  # TODO: Implement

def get_text_rows(texts: list[Text | None], rows: int, offset: int = 0):
    if len(texts)-rows-offset > 0:
        rows_start = len(texts)-rows-offset
        rows_end = len(texts)-offset
    else:
        rows_start = 0
        rows_end = len(texts)
    return texts[rows_start:rows_end]

def print_text_rows(texts: list[Text | None], position: tuple[int, int]):
    for i,message in enumerate(texts):
        if message is not None:
            message.print(position[0], position[1]+i)