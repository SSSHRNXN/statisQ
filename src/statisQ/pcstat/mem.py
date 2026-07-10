#!/usr/bin/env python3

from ..lib.coloropen import FG, TTY_Stat, clog, BG
from ..ui import ui_parts
import psutil



def get_memory_usage():
    memory_stat = psutil.virtual_memory()
    return memory_stat.total, memory_stat.used, memory_stat.available, memory_stat.percent

def get_gb_value(value):
    return f'{value / (1024 ** 3):.1f}'

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

def usage_bar(percent_for_color, value, length=10):
    bar_color = usage_status_color(percent_for_color)
    filled = value * length // 100
    empty = length - filled
    return f'{bar_color}{"+" * int(filled)}{BG.RESET}{FG.GRAY}{ui_parts.HORIZONTAL_L * int(empty)}{FG.RESET}'

def get_stat():
    total, used, available, percent = get_memory_usage()

    allstat = [
            ('TOTAL',      f'{get_gb_value(total)}',      100) , 
            ('USED',       f'{get_gb_value(used)}',       percent) , 
            ('AVAILABLE',  f'{get_gb_value(available)}',  100 - percent) , 
            ('%USE%',      f'{percent}',                  None)
            ]

    max_length_label = (max(len(l[0]) for l in allstat))
    max_length_value = (max(len(l[1]) for l in allstat))

    bar_length = max(TTY_Stat.columns() - max_length_value - max_length_label - 8,10)

    lines = []
    for label, value, pct in allstat:
        if label == '%USE%':
            suff = ' %'
            bar = f'{(" " * bar_length)}'
        else:
            suff = 'gb'
            bar = usage_bar(percent, pct, bar_length)

        lines.append(f'{ui_parts.VERTICAL_L}{label:<{max_length_label + 1}} {value:>{max_length_value}}{FG.RESET} {suff} {bar}{ui_parts.VERTICAL_L}')

    return '\n'.join(lines)
