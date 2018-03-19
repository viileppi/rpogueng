import random
import time

class Skill:
    def __init__(self, d):
        self.dice = d
        self.xp = 0
        self.limit = self.dice * 3

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
            r += self.rll(sixes)
        if zeros >= sixes or zeros == 0:
            for num in l:
                r += num
        return r

    def roll(self, limit):
        ''' takes targets limit and tries to beat it
            returns true if beaten '''
        if self.rll(self.dice) > limit:
            return True
        else:
            return False
