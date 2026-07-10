#!/usr/bin/env python3

import os 
import time
import sys

from statisQ.lib.coloropen import TTY_Stat
from .pcstat import mem, cpu
from .ui.ui_hat_bar import top_bar, bot_bar
from .ui import ui_incorrect_render

UPDATE_INTERVAL = 1
MIN_HEIGHT = 21
MIN_WIDTH = 35

def enable_alt_screen():
    sys.stdout.write('\033[?1049h')
    sys.stdout.flush()

def disable_alt_screen():
    sys.stdout.write('\033[?1049l')
    sys.stdout.flush()

def main():
    try:
        while True:
            COLUMNS = TTY_Stat.columns()
            LINES = TTY_Stat.lines()

            if COLUMNS < MIN_WIDTH or LINES < MIN_HEIGHT:
                os.system('clear')
                print(ui_incorrect_render.failed_render_window(COLUMNS, LINES, MIN_WIDTH, MIN_HEIGHT))
            else:
                sys.stdout.write('\033[H')
                #RAM
                print(top_bar("RAM", time=True))
                print(mem.get_stat())
                print(bot_bar())
                #CPU
                print(top_bar("CPU"))
                print(cpu.get_cpu_usage())
                print(bot_bar())
            time.sleep(UPDATE_INTERVAL)
            sys.stdout.write('\033[J')
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    enable_alt_screen()
    main()
    disable_alt_screen()
