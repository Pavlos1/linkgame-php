#!/usr/bin/env python2
# Waits for one of the daemons to write to /srv/res(t)
# and executes '/srv/daemons/runfunc.groovy' as user 'mallory(t)'.
# Must be running as root to work.

from time import sleep
from timeit import timeit
from subprocess import call
from sys import argv

fp = open("/srv/whoami")
whoami = fp.read().lstrip().rstrip()
fp.close()

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
        # Allow mallory(t) to read&write from /srv/mallory(t)
        call(["chown", "-R", user, "/srv/" + user])
        # In case mallory(t) tries to delete the folder
        call(["chown", whoami, "/srv/" + user])
        # Run it! I'm being generous with the time
        # here to allow for VM spinup etc
        func = lambda: call(["sudo", "-u", user, "timeout", "--foreground", "5", "/srv/daemons/runfunc.groovy", arg1])
        timetaken = 1000 * timeit(stmt=func, number=1)
        call(["pkill", "-9", "-u", user])
        # Allow the db user (http or www-data) to access contents
        call(["chown", "-R", whoami, "/srv/" + user])
        # Notify that task has completed
        fp = open(path, "w")
        fp.write("completed:%d" %timetaken);
        fp.close()
    sleep(1)
