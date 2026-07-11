#!usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path

config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from ..lib.coloropen import FG, BG, TTY_Stat
from ..ui import ui_parts

bg_color = f'\033[{config.getint('UI', 'BG_COLOR')}m'
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len  = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')

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


def full_bar(label:str, value:float, suff:str, bar_value=None, str_value=None, offset=offset, esymbol=None):
    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset, 10)

    if bar_value is None:
        bar_value = int(value)

    if str_value is None:
        str_value = f'{value:>{value_len}.1f}'

    if esymbol is None:
        ubar = bar(bar_value, bar_value, bar_length)
    else:
        ubar = bar(bar_value, bar_value, bar_length, empty_symbol=esymbol)


    return str(f'{bg_color}{ui_parts.VERTICAL_L}{label:<{label_len}}{str_value:>{value_len}} {suff:<{suff_len}}{BG.RESET}{ubar}{ui_parts.VERTICAL_L}')
