#!/usr/bin/env python3

import psutil

from ..cfg import config
from ..ui import ui_bar

def uptime():
    uptime = psutil.boot_time()

    return uptime
