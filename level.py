import random
import curses
import objects

class Level:
    ''' level '''
    def __init__(self, h, w):
        ''' make a level '''
        self.bln = True
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

    def hostiles(self, y, x):
        ''' returns instance in given coordinates '''
        for i in range(1, len(self.characters), 1):
            c = self.characters[i]
            if c.state == "fight":
                if abs(c.y - y) < 4 and abs(c.x - x) < 4:
                    return c

    def anyHostiles(self):
        ''' returns True if there's any hostiles '''
        r = False
        for i in range(1, len(self.characters), 1):
            c = self.characters[i]
            if c.state == "fight":
                r = True
        return r

    def wheres_waldo(self):
        ''' returns players coordinates [y, x] '''
        return self.characters[0].y, self.characters[0].x

class Map(Level):
    ''' the whole wide world '''
    def __init__(self, l_h, l_w):
        self.Map = {}
        self.Map[0] = {}
        self.Map[0][0] = Level(l_h, l_w)
        self.num_levels = 3
        self.x = 0
        self.y = 0
        self.h = l_h
        self.w = l_w
        self.p1 = objects.Character(10, 10, "@", [l_h, l_w])
        self.p1.color = 0
        self.p1.hp = 30
        self.p1.max_hp = 30
        self.Map[self.y][self.x].characters.append(self.p1)
        for i in range(3):
            self.Map[self.y][self.x].characters.append(objects.Monster(random.randint(0, self.h), random.randint(0, self.w), chr(random.randint(65, 100)), [self.h, self.w]))

    def newLevel(self):
        ''' makes a new level to map '''
        self.num_levels = self.num_levels + 1
        if self.Map.get(self.y) == None:
            self.Map[self.y] = {}
        if self.Map[self.y].get(self.x) == None:
            self.Map[self.y][self.x] = Level(self.h, self.w)
            self.Map[self.y][self.x].characters.append(self.p1)
            for i in range(int(self.num_levels)):
                self.Map[self.y][self.x].characters.append(objects.Monster(random.randint(0, self.h), random.randint(0, self.w), chr(random.randint(65, 100)), [self.h, self.w]))
        return self.Map[self.y][self.x]
