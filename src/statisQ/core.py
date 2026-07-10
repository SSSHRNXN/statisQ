#!/usr/bin/env python3

import os 
import time
import sys
from .pcstat import mem
from .ui.ui_hat_bar import top_bar, bot_bar

UPDATE_INTERVAL = 1

def enable_alt_screen():
    sys.stdout.write('\033[?1049h')
    sys.stdout.flush()

def disable_alt_screen():
    sys.stdout.write('\033[?1049l')
    sys.stdout.flush()

def main():
    try:
        while True:
            os.system('clear')

            print(top_bar("RAM"))
            #statistic
            print(mem.get_stat())
            #statistic
            print(bot_bar())
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    enable_alt_screen()
    main()
    disable_alt_screen()
