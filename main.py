#!/usr/bin/python3
from curses import wrapper
import curses
import pickle
import level
from display import Display

# def main(scr):
#     ''' get the size of the console '''
#     WIDTH = scr.getmaxyx()[1] - 2
#     HEIGHT = scr.getmaxyx()[0] - 2
#     return WIDTH, HEIGHT
#
# WIDTH, HEIGHT = wrapper(main)
WIDTH, HEIGHT = 36, 20

Map = level.Map(HEIGHT, WIDTH)
keybinds = {}   # y  x
keybinds["KEY_UP"] = [-1, 0]
keybinds["KEY_DOWN"] = [1, 0]
keybinds["KEY_LEFT"] = [0, -1]
keybinds["KEY_RIGHT"] = [0, 1]
keybinds[("k")] = [-1, 0]
keybinds[("j")] = [1, 0]
keybinds[("h")] = [0, -1]
keybinds[("l")] = [0, 1]
keybinds[("y")] = [-1, -1]
keybinds[("u")] = [-1, 1]
keybinds[("b")] = [1, -1]
keybinds[("n")] = [1, 1]
keybinds[(".")] = [0, 0]
keybinds[("m")] = [0, 0, "m"]
keybinds[("t")] = [0, 0, "t"]
keybinds[("?")] = [0, 0, "?"]

foo = Display(WIDTH, HEIGHT, keybinds, Map)

wrapper(foo.main)
