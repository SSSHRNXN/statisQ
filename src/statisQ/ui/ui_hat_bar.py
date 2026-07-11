#!/usr/bin/env python3

from ..lib.coloropen import FG, BG, TTY_Stat
from ..ui import ui_parts
from datetime import datetime 


def top_bar(label, text="", time=False):
    LINES   = TTY_Stat.lines()
    COLUMNS = TTY_Stat.columns()

    label_len = len(label) + 2
    label_str = f'{ui_parts.CORNER_BR}{label}{ui_parts.CORNER_BL}'
    if text == "":
        additional_text = ""
    else:
        additional_text = f'{ui_parts.CORNER_BR}{text}{ui_parts.CORNER_BL}'
        add_text_len = len(text) + 2

    if time:
        remover_value = 2 + 10 
        curr_time = f'{ui_parts.CORNER_BR}{datetime.now().time().strftime("%H:%M:%S")}{ui_parts.CORNER_BL}'
    else:
        remover_value = 2
        curr_time = ""

    return f'{ui_parts.CORNER_TL}{label_str}{ui_parts.HORIZONTAL_L * (COLUMNS - remover_value - label_len)}{curr_time}{ui_parts.CORNER_TR}'


def bot_bar():
    COLUMNS = TTY_Stat.columns()
    LINES   = TTY_Stat.lines()
    return f'{ui_parts.CORNER_BL}{ui_parts.HORIZONTAL_L * (COLUMNS - 2)}{ui_parts.CORNER_BR}'
