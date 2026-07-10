#!/usr/bin/env python3

from ..lib.coloropen import FG, BG, TTY_Stat
from ..ui import ui_parts


def top_bar(label):
    LINES   = TTY_Stat.lines()
    COLUMNS = TTY_Stat.columns()

    label_len = len(label) + 4
    label_str = f'{ui_parts.CORNER_BR} {label} {ui_parts.CORNER_BL}'
    return f'{ui_parts.CORNER_TL}{label_str}{ui_parts.HORIZONTAL_L * (COLUMNS - 2 - label_len)}{ui_parts.CORNER_TR}'


def bot_bar():
    COLUMNS = TTY_Stat.columns()
    LINES   = TTY_Stat.lines()
    return f'{ui_parts.CORNER_BL}{ui_parts.HORIZONTAL_L * (COLUMNS - 2)}{ui_parts.CORNER_BR}'
