import random
import skills

class Object:
    ''' color = 1...6 '''
    def __init__(self, y, x, c, maxyx):
        self.name = ""
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.blocking = False
        self.char = c
        self.color = 0
        self.alive = True
        self.action = ""
        self.fight = skills.Skill(3)
        self.max_hp = 10
        self.hp = 10
        self.sens = random.randint(8, 22)
        self.turns = 0
        self.reaction = {-1: None,
                         0: None,
                         1: None}
        self.act = ["fight", "flee", "ignore", "like"]
        for key in self.reaction:
            r = random.randint(0, 10)
            if r < 5:
                self.reaction[key] = self.act[0]    # fight
            elif r >= 5 and r < 7:
                self.reaction[key] = self.act[1]    # flee
            elif r >= 7 and r < 9:
                self.reaction[key] = self.act[2]    # ignore
            elif r >= 9:
                self.reaction[key] = self.act[3]    # like
        self.reaction[-1] = "like"
        self.state = self.reaction[0]

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
        self.turns += 1
        if self.turns % 5 == 0:
            self.hp = min(self.max_hp, self.hp + 0.1)
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
            a, b = self.fight.roll(foo.fight.limit)
            #  self.state = self.reaction[-1]
            if a:
                foo.hp -= b
                self.action = self.char + " makes " + str(b) + " damage"
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

    def talk(self, level):
        for y in range(-2, 2, 1):
            for x in range(-2, 2, 1):
                newx = self.x
                newy = self.y
                newx = min(self.maxyx[1], newx + x)
                newx = max(0, newx)
                newy = min(self.maxyx[0], newy + y)
                newy = max(0, newy)
                foo = level.blocking(newy, newx)
                if foo != None and foo != self:
                    foo.state = foo.reaction[1]


class Monster(Character):
    ''' NPC-class '''
    def follow(self, level):
        player = level.wheres_waldo()
        foo = level.hostiles(self.y, self.x)
        if foo != None and abs(foo.y - self.y) < self.sens and abs(foo.x - self.x) < self.sens:
            if foo.y < self.y:
                self.direction[0] = -1
            if foo.y > self.y:
                self.direction[0] = 1
            if foo.x < self.x:
                self.direction[1] = -1
            if foo.x > self.x:
                self.direction[1] = 1
        elif abs(player[0] - self.y) < self.sens and abs(player[1] - self.x) < self.sens:
            if player[0] < self.y:
                self.direction[0] = -1
            if player[0] > self.y:
                self.direction[0] = 1
            if player[1] < self.x:
                self.direction[1] = -1
            if player[1] > self.x:
                self.direction[1] = 1
    def attack(self, level):
        player = level.wheres_waldo()
        if abs(player[0] - self.y) < self.sens and abs(player[1] - self.x) < self.sens:
            if player[0] < self.y:
                self.direction[0] = -1
            if player[0] > self.y:
                self.direction[0] = 1
            if player[1] < self.x:
                self.direction[1] = -1
            if player[1] > self.x:
                self.direction[1] = 1

    def flee(self, level):
        player = level.wheres_waldo()
        if abs(player[0] - self.y) < self.sens and abs(player[1] - self.x) < self.sens:
            if player[0] < self.y:
                self.direction[0] = 1
            if player[0] > self.y:
                self.direction[0] = -1
            if player[1] < self.x:
                self.direction[1] = 1
            if player[1] > self.x:
                self.direction[1] = -1
        else:
            self.state = self.reaction[0]
            self.direction = [0, 0]

    def move(self, level):
        ''' moves the instance and checks for blocking (bool)
            with added AI '''
        if self.state == "fight":
            self.attack(level)
            self.color = 1
        if self.state == "like":
            self.follow(level)
            self.color = 10
        if self.state == "flee":
            self.flee(level)
            self.color = 3
        if self.state == "ignore":
            self.direction[0] = random.randint(-1, 1)
            self.direction[1] = random.randint(-1, 1)
            self.color = 4
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
            if self.state == "fight":
                if self.fight.roll(foo.fight.limit):
                    foo.hp -= 2
                    self.action = self.char + " hits " + foo.char
                    if foo.hp < 1:
                        foo.alive = False
                        foo.char = " "
                        self.action = "killed"
                else:
                    self.action = "missed..."
            if self.state == "like" and foo.char != "@":
                if self.fight.roll(foo.fight.limit):
                    foo.hp -= 2
                    self.action = "smack!"
                    if foo.hp < 1:
                        foo.alive = False
                        foo.char = " "
                        self.action = "killed"
                else:
                    self.action = "missed..."
        else:
            self.x = newx
            self.y = newy
            self.action = ""

class Tile(Object):
    ''' tile class '''
    def __init__(self, y, x, type_of, maxyx):
        self.maxyx = maxyx  # y,x
        self.x = x
        self.y = y
        self.blocking = True
        self.color = 0
        self.alive = False
        self.fight = skills.Skill(100)
        self.hp = 100
        self.reaction = {-1: "ignore",
                         0: "ignore",
                         1: "ignore"}

        if type_of == 0:
            self.char = "|"
            self.color = random.randint(184, 187)
            self.blocking = True
        if type_of == 1:
            self.char = "Y"
            self.color = random.randint(40, 43)
            self.blocking = True
        if type_of == 2:
            self.char = "~"
            self.color = random.randint(24, 27)
            self.blocking = False
        else:
            self.char = "#"
            self.color = random.randint(240, 247)
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
