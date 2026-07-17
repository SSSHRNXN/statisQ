#!/usr/bin/env python3

import psutil
import time

from ..ui import ui_bar

def uptime():
    uptime_full = int(time.time() - psutil.boot_time())
    days = uptime_full // 86400
    hours = (uptime_full % 86400) // 3600
    mins = (uptime_full % 3600) // 60
    sec = uptime_full % 60

    return ui_bar.empty_bar(f'Uptime: {days}d {hours}h {mins}m {sec}s')
