#!/usr/bin/env python2
# Waits for one of the daemons to write to /srv/res
# and executes '/srv/daemons/runfunc.groovy' as user 'mallory'.
# Must be running as root to work.

from time import sleep
from subprocess import call

baseDir = "/srv/mallory"

while True:
    fp = open("/srv/res", "r")
    contents = fp.read().lower()
    fp.close()
    if "running" in contents:
        # Run it! I'm being generous with the time
        # here to allow for VM spinup etc
        call(["timeout", "--foreground", "5", "sudo", "-u", "mallory", "/srv/daemons/runfunc.groovy"])
        call(["pkill", "-9", "-u", "mallory"])
        fp = open("/srv/res", "w")
        fp.write("completed");
        fp.close()
    sleep(1)
