#!/usr/bin/env python3

import psutil
from ..ui.ui_bar import full_line, empty_bar
from ..lib.coloropen import FG255, FG
from ..cfg import config


# for laptops:
def get_battery_percent():
    label = "BATT"
    battery_stat = psutil.sensors_battery()
    battery_percent, o, pluged_or_not = battery_stat

    return full_line(label, f'{battery_percent:.1f}', battery_percent, "%", reversed_color=True)

def get_charge_status():

    battery_stat = psutil.sensors_battery()
    batter_percent, o, pluged_or_not = battery_stat
    if pluged_or_not:
        text = 'Charging...'
    else:
        text = 'Not charging.'

    return empty_bar(f'{text:^20}')

def get_stat():
    battery_stat = psutil.sensors_battery()

    lines = []
    if not battery_stat is None:
        lines.append(get_battery_percent())
        lines.append(get_charge_status())

    return '\n'.join(lines)
