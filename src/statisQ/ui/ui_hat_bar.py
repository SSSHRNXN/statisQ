#!/usr/bin/env python3

from ..cfg import config

from ..lib.coloropen import ST, TTY_Stat
from ..ui import ui_parts
from datetime import datetime 

text_offset = config.UI.TEXT_OFFSET
min_width = config.UI.MIN_WIDTH
label_len = config.UI.LABEL_LEN
value_len = config.UI.VALUE_LEN
suff_len  = config.UI.SUFF_LEN
offset = config.UI.OFFSET

def top_bar(label, text="", time=False):
    COLUMNS = TTY_Stat.columns()
    corner_count = 2
    remover_value = 0 + corner_count #only full bar corners

    label_len = len(label) + corner_count
    label_str = f'{ui_parts.CORNER_BR}{ST.REVERSE}{label}{ST.RESET}{ui_parts.CORNER_BL}'
    if text == "":
        additional_text = ""
        add_text_len = 0
    else:
        avail_space = COLUMNS - corner_count - label_len
        if len(text) > avail_space:
            text = f"{text[:text_offset]}*"

        additional_text = f'{ui_parts.CORNER_BR}{ST.REVERSE}{text}{ST.RESET}{ui_parts.CORNER_BL}'
        add_text_len = len(text) + corner_count

    if time:
        remover_value += 8 + corner_count #len(time) + time str corners + full bar corners
        curr_time = f'{ui_parts.CORNER_BR}{ST.REVERSE}{datetime.now().time().strftime("%H:%M:%S")}{ST.RESET}{ui_parts.CORNER_BL}'
    else:
        curr_time = ""

    return f'{ui_parts.CORNER_TL}{label_str}{ui_parts.HORIZONTAL_L * (COLUMNS - remover_value - label_len - add_text_len)}{additional_text}{curr_time}{ui_parts.CORNER_TR}'


def bot_bar(text=""):
    COLUMNS = TTY_Stat.columns()

    if text == "":
        additional_text = ""
        add_text_len = 0
    else:
        additional_text = f'{ui_parts.CORNER_BR}{ST.REVERSE}{text}{ST.RESET}{ui_parts.CORNER_BL}'
        add_text_len = len(text) + 2

    return f'{ui_parts.CORNER_BL}{additional_text}{ui_parts.HORIZONTAL_L * (COLUMNS - 2 - add_text_len)}{ui_parts.CORNER_BR}'

def straight_line():
    COLUMNS = TTY_Stat.columns()

    return f'{ui_parts.VERTICAL_L}{ui_parts.HORIZONTAL_L * (COLUMNS - 2)}{ui_parts.VERTICAL_L}'
