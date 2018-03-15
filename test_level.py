#!/usr/bin/python3
import objects
import level
import random
import pickle
import sys

w = int(sys.argv[1])
h = int(sys.argv[2])

a = level.Level(h, w)

with open("testlevel.pickle", "wb") as f:
    pickle.dump(a, f, pickle.HIGHEST_PROTOCOL)
