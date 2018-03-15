import random

class Object:
    ''' base class for everything '''
    def __init__(self, y, x, c, color, maxyx):
        self.name = ""
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.blocking = False
        self.char = c
        self.color = color
        self.alive = None

    def position(self):
        ''' return position [y, x] '''
        return [self.y, self.x]


class Character(Object):
    ''' character class '''
    def ai(self):
        ''' in the player-class ai() does nothing... '''
        pass

    def move(self, level):
        ''' moves the instance and checks for blocking (bool) '''
        self.alive = True
        self.old_x = self.x
        self.old_y = self.y
        newx = self.x
        newy = self.y
        newx = min(self.maxyx[1], newx + self.direction[1])
        newx = max(0, newx)
        newy = min(self.maxyx[0], newy + self.direction[0])
        newy = max(0, newy)
        foo = level.blocking(newy, newx)
        if foo != None:
            # for testing-purpose change the character on collision
            self.x = self.old_x
            self.y = self.old_y
            if str(type(foo))[:18] == "<class 'objects.Mo":
                foo.char = chr(ord(foo.char) + 1)
        else:
            self.x = newx
            self.y = newy

class Monster(Character):
    ''' NPC-class '''
    def ai(self):
        ''' moves randomly NPC '''
        if random.randint(0, 4) == 0:
            self.direction = [random.randint(-1, 1), random.randint(-1, 1)]

class Tile(Object):
    ''' tile class '''
    def __init__(self, y, x, c, color, maxyx):
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.blocking = True
        self.char = c
        self.color = color
        self.alive = False


class Item(Object):
    ''' item class '''
    def __init__(self, y, x, c, color, maxyx):
        self.maxyx = maxyx  # y,x
        self.alive = False
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.blocking = False
        self.char = c
        self.color = color
