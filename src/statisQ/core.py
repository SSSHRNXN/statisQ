#!/usr/bin/env python3

import os 
import time
import sys

#config
from .cfg import config

#ui
from statisQ.lib.coloropen import TTY_Stat, BG
from .pcstat import mem, cpu, disk
from .ui.ui_hat_bar import top_bar, bot_bar
from .ui import ui_incorrect_render

UPDATE_INTERVAL = config.LOGIC.UPDATE_INTERVAL
MIN_HEIGHT = config.UI.MIN_HEIGHT
MIN_WIDTH = config.UI.MIN_WIDTH

def enable_alt_screen():
    sys.stdout.write('\033[?1049h') #show alt screen
    sys.stdout.write('\033[?25l')   #disable cursor
    sys.stdout.flush()

def disable_alt_screen():
    sys.stdout.write('\033[?25h')  #enable cursor
    sys.stdout.write('\033[?1049l') #disable alt screen
    sys.stdout.flush()

def main():
    enable_alt_screen()
    try:
        while True:
            COLUMNS = TTY_Stat.columns()
            LINES = TTY_Stat.lines()

            if COLUMNS < MIN_WIDTH or LINES < MIN_HEIGHT:
                sys.stdout.write('\033[2J') #term clear
                print(ui_incorrect_render.failed_render_window(COLUMNS, LINES, MIN_WIDTH, MIN_HEIGHT))
            else:
                sys.stdout.write('\033[H')
                #CPU
                print(top_bar("CPU", text=f'{cpu.get_cpu_name()}'))
                print(cpu.get_stat())
                print(bot_bar())
                #RAM
                print(top_bar("RAM", time=True))
                print(mem.get_stat())
                print(bot_bar())
                #disk
                print(top_bar("DISK"))
                print(disk.get_stat())
                print(bot_bar())
                print(bot_bar(f'UPDATE INTERVAL:{UPDATE_INTERVAL}'))
            time.sleep(UPDATE_INTERVAL)
            sys.stdout.write('\033[J')
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        disable_alt_screen()

if __name__ == '__main__':
    main()
