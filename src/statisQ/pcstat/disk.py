#!/usr/bin/env python3

import psutil
from ..ui import ui_bar

label_len = 12
value_len = 2

def get_disk_usage():
    label = "TOTAL"



    disk_total = f'{(psutil.disk_usage('/').total) / 1e9:.1f}'

    return str(disk_total)

def get_stat():
    lines = []

    lines.append(get_disk_usage())

    return '\n'.join(lines)

