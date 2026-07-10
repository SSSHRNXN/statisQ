#!/usr/bin/env python3

import os 
import time
from .pcstat import mem
from .ui.ui_hat_bar import top_bar, bot_bar

UPDATE_INTERVAL = 1


def main():
    try:
        while True:
            os.system('clear')

            print(top_bar())
            #statistic
            mem.get_stat()
            #statistic
            print(bot_bar())

            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
