#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level
from display import Display

WIDTH = 80
HEIGHT = 40
lvl = level.Level(HEIGHT, WIDTH)

p1 = objects.Character(10, 10, "@", 0, [HEIGHT, WIDTH])
lvl.wholevel["characters"].append(p1)
for i in range(8):
    lvl.wholevel["characters"].append(objects.Monster(random.randint(0, HEIGHT), random.randint(0, WIDTH), "T", random.randint(1, 8), [HEIGHT, WIDTH]))


keybinds = {}   # y  x
keybinds["k"] = [-1, 0]
keybinds["j"] = [1, 0]
keybinds["h"] = [0, -1]
keybinds["l"] = [0, 1]
keybinds["y"] = [-1, -1]
keybinds["u"] = [-1, 1]
keybinds["b"] = [1, -1]
keybinds["n"] = [1, 1]

foo = Display(WIDTH, HEIGHT, keybinds, lvl, p1)

wrapper(foo.main)
