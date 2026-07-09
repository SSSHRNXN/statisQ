#!/usr/bin/env python3

from ..lib.coloropen import FG, clog
from ..ui import ui_parts
import psutil

PERSENT_THRESHOLDS = [
        (0, FG.WHITE),
        (30, FG.GREEN),
        (50, FG.YELLOW),
        (80, FG.RED)
        ]

def usage_status_color(percent):
    for threshold, color in PERSENT_THRESHOLDS:
        if percent >= threshold:
            return color
    return FG.WHITE

def get_memory_usage():
    memory_stat = psutil.virtual_memory()
    return memory_stat.total, memory_stat.used, memory_stat.available, memory_stat.percent


total, used, available, percent = get_memory_usage()

def memtotal():
    print(clog(total , level="debug"))   
    print(clog(f'{total / (1024 ** 3):.2f}' , level="debug"))   
    
    color = usage_status_color(percent)
    usage_bar = f'{color}{ui_parts.HORIZONTAL_L * 10}'
    return f'TOTAL: {total / (1024 ** 3):.2f} gb {usage_bar}'


print(memtotal())
