#!/usr/bin/env python3

from ..lib.coloropen import TTY_Stat, FG
from ..ui import ui_parts

def failed_render_window(columns, lines, min_columns, min_lines):

    def color_value(value, min_value):
        if value < min_value:
            return f'{FG.RED}{value}{FG.RESET}'
        else:
            return f'{FG.GREEN}{value}{FG.RESET}'
        
    return f'Not enough space\nfor render\n{color_value(columns, min_columns)} {color_value(lines, min_lines)}\n{FG.YELLOW}{min_columns} {min_lines}{FG.RESET}'
