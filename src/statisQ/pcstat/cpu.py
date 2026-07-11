#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from platform import machine
from ..lib.coloropen import TTY_Stat
from ..ui import ui_parts, ui_bar
import psutil

label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len = config.getint('UI', 'SUFF_LEN')
offset = 3 # count of spaces in f strigs

def ubar(value:int, label):

    if label == 'MAX_FQ' or label == 'ARCH':
        symbol = "+"
    else:
        symbol = ui_parts.HORIZONTAL_L

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset, 10)
    bar = ui_bar.bar(value, value, bar_length, empty_symbol=symbol)

    return bar

def final_line(label:str, value:float, suff:str, bar_value=None):
    if bar_value is None:
        bar_value = int(value)

    return str(f'{ui_parts.VERTICAL_L}{label:<{label_len}}{value:>{value_len}.1f} {suff:<{suff_len}}{ubar(bar_value, label)}{ui_parts.VERTICAL_L}')

def get_cpu_usage():
    label = "USAGE"
    cpu_usage = psutil.cpu_percent()

    return final_line(label, cpu_usage, "%%")

def get_cpu_temp():
    label = "TEMP"

    sens_temps = psutil.sensors_temperatures()
    cpu_temp = sens_temps.get('k10temp', [])

    ctemp = "###"
    for e in cpu_temp:
        if e.label == 'Tctl':
            ctemp = int(e.current)
            break

    bar_length = max(TTY_Stat.columns() - label_len - value_len - suff_len - offset, 10)
    if ctemp == "###":
        bar = ui_bar.bar(0, 100, bar_length)
    else:
        bar = ui_bar.bar(ctemp, ctemp, bar_length)

    return final_line(label, int(ctemp), "°C")

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

    return final_line(label, mhz_pct, "MHz")

def get_max_cpu_freq():
    label = "MAX_FQ"
    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    
    return final_line(label, max_fq, "MHz", bar_value=0)

def get_cpu_arch():
    label = "ARCH"
    arch = machine()

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{arch:^{value_len + 5}}{ubar(int(0), label)}{ui_parts.VERTICAL_L}' 

def get_stat():
    lines = []

    lines.append(get_cpu_usage())
    lines.append(get_cpu_temp())
    lines.append(get_cpu_freq())
    lines.append(get_max_cpu_freq())
    lines.append(get_cpu_arch())
    
    return '\n'.join(lines)
