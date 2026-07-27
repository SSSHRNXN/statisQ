#!/usr/bin/env python3

class UI():

    LABEL_LEN = 6
    VALUE_LEN = 8
    SUFF_LEN = 4
    OFFSET = 5
    TEXT_OFFSET = 22

    MIN_HEIGHT = 21
    MIN_WIDTH = 35

    class COLORS():
        #UI colors
        BG = 231
        TEXT = 232
        BG_LINE = 239
        LINE = 111

        #status bar color
        LOW = 45 
        MID = 40
        HIGH = 220
        FULL = 196
        EMPTY_COLOR = 98

    FILLED_SMBL = "+"
    EMPTY_SMBL = "─"

class LOGIC(): 

    UPDATE_INTERVAL = 1
