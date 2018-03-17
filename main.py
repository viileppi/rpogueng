#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level
from display import Display

WIDTH = 40
HEIGHT = 20

p1 = objects.Character(10, 10, "@", 1, [HEIGHT, WIDTH])
m1 = objects.Monster(random.randint(0, HEIGHT), random.randint(0, WIDTH), "J", 2, [HEIGHT, WIDTH])
m2 = objects.Monster(random.randint(0, HEIGHT), random.randint(0, WIDTH), "T", 3, [HEIGHT, WIDTH])

lvl = level.Level(HEIGHT, WIDTH)
lvl.wholevel["characters"] = [m1, m2, p1]

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
