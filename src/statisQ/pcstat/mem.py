#!/usr/bin/env python3

from webbrowser import get

from ..lib.coloropen import FG, clog
from ..ui import ui_parts
import psutil



def get_memory_usage():
    memory_stat = psutil.virtual_memory()
    return memory_stat.total, memory_stat.used, memory_stat.available, memory_stat.percent

total, used, available, percent = get_memory_usage()

def get_gb_value(value):
    return f'{value / (1024 ** 3):.2f}'

PERSENT_THRESHOLDS = [
        (0, FG.WHITE),
        (30, FG.GREEN),
        (50, FG.YELLOW),
        (80, FG.RED)
        ]

def usage_status_color(percent):
    for threshold, color in reversed(PERSENT_THRESHOLDS):
        if percent >= threshold:
            return color

def usage_bar(value, length=15):
    bar_color = usage_status_color(percent)
    filled = value * length // 100
    empty = length - filled
    return f'{bar_color}{ui_parts.HORIZONTAL_L * int(filled)}{FG.WHITE}{ui_parts.HORIZONTAL_L * int(empty)}{FG.RESET}'

def memfullstat():
    allstat = [
            ('TOTAL:',      f'{get_gb_value(total)}',       100,            usage_bar(100)) , 
            ('USED:',       f'{get_gb_value(used)}',        percent,        usage_bar(percent)) , 
            ('AVAILABLE:',  f'{get_gb_value(available)}',   100 - percent,  usage_bar(100 - percent)) , 
            ('PERCENT:',    f'{percent}%',                  '',         '')
            ]

    max_length_label = (max(len(l[0]) for l in allstat))
    max_length_value = (max(len(l[1]) for l in allstat))

    for label, value, percen, bar in allstat:
        print(f'{label} {value} {percen} {bar}')

memfullstat()
