#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from ..lib.coloropen import FG, TTY_Stat, clog, BG
from ..ui import ui_parts, ui_bar
import psutil

bg_color = f'\033[{config.getint('UI', 'BG_COLOR')}m'
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')

def get_memory_usage():
    memory_stat = psutil.virtual_memory()
    return memory_stat.total, memory_stat.used, memory_stat.available, memory_stat.percent

def get_gb_value(value):
    return f'{value / (1024 ** 3):.1f}' 

def get_stat():
    total, used, available, percent = get_memory_usage()

    allstat = [
            ('TOTAL',   f'{get_gb_value(total)}',       0) ,
            ('AVAIL',   f'{get_gb_value(available)}',   100 - percent) ,
            ('USAGE',    f'{get_gb_value(used)}',        percent) ,
            ('%USE%',   f'{percent}',                   percent)
            ]

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset,10)

    lines = []
    for label, value, pct in allstat:
        esymbol = ui_parts.HORIZONTAL_L
        if label == '%USE%' or label == 'TOTAL':
            if label == "%USE%":
                suff = '%'
            else:
                suff = "gb"
                esymbol = "+" 
        else:
            suff = 'gb'
        lines.append(ui_bar.full_bar(label, float(value), suff, bar_value=pct, esymbol=esymbol))
#        lines.append(f'{bg_color}{ui_parts.VERTICAL_L}{label:<{label_len}}{value:>{value_len}} {suff:<{suff_len}}{bar}{ui_parts.VERTICAL_L}{BG.RESET}')

    return '\n'.join(lines)
