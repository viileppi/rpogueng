#!/usr/bin/python3
import curses
from curses import wrapper
import pickle
import objects
import random
import level
from helper import showHelp

class Display:
    ''' foo '''
    def __init__(self, w, h, keybinds, lvl):
        self.w = w
        self.h = h
        self.keybinds = keybinds
        self.Map = lvl
        self.lvl = self.Map.Map[0][0]
        self.del_list = []

    def showMap(self):
        minimap = curses.newwin(self.h + 1, self.w + 1, 1, 0)
        # draw minimap
        for line in self.Map.Map:
            for col in self.Map.Map[line]:
                if self.Map.Map[line][col].anyHostiles():
                    minimap.addstr(self.half_h + line, self.half_w + col, "#", curses.color_pair(1))
                    minimap.addstr(self.Map.y + self.half_h, self.Map.x + self.half_w, "@", curses.color_pair(1))
                else:
                    minimap.addstr(self.half_h + line, self.half_w + col, "#", curses.color_pair(2))
                    minimap.addstr(self.Map.y + self.half_h, self.Map.x + self.half_w, "@", curses.color_pair(2))
        minimap.addstr(1,1, "Map", curses.color_pair(1))
        minimap.border()
        minimap.refresh()
        minimap.getkey()
        minimap.clear()
        del minimap

    def handleIO(self):
        p1 = self.lvl.characters[0]
        # move to new levels or make such

        if p1.x <= 0:
            # going from right to left
            self.Map.x -= 1
            self.lvl = self.Map.newLevel()
            p1.x = self.lvl.w 

        elif p1.x >= self.w:
            # going from left to right
            self.Map.x += 1
            self.lvl = self.Map.newLevel()
            self.lvl.characters[0].x = 0

        if p1.y <= 0:
            self.Map.y -= 1
            self.lvl = self.Map.newLevel()
            p1.y = self.lvl.h 

        elif p1.y >= self.h:
            self.Map.y += 1
            self.lvl = self.Map.newLevel()
            p1.y = 0


        # check if player is still alive
        if not p1.alive:
            self.stdscr.addstr(self.half_h, self.half_w, "GAME OVER!!!")
            self.stdscr.refresh()
            self.stdscr.getkey()
            user_input = "q"

    def draw(self, direction):
        # draw tiles
        p1 = self.lvl.characters[0]
        p1.direction = direction
        self.stdscr.erase()
        self.statuswin.erase()
        for tile in self.lvl.tiles:
            self.stdscr.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.color))
            self.stdscr.noutrefresh()
        # draw characters
        for index, char in enumerate(self.lvl.characters):
            char.move(self.lvl)
            char.direction = [0, 0]
            if char.action != "":
                self.logwin.addstr(char.action + "\n")
                self.logwin.noutrefresh()
                char.action = ""
            try:
                # self.stdscr.addstr(erase_y, erase_x, " ")
                self.stdscr.addstr(char.y, char.x, char.char, curses.color_pair(char.color))
                self.stdscr.noutrefresh()
            except curses.error:
                pass
            if char.alive == False:
                self.del_list.append(index)
                self.logwin.addstr(char.name + " died...\n")
                self.logwin.noutrefresh()
        # delete killed characters
        for char in self.del_list:
            try:
                # self.stdscr.delch(self.lvl.characters[char].y, self.lvl.characters[char].x)
                self.lvl.characters.pop(char)
            except IndexError:
                pass
        self.del_list = []
        self.statuswin.addstr("HP:" + str(int(self.lvl.characters[0].hp)))
        self.statuswin.noutrefresh()
        curses.doupdate()
        # input

    def main(self, mainwin):
        mainwin.keypad(1)
        showHelp(mainwin)
        mainwin.vline(0, self.w + 1, "|", self.h)
        mainwin.refresh()
        self.stdscr = mainwin.subwin(self.h + 1, self.w + 1, 1, 0)
        self.stdscr.idcok(False)
        self.stdscr.idlok(False)
        self.statuswin = mainwin.subwin(1,self.w, 0, 0)
        self.logwin = mainwin.subpad(self.h, self.w, 1, self.w + 2)
        self.logwin.scrollok(True)
        self.maxyx = self.stdscr.getmaxyx()
        self.half_h = int(self.h / 2)
        self.half_w = int(self.w / 2)
        self.x = 10
        self.y = 10
        # generating color pairs
        for fg in range(1, 8, 1):
            try:
                curses.init_pair((fg), fg, 0)
            except curses.error:
                pass
        curses.curs_set(0)
        user_input = ""
        direction = [0, 0]
        action = "\n"
        action_list = []
        # mainloop
        while user_input != "q":
            self.handleIO()
            self.draw(direction)
            user_input = mainwin.getkey()
            try:
                direction = self.keybinds[user_input]
            except KeyError:
                self.logwin.addstr("Invalid key: " + user_input + "\n", curses.color_pair(1))
                self.logwin.noutrefresh()
            if len(direction) == 3:
                if direction[2] == "m":
                    self.showMap()
                if direction[2] == "t":
                    self.lvl.characters[0].talk(self.lvl)
                    self.logwin.addstr("You talk\n")
                    self.logwin.noutrefresh()
                if direction[2] == "?":
                    showHelp(mainwin)

