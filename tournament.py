#!/usr/bin/env python2

from tests import runTest
from time import sleep
import db

fp = open("/srv/sol.txt")
raw = []
for solution in fp.readlines():
    raw.append(solution.lstrip().rstrip())
fp.close()

def getTenNewestUsers():
    cnx = db.dbConnect("linkgame")
    cur = cnx.cursor()
    cur.execute(("SELECT uid FROM tests WHERE testStatus=1;"))
    dbusers = cur.fetchall()
    cnx.close()

    users = []
    for (uid,) in dbusers:
        cnx = db.dbConnect("linkgame")
        cur = cnx.cursor()
        cur.execute("SELECT placementID FROM tournament WHERE uid=%s", [uid])
        dbmaxs = cur.fetchall()
        cnx.close()
        maximum = -1
        for (placementID,) in dbmaxs:
            if placementID > maximum:
                maximum = placementID
        users.append((uid, maximum))

    return sorted(users, key=lambda x: x[1])[:10]

def testUsers():
    users = getTenNewestUsers()
    # Not quite as dumb as it looks
    times = [[]] * len(users)
    totaldebug = [""] * len(users)
    for trial in range(10):
        for tupIndex in range(len(users)):
            (uid, placementID) = users[tupIndex]
            placementID += 1
            if placementID >= len(raw):
                # Right, but, like, are you sure?
                cnx = db.dbConnect("linkgame")
                cur = cnx.cursor()
                cur.execute("SELECT placementID FROM tournament WHERE uid=%s", [uid])
                placements_ = cur.fetchall()
                cnx.close()
                placements = []
                for (placement,) in placements_:
                    placements.append(placement)
                for i in range(len(raw)):
                    if not (i in placements):
                        placementID = i
                        users[tupIndex][1] = i - 1
                if placementID >= len(raw):
                    # We've tested all the solutons for this user
                    continue

            if placementID == len(raw) - 1:
                # Ahahahahaha have fun
                (answer, debug, timeTaken) = runTest(uid, raw[placementID][:3], True)
            else:
                # 3 tiles * 3 chars/tile = 9 chars (~ 1s)
                (answer, debug, timeTaken) = runTest(uid, raw[placementID][:9], True)
            # An incorrect answer incurs a 10s penalty.
            # This is included in the mean calculation
            if len(answer) != 1 or answer[0] != raw[placementID]:
                timeTaken += 10000
                print "[debug] Answer incorrect or not given", uid, placementID, timeTaken
            else:
                print "[debug] Answer correct", uid, placementID, timeTaken
            # I have to do it this was because Python's lists are pass-by-reference
            # Seriously, both 'times[tupIndex].append(...)' and 'times[tupIndex] += [...]' fail!!
            times[tupIndex] = times[tupIndex] + [timeTaken]
            totaldebug[tupIndex] += debug
            totaldebug += ("\n" + ("-"*20) + "\n")

    ret = []
    for i in range(len(users)):
        if times[i] == []:
            ret.append((users[i][0], users[i][1] + 1, None, "No data."))
        else:
            ret.append((users[i][0], users[i][1] + 1, int(sum(times[i])/len(times[i])), totaldebug[i]))

    return ret; 


if __name__ == "__main__":
    while True:
        cnx = db.dbConnect("linkgame")
        cur = cnx.cursor()
        for (uid, placementID, avgtime, debug) in testUsers():
            if (avgtime != None):
                cur.execute("INSERT INTO tournament SET uid=%s, placementID=%s, timeTaken=%s, debug=%s;", [uid, placementID, avgtime, debug])
        
        cnx.commit()
        cnx.close()
        sleep(5)

