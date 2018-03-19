import random
import time

class Skill:
    def __init__(self):
        self.dice = 1
        self.xp = 0

    def rll(self, n):
        ''' my modified D6 rules '''
        l = []
        r = 0
        for i in range(n):
            throw = random.randint(0, 6)
            print(throw)
            l.append(throw)
        zeros = l.count(0)
        sixes = l.count(6)
        if sixes > zeros:
            print("more!")
            r += self.rll(sixes)
        if zeros >= sixes or zeros == 0:
            for num in l:
                r += num
        return r

    def roll(self):
        return self.rll(self.dice)

a = Skill()
a.dice = 6
for i in range(8):
    print("total: " + str(a.roll()))
    time.sleep(1)
