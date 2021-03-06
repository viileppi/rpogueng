import random
import skills

class Object:
    ''' color = 1...6 '''
    def __init__(self, y, x, c, maxyx):
        self.name = c
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
        self.sens = random.randint(5, 12)
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
        self.state = self.reaction[0]

    def position(self):
        ''' return position [y, x] '''
        return [self.y, self.x]


class Character(Object):
    ''' character class '''

    def move(self, level):
        ''' moves the instance and checks for blocking (bool)
            returns old_y and old_x '''
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
            self.x = self.old_x
            self.y = self.old_y
            a, b = self.fight.roll(foo.fight.limit)
            foo.state = foo.reaction[-1]
            if a:
                foo.hp -= b
                self.action = "You hit " + foo.name
                if foo.hp < 1:
                    foo.die(level)
                    foo.alive = False
            else:
                self.action = "missed..."
        else:
            self.x = newx
            self.y = newy
            self.action = ""

    def talk(self, level):
        self.action = "@ talks with calming voice"
        for y in range(-3, 3, 1):
            for x in range(-3, 3, 1):
                newx = self.x
                newy = self.y
                newx = min(self.maxyx[1], newx + x)
                newx = max(0, newx)
                newy = min(self.maxyx[0], newy + y)
                newy = max(0, newy)
                foo = level.blocking(newy, newx)
                if foo != None and foo != self:
                    foo.state = foo.reaction[1]

    def die(self, level):
        q = level.wheres_waldo()
        p = q[0] + q[1]
        m = self.x + self.y
        if abs(p - m) < 2 and self.state == "like":
            a = SausageMonster(self.y, self.x, "*", self.maxyx)
            a.hp = 1
            a.name = "Sausage monster"
            a.action = "Alien rises from the death!"
            a.color = 5
            level.characters.append(a)


class Monster(Character):
    ''' NPC-class '''
    def follow(self, level):
        player = level.wheres_waldo()
        p1 = level.characters[0]
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
        if abs(player[0] - self.y) < 3 and abs(player[1] - self.x) < 3:
            if p1.hp < p1.max_hp:
                p1.hp = min(p1.max_hp, p1.hp + 1)
                self.hp -= 2
                if self.hp < 1:
                    self.die(level)
                    self.alive = False
                self.action = self.name + " gives HP for you!"
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
            with added AI, returns old_y and old_x '''
        if self.state == "fight":
            self.attack(level)
            self.color = 1
        if self.state == "like":
            self.follow(level)
            self.color = 2
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
            if self.state == "fight" and foo.name != "tile" and foo.char != "*":
                if self.fight.roll(foo.fight.limit):
                    foo.state = foo.reaction[-1]
                    foo.hp -= 2
                    self.action = self.name + " hits " + foo.name
                    if foo.hp < 1:
                        foo.die(level)
                        foo.alive = False
                        self.action = "killed"
                else:
                    self.action = self.name + " missed..."
            if self.state == "like" and foo.char != "@":
                if self.fight.roll(foo.fight.limit):
                    foo.hp -= 2
                    if foo.hp < 1:
                        foo.die(level)
                        foo.alive = False
                        self.action = "killed"
                else:
                    self.action = "missed..."
            if foo.name == "tile":
                self.hp -= 1
                self.action = self.name + " smashes to the wall"
        else:
            self.x = newx
            self.y = newy

class SausageMonster(Monster):
    ''' from a movie I saw... '''
    def die(self, level):
        a = SausageMonster(self.y, self.x, "*", self.maxyx)
        a.hp = 1
        a.name = "Sausage monster"
        a.action = "The sausage moster split into two new monsters"
        a.color = 5
        b = SausageMonster(self.y + 1, self.x + 1, "*", self.maxyx)
        b.hp = 1
        b.name = "Sausage monster"
        b.color = 5
        level.characters.append(a)
        level.characters.append(b)

    def move(self, level):
        self.direction[0] = random.randint(-1, 1)
        self.direction[1] = random.randint(-1, 1)
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
        else:
            self.x = newx
            self.y = newy

            

class Tile(Object):
    ''' tile class '''
    def __init__(self, y, x, type_of, maxyx):
        self.name = "tile"
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
            self.blocking = True
        if type_of == 1:
            self.char = "Y"
            self.blocking = True
        if type_of == 2:
            self.char = "~"
            self.blocking = False
        else:
            self.char = "#"
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
