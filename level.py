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
        a = objects.Tile(0, 0, "basic", [self.h, self.w])
        for i in range(int(h * w / 8)):
            # generate tiles from color range 33...64
            self.level[y][x] = objects.Tile(y, x, a.types[random.randint(0, len(a.types) - 1)], [self.h, self.w])
            self.level[y][x].blocking = True
            y = (y + self.diry[random.randint(0, len(self.diry) - 1)]) % self.h
            x = (x + self.diry[random.randint(0, len(self.diry) - 1)]) % self.w


        self.wholevel = {}
        self.wholevel["tiles"] = []
        self.wholevel["items"] = []
        self.wholevel["characters"] = []
        for row in self.level:
            for col in row:
                if col != None:
                    self.wholevel["tiles"].append(col)

    def blocking(self, y, x):
        ''' returns instance in given coordinates '''
        for keys in self.wholevel:
            for c in self.wholevel[keys]:
                if c.y == y and c.x == x:
                    return c


    def wheres_waldo(self):
        ''' returns players coordinates [y, x] '''
        return [self.wholevel["characters"][0].y, self.wholevel["characters"][0].x]

    def delete(self, name):
        self.wholevel.pop(name)



# foo = Level(8, 8)
# for i in range(8):
#     for k in range(8):
#         print(foo.blocking(i, k))
