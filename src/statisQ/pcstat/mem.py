#!/usr/bin/env python3

from ..cfg import config

from ..lib.coloropen import FG, TTY_Stat, clog, BG, BG255
from ..ui import ui_parts, ui_bar
import psutil

bg_color = BG255(config.UI.COLORS.BG)
label_len = config.UI.LABEL_LEN
value_len = config.UI.VALUE_LEN
suff_len = config.UI.SUFF_LEN
offset = config.UI.OFFSET


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
            ('USAGE',    f'{get_gb_value(used)}',       percent),
            ('%USE%',   f'{percent}',                   percent)
            ]

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset,10)

    lines = []
    for label, value, pct in allstat:
        esymbol = ui_parts.nHORIZONTAL_L 
        color = None
        if label == 'TOTAL' or label == '%USE%':
            suff = "%"
            if label == 'TOTAL':
                suff = "gb"
                esymbol = "+"
        else:
            if label == 'AVAIL':
                color = percent 
            suff = "gb"

        lines.append(ui_bar.full_line(label, float(value), pct, suff, pct_for_color=color, esymbol=esymbol ))


    return '\n'.join(lines)
