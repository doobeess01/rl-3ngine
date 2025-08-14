from game.text import Text

def wrap_texts(texts: list[Text | None]):
    return texts  # TODO: Implement

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