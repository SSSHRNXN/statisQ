#!/usr/bin/env python3 

from ..cfg import config
from ..lib.coloropen import BG255, BG, FG255

#bg_color = f'\033[{config.UI.BG_LINE_COLOR}m'
bg_color = BG255(config.UI.COLORS.BG_LINE)
line_color = FG255(config.UI.COLORS.LINE)

CORNER_TL = f'{bg_color}{line_color}{"╭"}{BG.RESET}'
CORNER_TR = f'{bg_color}{line_color}{"╮"}{BG.RESET}'
CORNER_BL = f'{bg_color}{line_color}{"╰"}{BG.RESET}'
CORNER_BR = f'{bg_color}{line_color}{"╯"}{BG.RESET}'
HORIZONTAL_L = f'{bg_color}{line_color}{"─"}{BG.RESET}'
VERTICAL_L = f'{bg_color}{line_color}{"│"}{BG.RESET}'
JOIN_RIGHT_L = f'{bg_color}{line_color}{"├"}{BG.RESET}'
JOIN_LEFT_L = f'{bg_color}{line_color}{"┤"}{BG.RESET}'


nCORNER_TL = "╭"
nCORNER_TR = "╮"
nCORNER_BL = "╰"
nCORNER_BR = "╯"
nHORIZONTAL_L = "─"
nVERTICAL_L = "│"
nJOIN_RIGHT_L = "├"
nJOIN_LEFT_L = "┤"
