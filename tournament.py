#!/usr/bin/env python2

from tests import doTest
from time import sleep

fp = open("/srv/sol.txt")
raw = []
for solution in fp.readlines():
    raw.append(solution.trim())
fp.close()

if __name__ == "__main__":
    while True:
        sleep(5)
