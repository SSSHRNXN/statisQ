#!/usr/bin/env python3

from ..lib.coloropen import FG, BG, TTY_Stat
from ..ui import ui_parts

COLUMNS = TTY_Stat.COLUMNS
LINES   = TTY_Stat.LINES
def top_bar():
    return f'{ui_parts.CORNER_TL}{ui_parts.HORIZONTAL_L * (COLUMNS - 2)}{ui_parts.CORNER_TR}'


def bot_bar():
    return f'{ui_parts.CORNER_BL}{ui_parts.HORIZONTAL_L * (COLUMNS - 2)}{ui_parts.CORNER_BR}'
