#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level

class Display:
    ''' foo '''
    def __init__(self, w, h, keybinds, lvl, player):
        self.w = w
        self.h = h
        self.keybinds = keybinds
        self.lvl = lvl
        self.player = player

    def main(self, stdscr):
        self.maxyx = stdscr.getmaxyx()
        self.half_h = self.maxyx[0]
        self.half_w = self.maxyx[1]
        self.x = 10
        self.y = 10
        # generating color pairs
        for i in range(1, 64, 1):
                curses.init_pair((i), i, 0)
        curses.curs_set(0)
        user_input = ""
        direction = [0, 0]
        action = " "
        while user_input != "q":
            # draw
            stdscr.clear()
            del_list = []
            for tile in self.lvl.wholevel["tiles"]:
                stdscr.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.color))
            for index, char in enumerate(self.lvl.wholevel["characters"]):
                char.move(self.lvl)
                stdscr.addstr(char.y, char.x, char.char, curses.color_pair(char.color))
                if char.alive == False:
                    del_list.append(index)
            for char in del_list:
                self.lvl.wholevel["characters"].pop(char)
            stdscr.addstr(0,0, action, curses.color_pair(1))
            stdscr.refresh()
            # input
            user_input = stdscr.getkey()
            try:
                direction = self.keybinds[user_input]
            except KeyError:
                stdscr.addstr(0, 0, "Invalid key: " + user_input)
            self.player.direction = direction
            direction = [0, 0]
