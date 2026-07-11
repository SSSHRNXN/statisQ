#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
config_file = Path(__file__).resolve().parents[1] / 'cfg' / 'statisQ.cfg'
config = ConfigParser()
config.read(config_file)

import psutil
from ..ui import ui_bar, ui_parts
from ..lib.coloropen import TTY_Stat

label_len = config.getint('UI', 'LABEL_LEN')
value_len = config.getint('UI', 'VALUE_LEN')
suff_len  = config.getint('UI', 'SUFF_LEN')
offset = config.getint('UI', 'OFFSET')

def get_disk_total():
    label = "TOTAL"
    suff = "gb"

    disk_total = f'{(psutil.disk_usage('/').total) / 1e9:.1f}'

    bar_len = TTY_Stat.columns() - label_len - value_len - suff_len - offset
    bar = ui_bar.bar(0, 0 , bar_len, empty_symbol="+")

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{str(disk_total):>{value_len}} {suff:<{suff_len}}{bar}{ui_parts.VERTICAL_L}'

def get_disk_usage():
    label = "USAGE(/)"
    suff = "gb"

    disk_total = f'{(psutil.disk_usage('/').total) / 1e9:.1f}'
    disk_usage = f'{(psutil.disk_usage('/').used) / 1e9:.1f}'
    disk_usage_prt = int(float(disk_usage) / float(disk_total) * 100)

    bar_len = TTY_Stat.columns() - label_len - value_len - suff_len - offset
    bar = ui_bar.bar(disk_usage_prt, disk_usage_prt , bar_len)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{str(disk_usage):>{value_len}} {suff:<{suff_len}}{bar}{ui_parts.VERTICAL_L}'

def get_disk_usage_prt():
    label = "%USE%"
    suff = "%"

    disk_pct = (psutil.disk_usage('/').percent)

    bar_len = TTY_Stat.columns() - label_len - value_len - suff_len - offset
    bar = ui_bar.bar(disk_pct, disk_pct , bar_len)

    return f'{ui_parts.VERTICAL_L}{label:<{label_len}}{str(disk_pct):>{value_len}} {suff:<{suff_len}}{bar}{ui_parts.VERTICAL_L}'

def get_stat():
    lines = []

    lines.append(get_disk_total())
    lines.append(get_disk_usage())
    lines.append(get_disk_usage_prt())

    return '\n'.join(lines)

