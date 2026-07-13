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

    disk_total = f'{(psutil.disk_usage("/").total) / 1e9:.1f}'

    return ui_bar.full_line(label, float(disk_total), 0, suff, esymbol="+")

def get_disk_usage():
    label = "USAGE(/)"
    suff = "gb"

    disk_total = f'{(psutil.disk_usage("/").total) / 1e9:.1f}'
    disk_usage = f'{(psutil.disk_usage("/").used) / 1e9:.1f}'
    disk_usage_prt = int(float(disk_usage) / float(disk_total) * 100)

    return ui_bar.full_line(label, float(disk_usage_prt), disk_usage_prt, suff)

def get_disk_usage_prt():
    label = "%USE%"
    suff = "%"

    disk_pct = (psutil.disk_usage('/').percent)

    return ui_bar.full_line(label, disk_pct, int(disk_pct), suff)

def get_stat():
    lines = []

    lines.append(get_disk_total())
    lines.append(get_disk_usage())
    lines.append(get_disk_usage_prt())

    return '\n'.join(lines)

