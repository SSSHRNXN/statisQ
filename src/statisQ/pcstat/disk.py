#!/usr/bin/env python3 from pathlib import Path

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

def get_disk_total(bar=True, used=False, percent=False,total=False):
    label = "TOTAL"
    suff = "gb"

#    disk_total = f'{(psutil.disk_usage("/").total) / 1e9:.1f}'
    disk_total = disk_usage = disk_usage_prt = 0
    for part in psutil.disk_partitions():
        if 'loop' in part or part.fstype in ('tmpfs', 'devtmpfs', 'squashfs'):
            continue
        usage = psutil.disk_usage(part.mountpoint)
        disk_total += usage.total
        disk_usage += usage.used
        disk_usage_prt += usage.percent

    if bar:
        return ui_bar.full_line(label, str(f'{disk_total / (1024 ** 3):.1f}'), 0, suff, esymbol="+")
    elif used:
        return disk_usage
    elif percent:
        return disk_usage_prt
    elif total:
        return disk_total

def get_disk_usage():
    label = "USAGE(/)"
    suff = "gb"
    
    disk_usage = f'{get_disk_total(bar=False,used=True) / (1024 ** 3):.1f}'
    disk_total = f'{get_disk_total(bar=False,total=True) / (1024 ** 3):.1f}' 
    if disk_usage == 0 or disk_total == 0:
        disk_usage_prt = 0
    else:
        disk_usage_prt = float(disk_usage) / float(disk_total) * 100

    return ui_bar.full_line(label, (disk_usage), int(disk_usage_prt), suff)

def get_disk_usage_prt():
    label = "%USE%"
    suff = "%"

    disk_usage = f'{get_disk_total(bar=False,used=True) / (1024 ** 3):.1f}'
    disk_total = f'{get_disk_total(bar=False,total=True) / (1024 ** 3):.1f}' 
    if disk_usage == 0 or disk_total == 0:
        disk_usage_prt = 0
    else:
        disk_usage_prt = float(disk_usage) / float(disk_total) * 100

    return ui_bar.full_line(label, f'{disk_usage_prt:.1f}', int(disk_usage_prt), suff)

def get_stat():
    lines = []

    lines.append(get_disk_total())
    lines.append(get_disk_usage())
    lines.append(get_disk_usage_prt())

    return '\n'.join(lines)

