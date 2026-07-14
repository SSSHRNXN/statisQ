#!usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path

config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from ..lib.coloropen import FG, BG, TTY_Stat
from ..ui import ui_parts

bg_color = f'\033[{config.getint("UI", "BG_COLOR")}m'
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len  = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')
empty_symbol = config.get('UI', 'EMPTY_SMBL')
filled_symbol = config.get('UI', 'FILLED_SMBL')

def bar(percent_for_color, value, length=10, filled_symbol=filled_symbol, empty_symbol=empty_symbol):
    PERCENT_THRESHOLDS = [
            (0, BG.WHITE + FG.BLACK),
            (30, BG.GREEN + FG.WHITE),
            (50, BG.YELLOW + FG.WHITE),
            (80, BG.RED + FG.WHITE )
            ]

    def usage_status_color(percent):
        for threshold, color in reversed(PERCENT_THRESHOLDS):
            if percent >= threshold:
                return color

    bar_color = usage_status_color(percent_for_color)
    filled = value * length // 100
    empty = length - filled
    return f'{bar_color}{filled_symbol * int(filled)}{BG.RESET}{FG.GRAY}{empty_symbol * int(empty)}{FG.RESET}'


def full_line(label:str, value, pct_for_bar:int, suff:str, pct_for_color=None, offset=offset, esymbol=ui_parts.HORIZONTAL_L):
    if pct_for_color is None:
        pct_for_color = pct_for_bar

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset,10)
    ubar = bar(pct_for_color, pct_for_bar, bar_length, empty_symbol=esymbol)

    return f'{bg_color}{ui_parts.VERTICAL_L}{label:<{label_len}}{value:>{value_len}} {suff:<{suff_len}}{BG.RESET}[{ubar}]{ui_parts.VERTICAL_L}'
