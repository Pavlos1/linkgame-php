#!/usr/bin/env python2
# Waits for one of the daemons to write to /srv/res
# and executes '/srv/daemons/runfunc.groovy' as user 'mallory'.
# Must be running as root to work.

from time import sleep
from timeit import timeit
from subprocess import call
from sys import argv

while True:
    if len(argv) > 1 and argv[1] == "tournament":
        path = "/srv/rest"
        arg1 = "tournament"
        user = "malloryt"
    else:
        path = "/srv/res"
        arg1 = "tests"
        user = "mallory"
    fp = open(path, "r")
    contents = fp.read().lower()
    fp.close()
    if "running" in contents:
        # Run it! I'm being generous with the time
        # here to allow for VM spinup etc
        func = lambda: call(["timeout", "--foreground", "5", "sudo", "-u", user, "/srv/daemons/runfunc.groovy", arg1])
        timetaken = 1000 * timeit(stmt=func, number=1)
        call(["pkill", "-9", "-u", user])
        fp = open(path, "w")
        fp.write("completed:%d" %timetaken);
        fp.close()
    sleep(1)
