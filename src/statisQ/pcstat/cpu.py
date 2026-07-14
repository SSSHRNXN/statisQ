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

bg_color = f'\033[{config.getint("UI", "BG_COLOR")}m'
label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')
empty_symbol = config.get('UI', 'EMPTY_SMBL')


def get_cpu_usage():
    label = "USAGE"
    cpu_usage = psutil.cpu_percent()

    return ui_bar.full_line(label, cpu_usage, int(cpu_usage), "%")

def get_cpu_name():
    with open("/proc/cpuinfo") as file: 
        for line in file:
            if "model name" in line:
                cpu_raw_name = line.split(':')[1].strip()
                cpu_name = cpu_raw_name.split()
                return ' '.join(cpu_name[:4]) 
        else:
            return 'CPU_NAME Not found'


def get_cpu_temp():
    label = "TEMP"

    sens_temps = psutil.sensors_temperatures()
    proc_name = get_cpu_name()
    if "AMD" in proc_name:
        cpu_temp = sens_temps.get('k10temp', [])
    else:
        cpu_temp = sens_temps.get('coretemp', [])

    ctemp = "###"
    for e in cpu_temp:
        if e.label in ('Tctl', 'Tdie', 'Package id 0'):
            ctemp = int(e.current)
            break
    else:
        if cpu_temp:
            ctemp = int(cpu_temp[0].current)


    if ctemp == "###":
        bar_value = 0
        return ui_bar.full_line(label, bar_value, bar_value, "°C", esymbol="+")
    else:
        bar_value = ctemp
        return ui_bar.full_line(label, bar_value, bar_value, "°C")


def get_cpu_freq():
    esymbol = empty_symbol
    label = "FREQ"

    freq = psutil.cpu_freq()
    if freq is None:
        esymbol = "+"
        curr_fq = min_fq = max_fq = 0
        mhz_pct = 0
    else:
        curr_fq, min_fq, max_fq = freq
        mhz_pct = (int(curr_fq) / int(max_fq) * 100)

    return ui_bar.full_line(label, float(f'{curr_fq:.1f}'), int(mhz_pct), "MHz", esymbol=esymbol)

def get_max_cpu_freq():
    label = "MAX_FQ"

    freq = psutil.cpu_freq()
    if freq is None:
        curr_fq = min_fq = max_fq = 0
        mhz_pct = 0
    else:
        curr_fq, min_fq, max_fq = freq
        mhz_pct = (int(curr_fq) / int(max_fq) * 100)
   
    return ui_bar.full_line(label, float(f'{max_fq:.1f}'), 0, "MHz", esymbol="+")

def get_cpu_arch():
    label = "ARCH"
    arch = machine()

    return ui_bar.full_line(label, arch, 0, " ", esymbol="+")

def get_stat():
    lines = []

    lines.append(get_cpu_usage())
    lines.append(get_cpu_temp())
    lines.append(get_cpu_freq())
    lines.append(get_max_cpu_freq())
    lines.append(get_cpu_arch())
    
    return '\n'.join(lines)
