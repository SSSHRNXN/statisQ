#!/usr/bin/env python3

from calendar import c

from ..lib.coloropen import FG, TTY_Stat
from ..ui import ui_parts, ui_bar
import psutil

def get_cpu_usage():
    label = "CPU_USAGE"
    label_len = 12
    
    cpu_usage_len = 6
    cpu_usage = psutil.cpu_percent() 

    bar_length = max(TTY_Stat.columns() - label_len - cpu_usage_len - 7, 10)
    bar = ui_bar.bar(cpu_usage, cpu_usage, bar_length)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {cpu_usage:^{cpu_usage_len}} {" %"} {bar}{ui_parts.VERTICAL_L}' 

def get_cpu_temp():
    label = "CPU_TEMP"
    label_len = 12
    cpu_temp_len = 6

    sens_temps = psutil.sensors_temperatures()
    cpu_temp = sens_temps.get('k10temp', [])


    ctemp = "###"
    for e in cpu_temp:
        if e.label == 'Tctl':
            ctemp = int(e.current)
            break

    bar_length = max(TTY_Stat.columns() - label_len - cpu_temp_len - 7, 10)
    if ctemp == "###":
        bar = ui_bar.bar(0, 100, bar_length)
    else:
        bar = ui_bar.bar(ctemp, ctemp, bar_length)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {ctemp:^{cpu_temp_len}} {"°C"} {bar}{ui_parts.VERTICAL_L}'

def get_cpu_name():
    with open("/proc/cpuinfo") as file: 
        for line in file:
            if "model name" in line:
                cpu_raw_name = line.split(':')[1].strip()
                cpu_name = cpu_raw_name.split()
                return ' '.join(cpu_name[:4]) 
        else:
            return 'CPU_NAME Not found'

