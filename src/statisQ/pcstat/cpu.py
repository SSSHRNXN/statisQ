#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

from platform import machine
from ..lib.coloropen import TTY_Stat, BG
from ..ui import ui_parts, ui_bar
import psutil

bg_color = f'\033[{config.getint('UI', 'BG_COLOR')}m'
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')


def get_cpu_usage():
    label = "USAGE"
    cpu_usage = psutil.cpu_percent()

    return ui_bar.full_bar(label, cpu_usage, "%")

def get_cpu_temp():
    label = "TEMP"

    sens_temps = psutil.sensors_temperatures()
    cpu_temp = sens_temps.get('k10temp', [])

    ctemp = "###"
    for e in cpu_temp:
        if e.label == 'Tctl':
            ctemp = int(e.current)
            break

    if ctemp == "###":
        bar_value = 0
    else:
        bar_value = ctemp

    return ui_bar.full_bar(label, bar_value, "°C")

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
    mhz_pct = int(curr_fq) / int(max_fq) * 100

    return ui_bar.full_bar(label, mhz_pct, "MHz")

def get_max_cpu_freq():
    label = "MAX_FQ"
    curr_fq, min_fq, max_fq = psutil.cpu_freq()
    
    return ui_bar.full_bar(label, max_fq, "MHz", esymbol="+", bar_value=0)

def get_cpu_arch():
    label = "ARCH"
    arch = machine()

    return ui_bar.full_bar(label, 0, "  ", str_value=arch, esymbol="+")

def get_stat():
    lines = []

    lines.append(get_cpu_usage())
    lines.append(get_cpu_temp())
    lines.append(get_cpu_freq())
    lines.append(get_max_cpu_freq())
    lines.append(get_cpu_arch())
    
    return '\n'.join(lines)
