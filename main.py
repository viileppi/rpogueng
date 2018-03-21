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
keybinds[int(curses.KEY_UP)] = [-1, 0]
keybinds[int(curses.KEY_DOWN)] = [1, 0]
keybinds[int(curses.KEY_LEFT)] = [0, -1]
keybinds[int(curses.KEY_RIGHT)] = [0, 1]
keybinds[ord("k")] = [-1, 0]
keybinds[ord("j")] = [1, 0]
keybinds[ord("h")] = [0, -1]
keybinds[ord("l")] = [0, 1]
keybinds[ord("y")] = [-1, -1]
keybinds[ord("u")] = [-1, 1]
keybinds[ord("b")] = [1, -1]
keybinds[ord("n")] = [1, 1]
keybinds[ord(".")] = [0, 0]
keybinds[ord("m")] = [0, 0, "m"]
keybinds[ord("t")] = [0, 0, "t"]

foo = Display(WIDTH, HEIGHT, keybinds, Map)

wrapper(foo.main)
