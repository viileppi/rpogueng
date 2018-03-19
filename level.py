import random
import curses
import objects

class Level:
    ''' level '''
    def __init__(self, h, w):
        ''' make a level '''
        self.h = h
        self.w = w
        self.level = []
        self.diry = [-1, 0, 1]
        for y in range(h):
            row = []
            for x in range(w):
                a = None
                row.append(a)
            self.level.append(row)
        self.y = int(h / 2)
        self.x = int(w / 2)
        for i in range(int(h * w / 8)):
            # generate tiles from color range 33...64
            self.level[y][x] = objects.Tile(y, x, random.randint(0, 3), [self.h, self.w])
            self.level[y][x].blocking = True
            y = (y + self.diry[random.randint(0, len(self.diry) - 1)]) % self.h
            x = (x + self.diry[random.randint(0, len(self.diry) - 1)]) % self.w

        self.tiles = []
        self.items = []
        self.characters = []
        self.wholevel = [self.tiles, self.items, self.characters]
        for row in self.level:
            for col in row:
                if col != None:
                    self.tiles.append(col)

    def blocking(self, y, x):
        ''' returns instance in given coordinates '''
        for keys in self.wholevel:
            for c in keys:
                if c.y == y and c.x == x:
                    return c

    def wheres_waldo(self):
        ''' returns players coordinates [y, x] '''
        return self.characters[0].y, self.characters[0].x
