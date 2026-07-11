#!/usr/bin/env python3

from ..lib.coloropen import FG, TTY_Stat, clog, BG
from ..ui import ui_parts, ui_bar
import psutil

label_len = 10
value_len = 6
offset = 7 #count of spaces and [] symbols

def get_memory_usage():
    memory_stat = psutil.virtual_memory()
    return memory_stat.total, memory_stat.used, memory_stat.available, memory_stat.percent

def get_gb_value(value):
    return f'{value / (1024 ** 3):.1f}' 

def get_stat():
    total, used, available, percent = get_memory_usage()

    allstat = [
            ('TOTAL',   f'{get_gb_value(total)}',      0) ,
            ('USED',    f'{get_gb_value(used)}',       percent) ,
            ('AVAIL',   f'{get_gb_value(available)}',  100 - percent) ,
            ('%USE%',       f'{percent}',                  0)
            ]

    max_length_label = (max(len(l[0]) for l in allstat))
    max_length_value = (max(len(l[1]) for l in allstat))

    bar_length = max(TTY_Stat.columns() - label_len - value_len - offset,10)

    lines = []
    for label, value, pct in allstat:
        if label == '%USE%' or label == 'TOTAL':
            if label == "%USE%":
                suff = ' %'
            else:
                suff = "gb"
            bar = ui_bar.bar(pct, pct, bar_length, empty_symbol='+')
        else:
            suff = 'gb'
            bar = ui_bar.bar(percent, pct, bar_length)

        lines.append(f'{ui_parts.VERTICAL_L}{label:<{label_len}}{value:>{value_len}}  {suff} {bar}{ui_parts.VERTICAL_L}')

    return '\n'.join(lines)
