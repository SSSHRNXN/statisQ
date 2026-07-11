#!/usr/bin/env python3

from calendar import c

from ..lib.coloropen import TTY_Stat
from ..ui import ui_parts, ui_bar
import psutil

label_len = 12
value_len = 6

def get_cpu_usage():
    label = "CPU_USAGE"

    cpu_usage = psutil.cpu_percent()

    bar_length = max(TTY_Stat.columns() - label_len - value_len - 7, 10)
    bar = ui_bar.bar(cpu_usage, cpu_usage, bar_length)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {cpu_usage:^{value_len}} {" %"} {bar}{ui_parts.VERTICAL_L}' 

def get_cpu_temp():
    label = "CPU_TEMP"

    sens_temps = psutil.sensors_temperatures()
    cpu_temp = sens_temps.get('k10temp', [])

    ctemp = "###"
    for e in cpu_temp:
        if e.label == 'Tctl':
            ctemp = int(e.current)
            break

    bar_length = max(TTY_Stat.columns() - label_len - value_len - 7, 10)
    if ctemp == "###":
        bar = ui_bar.bar(0, 100, bar_length)
    else:
        bar = ui_bar.bar(ctemp, ctemp, bar_length)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {ctemp:^{value_len}} {"°C"} {bar}{ui_parts.VERTICAL_L}'

def get_cpu_name():
    with open("/proc/cpuinfo") as file: 
        for line in file:
            if "model name" in line:
                cpu_raw_name = line.split(':')[1].strip()
                cpu_name = cpu_raw_name.split()
                return ' '.join(cpu_name[:4]) 
        else:
            return 'CPU_NAME Not found'

def get_cpu_freq():
    label = "CPU_FREQ"

    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    mhz_pct = int(int(curr_fq) / int(max_fq) * 100)

    bar_length = max(TTY_Stat.columns() - label_len - value_len - 7, 10)
    bar = ui_bar.bar((mhz_pct), mhz_pct, bar_length)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{int(curr_fq):^{value_len}} {"MHz"} {bar}{ui_parts.VERTICAL_L}'

def get_max_cpu_freq():
    label = "CPU_MAX_FQ"
    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    
    bar_length = max(TTY_Stat.columns() - label_len - value_len - 7, 10)
    bar = ui_bar.bar(0, 0, bar_length)
    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{int(max_fq):^{value_len}} {"MHz"} {bar}{ui_parts.VERTICAL_L}'


def get_stat():
    lines = []

    lines.append(get_cpu_usage())
    lines.append(get_cpu_temp())
    lines.append(get_cpu_freq())
    lines.append(get_max_cpu_freq())
    
    return '\n'.join(lines)
