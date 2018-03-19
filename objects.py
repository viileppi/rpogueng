import random
import skills

class Object:
    ''' color = 1...6 '''
    def __init__(self, y, x, c, color, maxyx):
        self.name = ""
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.blocking = False
        self.char = c
        self.color = color
        self.alive = True
        self.action = ""
        self.fight = skills.Skill(3)
        self.hp = 10

    def position(self):
        ''' return position [y, x] '''
        return [self.y, self.x]

    def suicide(self):
        self.alive = False


class Character(Object):
    ''' character class '''

    def move(self, level):
        ''' moves the instance and checks for blocking (bool)
            returns characters action (str) '''
        self.old_x = self.x
        self.old_y = self.y
        newx = self.x
        newy = self.y
        newx = min(self.maxyx[1], newx + self.direction[1])
        newx = max(0, newx)
        newy = min(self.maxyx[0], newy + self.direction[0])
        newy = max(0, newy)
        foo = level.blocking(newy, newx)
        if foo != None and foo != self:
            # for testing-purpose change the character on collision
            self.x = self.old_x
            self.y = self.old_y
            if self.fight.roll(foo.fight.limit):
                foo.hp -= 2
                self.action = "smack!"
                if foo.hp < 1:
                    foo.alive = False
                    foo.char = " "
                    self.action = "hulk smash"
            else:
                self.action = "missed..."
        else:
            self.x = newx
            self.y = newy
            self.action = ""

class Monster(Character):
    ''' NPC-class '''
    def move(self, level):
        ''' moves the instance and checks for blocking (bool)
            with added AI '''
        player = level.wheres_waldo()
        if abs(player[0] - self.y) < 8 and abs(player[1] - self.x) < 8:
            if player[0] < self.y:
                self.direction[0] = -1
            if player[0] > self.y:
                self.direction[0] = 1
            if player[1] < self.x:
                self.direction[1] = -1
            if player[1] > self.x:
                self.direction[1] = 1
        self.old_x = self.x
        self.old_y = self.y
        newx = self.x
        newy = self.y
        newx = min(self.maxyx[1], newx + self.direction[1])
        newx = max(0, newx)
        newy = min(self.maxyx[0], newy + self.direction[0])
        newy = max(0, newy)
        foo = level.blocking(newy, newx)
        if foo != None and foo != self:
            self.x = self.old_x
            self.y = self.old_y
            if self.fight.roll(foo.fight.limit):
                foo.hp -= 2
                self.action = "smack!"
                if foo.hp < 1:
                    foo.alive = False
                    foo.char = " "
                    self.action = "monster smash"
            else:
                self.action = "missed..."
        else:
            self.x = newx
            self.y = newy
            self.action = ""

# if foo != None:
        #     # for testing-purpose change the character on collision
        #     self.x = self.old_x
        #     self.y = self.old_y
        #     # if str(type(foo))[:18] == "<class 'objects.Mo":
        #     #     foo.char = chr(ord(foo.char) + 1)
        # else:
        #     self.x = newx
        #     self.y = newy

class Tile(Object):
    ''' tile class '''
    def __init__(self, y, x, type_of, maxyx):
        skeleton = {}
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.blocking = True
        self.color = 0
        self.alive = False
        self.fight = skills.Skill(100)
        self.hp = 100

        if type_of == 0:
            self.char = "#"
            self.color = random.randint(52, 62)
            self.blocking = True
        if type_of == 1:
            self.char = "Y"
            self.color = random.randint(32, 54)
            self.blocking = True
        if type_of == 2:
            self.char = "~"
            self.color = random.randint(18, 22)
            self.blocking = False
        else:
            self.char = "."
            self.color = 0
            self.blocking = False





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
