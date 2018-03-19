#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level

class Display:
    ''' foo '''
    def __init__(self, w, h, keybinds, lvl):
        self.w = w
        self.h = h
        self.keybinds = keybinds
        self.Map = lvl
        self.lvl = self.Map.Map[0][0]

    def main(self, mainwin):
        stdscr = mainwin.subwin(self.h + 1, self.w + 1, 1, 0)
        minimap = mainwin.subwin(self.h + 1, self.w + 1, 1, self.w + 1)
        statuswin = mainwin.subwin(1,self.w, 0, 0)
        self.maxyx = stdscr.getmaxyx()
        self.half_h = int(self.h / 2)
        self.half_w = int(self.w / 2)
        self.x = 10
        self.y = 10
        # generating color pairs
        for i in range(1, 256, 1):
                curses.init_pair((i), i, 0)
        curses.curs_set(0)
        user_input = ""
        direction = [0, 0]
        action = " "
        while user_input != "q":
            stdscr.clear()
            del_list = []
            # draw minimap
            for line in self.Map.Map:
                for col in self.Map.Map[line]:
                    minimap.addstr(self.half_h + line, self.half_w + col, "#")
            minimap.addstr(self.Map.y + self.half_h, self.Map.x + self.half_w, "@")
            minimap.border()
            minimap.refresh()
            # draw tiles
            for tile in self.lvl.tiles:
                stdscr.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.color))
            # draw characters
            for index, char in enumerate(self.lvl.characters):
                char.move(self.lvl)
                stdscr.addstr(char.y, char.x, char.char, curses.color_pair(char.color))
                if char.alive == False:
                    del_list.append(index)
            # delete killed characters
            for char in del_list:
                self.lvl.characters.pop(char)
            # show actions
            action = self.lvl.characters[0].action
            statuswin.clear()
            statuswin.addstr(0,0, "HP:" + str(int(self.lvl.characters[0].hp)) + "|" + action)
            stdscr.border()
            stdscr.refresh()
            statuswin.refresh()
            # input
            user_input = stdscr.getkey()
            try:
                direction = self.keybinds[user_input]
            except KeyError:
                stdscr.addstr(0, 0, "Invalid key: " + user_input)
            self.lvl.characters[0].direction = direction

            # move to new levels or make such
            if self.lvl.characters[0].x <= 1:
                self.Map.x -= 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].x = self.lvl.characters[0].maxyx[1] - 1
            if self.lvl.characters[0].x >= self.w:
                self.Map.x += 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].x = 1

            if self.lvl.characters[0].y <= 1:
                self.Map.y -= 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].y = self.lvl.characters[0].maxyx[0] - 1
            if self.lvl.characters[0].y >= self.h:
                self.Map.y += 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].y = 1

            direction = [0, 0]
            # check if player is still alive
            if not self.lvl.characters[0].alive:
                for i in range(self.h):
                    stdscr.addstr(i, i, "GAME OVER!!!")
                    stdscr.refresh()
                    curses.napms(50)
                user_input = "q"
