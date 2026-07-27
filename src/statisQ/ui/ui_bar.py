#!usr/bin/env python3

from ..cfg import config

from ..lib.coloropen import FG, BG, TTY_Stat, BG255, FG255
from ..ui import ui_parts

bg_color = BG255(config.UI.COLORS.BG)
text_color = FG255(config.UI.COLORS.TEXT)
label_len = config.UI.LABEL_LEN
value_len = config.UI.VALUE_LEN
suff_len  = config.UI.SUFF_LEN
offset = config.UI.OFFSET
empty_symbol = config.UI.EMPTY_SMBL
filled_symbol = config.UI.FILLED_SMBL

def bar(percent_for_color, value, length=10, filled_symbol=filled_symbol, empty_symbol=empty_symbol):
    PERCENT_THRESHOLDS = [
            (0, BG255(config.UI.COLORS.LOW) + FG.BLACK),
            (30, BG255(config.UI.COLORS.MID) + FG255(255)),
            (50, BG255(config.UI.COLORS.HIGH) + FG255(255)),
            (80, BG255(config.UI.COLORS.FULL) + FG255(255))
            ]

    def usage_status_color(percent):
        for threshold, color in reversed(PERCENT_THRESHOLDS):
            if percent >= threshold:
                return color

    bar_color = usage_status_color(percent_for_color)
    filled = value * length // 100
    empty = length - filled
    return f'{bar_color}{filled_symbol * int(filled)}{BG.RESET}{FG.GRAY}{BG255(config.UI.COLORS.EMPTY_COLOR)}{empty_symbol * int(empty)}{FG.RESET}'


def full_line(label:str, value, pct_for_bar:int, suff:str, pct_for_color=None, offset=offset, esymbol=ui_parts.nHORIZONTAL_L):
    if pct_for_color is None:
        pct_for_color = pct_for_bar

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset,10)
    ubar = bar(pct_for_color, pct_for_bar, bar_length, empty_symbol=esymbol)

    return f'{ui_parts.VERTICAL_L}{bg_color}{text_color}{label:<{label_len}}{value:>{value_len}} {suff:<{suff_len}}{BG.RESET}[{ubar}]{ui_parts.VERTICAL_L}'

def empty_bar(text="", center=False):
    bar_length = TTY_Stat.columns() - 2 - len(text)
    if bar_length < 0: bar = 0
    if len(str(text)) > bar_length + len(text):
        text = f'{text[:bar_length-1]}{BG.WHITE}{FG.BLACK}*{BG.RESET}'
    return f'{ui_parts.VERTICAL_L}{bg_color}{text_color}{text}{" " * (bar_length)}{BG.RESET}{ui_parts.VERTICAL_L}'
