#!/usr/bin/env python3

from platform import machine
from ..lib.coloropen import TTY_Stat
from ..ui import ui_parts, ui_bar
import psutil

label_len = 10
value_len = 6
offset = 7 # count of spaces in f strigs

def ubar(value:int):

    bar_length = max(TTY_Stat.columns() - label_len - value_len - offset, 10)
    bar = ui_bar.bar(value, value, bar_length)

    return bar

def get_cpu_usage():
    label = "USAGE"
    cpu_usage = psutil.cpu_percent()

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {cpu_usage:^{value_len}} {" %"} {ubar(int(cpu_usage))}{ui_parts.VERTICAL_L}'

def get_cpu_temp():
    label = "TEMP"

    sens_temps = psutil.sensors_temperatures()
    cpu_temp = sens_temps.get('k10temp', [])

    ctemp = "###"
    for e in cpu_temp:
        if e.label == 'Tctl':
            ctemp = int(e.current)
            break

    bar_length = max(TTY_Stat.columns() - label_len - value_len - offset, 10)
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
    label = "FREQ"
    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    mhz_pct = int(int(curr_fq) / int(max_fq) * 100)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{int(curr_fq):^{value_len}} {"MHz"} {ubar(int(mhz_pct))}{ui_parts.VERTICAL_L}'

def get_max_cpu_freq():
    label = "MAX_FQ"
    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    
    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{int(max_fq):^{value_len}} {"MHz"} {ubar(int(0))}{ui_parts.VERTICAL_L}'

def get_cpu_arch():
    label = "ARCH"
    arch = machine()

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}} {arch:^{value_len + 4}}{ubar(int(0))}{ui_parts.VERTICAL_L}' 

def get_stat():
    lines = []

    lines.append(get_cpu_usage())
    lines.append(get_cpu_temp())
    lines.append(get_cpu_freq())
    lines.append(get_max_cpu_freq())
    lines.append(get_cpu_arch())
    
    return '\n'.join(lines)
