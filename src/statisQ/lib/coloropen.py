#!/usr/bin/env python3

#ver 0.0.1

from datetime import date, datetime
import shutil
import re

ANSI_base = '\033['

class ANSI_Code_output():
    def __init__(self):
        for name_code, value in vars(self.__class__).items():
            if isinstance(value, int) and not name_code.startswith("_"):
                setattr(self, name_code, f'{ANSI_base}{value}m')


class TTY_Stat():
    #constant
    COLUMNS, LINES = shutil.get_terminal_size()

    @classmethod
    def columns(cls):
        return shutil.get_terminal_size().columns

    @classmethod
    def lines(cls):
        return shutil.get_terminal_size().lines

        
class ANSI_Codes_Foreground(ANSI_Code_output):

    # Standart
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37

    # Bright Standart not for stupid terminals and term env
    GRAY = 90
    LIGHTRED = 91
    LIGHTGREEN = 92
    LIGHTYELLOW = 93
    LIGHTBLUE = 94
    LIGHTPURPLE = 95
    LIGHTCYAN = 96
    LIGHTWHITE = 97

    RESET = 0

class ANSI_Codes_Background(ANSI_Code_output):

    # Standart
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47

    # Bright Standart not for stupid terminals and term env
    GRAY = 100
    LIGHTRED = 101
    LIGHTGREEN = 102
    LIGHTYELLOW = 103
    LIGHTBLUE = 104
    LIGHTPURPLE = 105
    LIGHTCYAN = 106
    LIGHTWHITE = 107

    RESET = 0


class TEXT_STYLE(ANSI_Code_output):

    BOLD = 1 
    DIM = 2 
    ITALIC = 3 
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    OVERLINE = 53

    RESET = 0


def Foreground_255Colors(color_value):
    if color_value > 255:
        invalid_value = f'{FG.RED}{ST.UNDERLINE}{ST.ITALIC}color_value = {color_value}{FG.RESET}'
        return f'{FG.RED}IndexError: {invalid_value}{FG.RED} . Index out of range 1-255'
    elif color_value < 1:
        invalid_value = f'{FG.RED}{ST.UNDERLINE}{ST.ITALIC}color_value = {color_value}{FG.RESET}'
        return f'{FG.RED}IndexError: {invalid_value}{FG.RED} . Index out of range 1-255'
    else:
        return f'{ANSI_base}38;5;{color_value}m'

def Background_255Colors(color_value):
    if color_value > 255:
        invalid_value = f'{FG.RED}{ST.UNDERLINE}{ST.ITALIC}color_value = {color_value}{FG.RESET}'
        return f'{FG.RED}IndexError: {invalid_value}{FG.RED} . Index out of range 1-255'
    elif color_value < 1:
        invalid_value = f'{FG.RED}{ST.UNDERLINE}{ST.ITALIC}color_value = {color_value}{FG.RESET}'
        return f'{FG.RED}IndexError: {invalid_value}{FG.RED} . Index out of range 1-255'
    else:
        return f'{ANSI_base}48;5;{color_value}m'

BG = ANSI_Codes_Background()
FG = ANSI_Codes_Foreground()
ST = TEXT_STYLE()
FG255 = Foreground_255Colors
BG255 = Background_255Colors

def ColorLogger(message, level="INF"):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_levels = {
            'INFO' : FG.GREEN,
            'INF' : FG.GREEN,
            'WARNING' : FG.YELLOW,
            'ERROR' : FG.RED,
            'CRITICAL' : FG.RED + ST.BLINK + ST.BOLD + ST.UNDERLINE,
            'DEBUG' : FG.GRAY
            }

    lenghlevel = len(max(log_levels, key=len))
    color = log_levels.get(level.upper(), FG.WHITE)
    if level.upper() == "CRITICAL":
        return f'{FG.CYAN}[{date}]  {color}{level.upper():^{lenghlevel}}{FG.RESET}  {color}{message}{FG.RESET}'
    else:
        return f'{FG.CYAN}[{date}] {color}[{level.upper():^{lenghlevel - 1}}] {message}{FG.RESET}'

clog = ColorLogger


def ansi_stripper(text_message):
    return re.sub(r'\033\[[0-9;]*m', '', text_message)

class Text_Alignment():

    def CENTER(message, borders=False,  cut=False, debug=False, shift_value=TTY_Stat.COLUMNS):
        message_len = len(ansi_stripper(str(message)))

        if borders:
            print("─" * TTY_Stat.COLUMNS)
        
        number_of_spaces = (((TTY_Stat.COLUMNS) // 2 ) - message_len // 2 ) 
        if number_of_spaces <= 0:
            number_of_spaces = 0
            number_of_spaces += 1

        message_formating = f'{" " * number_of_spaces}'

        if len(str(message)) > shift_value:
            cut_value = shift_value - 2
            if cut:
                message_cut = str(message)[:cut_value]
                print(f'{message_formating}{message_cut[:-2]}{ST.REVERSE}*>{FG.RESET}')
            else:
                for i in range(0, len(str(message)), cut_value):
                    print(f'{message_formating}{str(message)[i:i+cut_value]}')

        else:
            print(f'{message_formating}{message}{FG.RESET}')

        if borders:
            print("─" * TTY_Stat.COLUMNS)
       
        if debug:
                print('COLUMNS:', TTY_Stat.COLUMNS,'LINES:', TTY_Stat.LINES, f'Center alignment work in progress')
                print(clog(f'number_of_spaces: {len(message_formating)}', level="DEBUG"))
                print(clog(f'message len() (includes ANSI): {len(str(message))}', level="DEBUG"))
                print(clog(f'message len() (without ANSI):  {message_len}', level="DEBUG"))
                print(clog(f'shift_value: {shift_value}', level= "DEBUG"))
                if cut:
                    cut_status = "ON"
                else:
                    cut_status = "OFF"
                print(clog(f'cut_mode: {cut_status}', level="DEBUG"))

ALIGN = Text_Alignment
