#!/usr/bin/env python2

from tests import runTest
from time import sleep
import db

fp = open("/srv/sol.txt")
raw = []
for solution in fp.readlines():
    raw.append(solution.trim())
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
        maximum = dbmaxs[0][0]
        for (placementID,) in dbmaxs:
            if placementID > maximum:
                maximum = placementID
        users.append((uid, maximum))

        return sorted(users, lambda x: x[1])[:10]

def testUsers():
    users = getTenNewestUsers()
    # Not quite as dumb as it looks
    times = [[]] * len(users)
    for trial in range(10):
    for tupIndex in range(len(users)):
        (uid, placementID) = users[tupIndex]
        placementID += 1
        if placementID >= len(raw):
            # We've tested all the solutons for this user
            continue
        else:
            if placementID = len(raw) - 1:
                # Ahahahahaha have fun
                (answer, debug, timetaken) = runTest(uid, raw[placementID][:3])
            else:
                # 3 tiles * 3 chars/tile = 9 chars (~ 1s)
                (answer, debug, timetaken) = runTest(uid, raw[placementID][:9])
            # An incorrect answer incurs a 10s penalty.
            # This is included in the mean calculation
            if len(answer) != 1 or answer[0] != raw[placementdID]:
                timeTaken += 10000
            times[tupIndex].append(timeTaken)
    ret = []
    for i in range(len(users)):
        if times[i] == []:
            ret.append((users[i][0], users[i][1], None))
        else:
            ret.append((users[i][0], users[i][1], int(sum(times[i])/len(times[i]))))
            

if __name__ == "__main__":
    while True:
        cnx = db.dbConnect("linkgame")
        cur = cnx.cursor()
        for (uid, placementID, avgtime) in testUsers():
            if (avgtime != None):
                cur.execute("INSERT INTO tournament SET uid=%s, placementID=%i, timeTaken=%i", [uid, placementID, avgtime])
        
        cnx.commit()
        cnx.close()
        sleep(5)

