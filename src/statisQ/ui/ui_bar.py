#!usr/bin/env python3

from ..lib.coloropen import FG, BG
from ..ui import ui_parts

def bar(percent_for_color, value, length=10, filled_symbol='+', empty_symbol=ui_parts.HORIZONTAL_L):
    PERSENT_THRESHOLDS = [
            (0, BG.WHITE + FG.BLACK),
            (30, BG.GREEN + FG.WHITE),
            (50, BG.YELLOW + FG.WHITE),
            (80, BG.RED + FG.WHITE )
            ]

    def usage_status_color(percent):
        for threshold, color in reversed(PERSENT_THRESHOLDS):
            if percent >= threshold:
                return color

    bar_color = usage_status_color(percent_for_color)
    filled = value * length // 100
    empty = length - filled
    return f'{bar_color}{filled_symbol * int(filled)}{BG.RESET}{FG.GRAY}{empty_symbol * int(empty)}{FG.RESET}'
