#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from ..lib.coloropen import ST, TTY_Stat
from ..ui import ui_parts
from datetime import datetime 

text_offset = config.getint('UI', 'TEXT_OFFSET')
min_width = config.getint('UI', 'MIN_WIDTH')
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len  = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')

def top_bar(label, text="", time=False):
    LINES   = TTY_Stat.lines()
    COLUMNS = TTY_Stat.columns()
    remover_value = 2
    corner_count = 2

    label_len = len(label) + corner_count
    label_str = f'{ui_parts.CORNER_BR}{ST.REVERSE}{label}{ST.RESET}{ui_parts.CORNER_BL}'
    if text == "":
        additional_text = ""
        add_text_len = 0
    else:
        avail_space = COLUMNS - remover_value - label_len
        if len(text) > avail_space:
            text = f"{text[:text_offset]}*"

        additional_text = f'{ui_parts.CORNER_BR}{ST.REVERSE}{text}{ST.RESET}{ui_parts.CORNER_BL}'
        add_text_len = len(text) + corner_count

    if time:
        remover_value =+ 10 
        curr_time = f'{ui_parts.CORNER_BR}{ST.REVERSE}{datetime.now().time().strftime("%H:%M:%S")}{ST.RESET}{ui_parts.CORNER_BL}'
    else:
        curr_time = ""

    return f'{ui_parts.CORNER_TL}{label_str}{ui_parts.HORIZONTAL_L * (COLUMNS - remover_value - label_len - add_text_len)}{additional_text}{curr_time}{ui_parts.CORNER_TR}'


def bot_bar(text=""):
    COLUMNS = TTY_Stat.columns()
    LINES   = TTY_Stat.lines()

    if text == "":
        additional_text = ""
        add_text_len = 0
    else:
        additional_text = f'{ui_parts.CORNER_BR}{ST.REVERSE}{text}{ST.RESET}{ui_parts.CORNER_BL}'
        add_text_len = len(text) + 2

    return f'{ui_parts.CORNER_BL}{additional_text}{ui_parts.HORIZONTAL_L * (COLUMNS - 2 - add_text_len)}{ui_parts.CORNER_BR}'
