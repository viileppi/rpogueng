#!/usr/bin/python3
import os
import curses
from curses import wrapper
import pickle
import objects
import random
import level
from display import Display

# def main(scr):
#     ''' get the size of the console '''
#     WIDTH = scr.getmaxyx()[1] - 1
#     HEIGHT = scr.getmaxyx()[0] - 1
#     return WIDTH, HEIGHT
#
# WIDTH, HEIGHT = wrapper(main)
WIDTH, HEIGHT = 40, 20

Map = level.Map(HEIGHT, WIDTH)

keybinds = {}   # y  x
keybinds["k"] = [-1, 0]
keybinds["j"] = [1, 0]
keybinds["h"] = [0, -1]
keybinds["l"] = [0, 1]
keybinds["y"] = [-1, -1]
keybinds["u"] = [-1, 1]
keybinds["b"] = [1, -1]
keybinds["n"] = [1, 1]

foo = Display(WIDTH, HEIGHT, keybinds, Map)

wrapper(foo.main)
