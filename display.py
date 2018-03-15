#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level

WIDTH = 40
HEIGHT = 40

p1 = objects.Character(10, 10, "@", curses.A_BOLD, [HEIGHT, WIDTH])
m1 = objects.Monster(random.randint(0, HEIGHT), random.randint(0, WIDTH), "J", curses.A_NORMAL, [HEIGHT, WIDTH])
m2 = objects.Monster(random.randint(0, HEIGHT), random.randint(0, WIDTH), "T", curses.A_NORMAL, [HEIGHT, WIDTH])

lvl = level.Level(HEIGHT, WIDTH)
lvl.wholevel["characters"] = [m1, m2, p1]

class Display:
    ''' foo '''
    def __init__(self, w, h, keybinds):
        self.w = w
        self.h = h
        self.keybinds = keybinds

    def main(self, stdscr):
        self.maxyx = stdscr.getmaxyx()
        self.half_h = self.maxyx[0]
        self.half_w = self.maxyx[1]
        self.x = 10
        self.y = 10
        curses.curs_set(0)
        user_input = ""
        while user_input != "q":
            # draw
            stdscr.clear()
            for tile in lvl.wholevel["tiles"]:
                stdscr.addstr(tile.y, tile.x, tile.char, tile.color)
            for char in lvl.wholevel["characters"]:
                char.ai()
                char.move(lvl)
                stdscr.addstr(char.y, char.x, char.char, char.color)
            stdscr.refresh()
            # input
            user_input = stdscr.getkey()
            try:
                direction = self.keybinds[user_input]
            except KeyError:
                stdscr.addstr(0, 0, "Invalid key: " + user_input)
            p1.direction = direction
            direction = [0, 0]

keybinds = {}   # y  x
keybinds["k"] = [-1, 0]
keybinds["j"] = [1, 0]
keybinds["h"] = [0, -1]
keybinds["l"] = [0, 1]
keybinds["y"] = [-1, -1]
keybinds["u"] = [-1, 1]
keybinds["b"] = [1, -1]
keybinds["n"] = [1, 1]

foo = Display(WIDTH, HEIGHT, keybinds)

wrapper(foo.main)
