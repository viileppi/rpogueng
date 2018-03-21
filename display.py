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

    def showHelp(self):
        f = open("help.txt", "r")
        hjelp = []
        for line in f:
            hjelp.append(line)
        f.close()
        helpwin = curses.initscr()
        try:
            for line in hjelp:
                helpwin.addstr(line)
        except curses.error:
            pass
        helpwin.refresh()
        helpwin.getkey()
        helpwin.clear()
        helpwin.refresh()
        del helpwin


    def main(self, mainwin):
        self.showHelp()
        stdscr = mainwin.subwin(self.h + 1, self.w + 1, 1, 0)
        stdscr.idcok(True)
        stdscr.idlok(1)
        statuswin = mainwin.subwin(1,self.w, 0, 0)
        logwin = mainwin.subwin(self.h + 1, self.w + 1, 1, self.w + 1)
        logwin.scrollok(True)
        logwin.idcok(True)
        logwin.idlok(1)
        self.maxyx = stdscr.getmaxyx()
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
        action = ""
        action_list = []

        while user_input != ord("q"):
            # show actions
            stdscr.clearok(1)
            logwin.clearok(1)
            del_list = []
            # draw tiles
            for tile in self.lvl.tiles:
                stdscr.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.color))
            # draw characters
            for index, char in enumerate(self.lvl.characters):
                erase_y, erase_x = char.move(self.lvl)
                char.direction = [0, 0]
                if char.action != "":
                    action_list.append(char.action)
                    char.action = ""
                try:
                    stdscr.addstr(erase_y, erase_x, " ")
                    stdscr.addstr(char.y, char.x, char.char, curses.color_pair(char.color))
                except curses.error:
                    pass
                if char.alive == False or char.hp < 1:
                    del_list.append(index)
                    action_list.append(char.char + " died...")
            # delete killed characters
            for char in del_list:
                try:
                    stdscr.delch(self.lvl.characters[char].y, self.lvl.characters[char].x)
                    self.lvl.characters.pop(char)
                except IndexError:
                    pass
            # iterate action_list and put them in to logwin
            for action in action_list:
                logwin.addstr(action + "\n")
            statuswin.addstr(0,0, "HP:" + str(int(self.lvl.characters[0].hp)))
            stdscr.border()
            stdscr.noutrefresh()
            statuswin.noutrefresh()
            logwin.noutrefresh()
            curses.doupdate()
            # input
            user_input = (stdscr.getch())
            try:
                direction = self.keybinds[user_input]
                if len(direction) == 3:
                    if direction[2] == "m":
                        self.showMap()
                    if direction[2] == "t":
                        self.lvl.characters[0].talk(self.lvl)
            except KeyError:
                stdscr.addstr(0, 0, "Invalid key: " + chr(user_input))
            self.lvl.characters[0].direction = direction
            # move to new levels or make such
            if self.lvl.characters[0].x <= 1:
                self.Map.x -= 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].x = self.lvl.characters[0].maxyx[1] - 1
                stdscr.clear()
                stdscr.refresh()
            if self.lvl.characters[0].x >= self.w:
                self.Map.x += 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].x = 1
                stdscr.clear()
                stdscr.refresh()
            if self.lvl.characters[0].y <= 1:
                self.Map.y -= 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].y = self.lvl.characters[0].maxyx[0] - 1
                stdscr.clear()
                stdscr.refresh()
            if self.lvl.characters[0].y >= self.h:
                self.Map.y += 1
                self.lvl = self.Map.newLevel()
                self.lvl.characters[0].y = 1
                stdscr.clear()
                stdscr.refresh()

            direction = [0, 0]
            # check if player is still alive
            if not self.lvl.characters[0].alive:
                stdscr.addstr(self.half_h, self.half_w, "GAME OVER!!!")
                stdscr.noutrefresh()
                curses.napms(2000)
                user_input = "q"
