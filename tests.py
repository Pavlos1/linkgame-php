#!/usr/bin/env python2
# The tests in this file are adapted from Steve's LinkGame test code
# See: https://gitlab.cecs.anu.edu.au/comp1110/comp1110-ass2/blob/master/tests/comp1110/ass2

import db
from time import sleep
from subprocess import call

baseDir = "/srv/mallory"
jarDir = "/srv/jars"

SOLUTIONS_ONE = [
            ["KAFCBGUCAGDFLEFPFBBGESHBWIJKJA", "KAFCBGUCAGDFLEFPFBBGESHBWIJKJAHKLJLH"],
            ["KAFCBGUCAGDFLEFPFBBGESHBOIA", "KAFCBGUCAGDFLEFPFBBGESHBOIAKJARKEJLH"],
            ["KAFTBAICFRDCEELWFJJGDMHK", "KAFTBAICFRDCEELWFJJGDMHKCIGNJCPKEBLF"],
            ["JABHBCBCGGDFIEKVFAFGG", "JABHBCBCGGDFIEKVFAFGGSHBXIAJJJUKHKLK"],
            ["JACRBHQCHCDGDELVFJ", "JACRBHQCHCDGDELVFJBGESHBUIAFJEHKLGLL"],
            ["IAFBBDRCEPDEWEB", "IAFBBDRCEPDEWEBSFJTGBFHGGILIJAQKIJLI"],
            ["GAEWBABCDJDA", "GAEWBABCDJDALEFMFCCGLUHBTIAQJCKKBILF"],
    ]

SOLUTIONS_MULTI = [
            ["KAFUBAICCPDALEFEFEQGHSHBNIB", "KAFUBAICCPDALEFEFEQGHSHBNIBCJFGKIRLE", "KAFUBAICCPDALEFEFEQGHSHBNIBCJFRKEGLI"],
            ["KAFCBGUCAGDFLEFPFBBGESHB", "KAFCBGUCAGDFLEFPFBBGESHBOIAKJARKEJLH", "KAFCBGUCAGDFLEFPFBBGESHBWIJKJAHKLJLH"],
            ["IAFBBGVCAJDJGEDQFEUGI", "IAFBBGVCAJDJGEDQFEUGIRHCIIHFJGNKFOLG", "IAFBBGVCAJDJGEDQFEUGIRHKIIHFJGNKFOLG"],
            ["KAAHBLTCAODEFEGMFC", "KAAHBLTCAODEFEGMFCEGERHGBIGVJCDKFJLF", "KAAHBLTCAODEFEGMFCEGERHGBIGVJIDKFJLF", "KAAHBLTCAODEFEGMFCEGEQHDBIGXJHDKFJLF", "KAAHBLTCAODEFEGMFCEGEVHBBIGXJADKFJLF"],
            ["JADVBJBCJRDCDED", "JADVBJBCJRDCDEDHFEWGBFHEJILSJCOKLMLC", "JADVBJBCJRDCDEDSFBWGBFHEJILGJEOKLHLE"],
            ["JAAPBGVCJRDC", "JAAPBGVCJRDCDEDSFBWGBFHECIFAJDHKGOLF", "JAAPBGVCJRDCDEDSFBWGBFHECIFAJDOKFHLG", "JAAPBGVCJRDCHEFSFBWGBFHEGIICJDDKKOLF"],
    ]

# Ugh, transpiled Java code
def normalize(placement):
    if placement == "" or placement[0] == '!':
        return ""
    pp = [None] * 12;
    flip = False;
    for i in range(0, len(placement), 3):
        idx = ord(placement[i + 1]) - ord('A')
        pp[idx] = placement[i : i + 3]
        if (idx == 0):
           flip = (ord(placement[i]) - ord('A')) > 11

    norm = ""
    for i in range(len(pp)):
        if (pp[i] != None):
            norm += pp[i];

    if (flip):
       norm = flipPlacement(norm);

    return norm;

# More of the same
def flipPlacement(placement):
    if placement == "" or placement[0] == '!':
        return ""
    flipped = ""
    for i in range(0, len(placement), 3):
        origin = ord(placement[i]) - ord('A')
        piece = placement[i + 1]
        orientation = ord(placement[i + 2]) - ord('A')

        origin = 23 - origin
        if orientation < 6:
            orientation = (orientation + 3) % 6
        else:
            orientation = 6 + ((orientation + 3) % 6)

        flipped += (chr(origin + ord('A')) + piece + chr(orientation + ord('A')))
        
    return flipped;


def runTest(uid, placements, tournament=False):
    if tournament:
        path = "/srv/rest"
        base = "/srv/malloryt"
    else:
        path = "/srv/res"
        base = "/srv/mallory"

    call(["rm", "-rf", base + "/*"])
    call(["cp", jarDir + "/" + uid + ".jar", base + "/injar.jar"])
    fp = open(base + "/in.txt", "w")
    fp.write(placements.rstrip().lstrip())
    fp.close()
    fp = open(base + "/out.txt", "w")
    fp.write("")
    fp.close()
    fp = open(base + "/debug.txt", "w")
    fp.write("")
    fp.close()

    call(["chmod", "1700", base + "/injar.jar"])
    call(["chmod", "1600", base + "/in.txt"])
    call(["chmod", "1600", base + "/out.txt"])
    call(["chmod", "1600", base + "/debug.txt"])
    
    fp = open(path, "w")
    fp.write("running")
    fp.close()

    while True:
        fp = open(path, "r")
        contents = fp.read().lower()
        fp.close()
        if "completed" in contents:
            res3 = int(contents.split(":")[1])
            break
        sleep(1)

    try:
        fp = open(base + "/out.txt")
        res1 = []
        for result in fp.readlines():
            res1.append(normalize(result.rstrip().lstrip()))
        fp.close()
    except OSError:
        res1 = ["!!NO RESULTS!!"]

    try:
        fp = open(base + "/debug.txt")
        res2 = fp.read().rstrip().lstrip()
        fp.close()
    except OSError:
        res2 = "No data."

    return (sorted(res1), res2, res3)


def doTests(uid):
    for test in SOLUTIONS_ONE:
        result = runTest(uid, test[0])
        if len(result[0]) != 1 or result[0][0] != test[1]:
            return (False, "Input: %s\nExpecting: %s\nGot: %s\nAdditional debug information:\n%s\n" %(test[0], str([test[1]]), str(result[0]), result[1]))
    
    for test in SOLUTIONS_MULTI:
        result = runTest(uid, test[0])
        if len(result[0]) != len(test) - 1 or result[0] != sorted(test[1:]):
            return (False, "Input: %s\nExpecting: %s\nGot: %s\nAdditional debug information:\n%s\n" %(test[0], str(test[1:]), str(result[0]), result[1]))

    return (True, "")

if __name__ == "__main__":
    while True:
        cnx = db.dbConnect("linkgame")
        cur = cnx.cursor()
        cur.execute(("SELECT * FROM tests;"))
        dbout = cur.fetchall()
        cnx.close()
        for (ID, uid, testStatus, debug) in dbout:
            if testStatus == 0:
                result = doTests(uid)
                if result[0]:
                    cnx = db.dbConnect("linkgame")
                    cur = cnx.cursor()
                    cur.execute("UPDATE tests SET testStatus=1 WHERE uid=%s;", [uid])
                    cnx.commit()
                    cnx.close()
                else:
                    cnx = db.dbConnect("linkgame")
                    cur = cnx.cursor()
                    cur.execute("UPDATE tests SET testStatus=-1, debug=%s WHERE uid=%s;", [result[1], uid])
                    cnx.commit()
                    cnx.close()
        sleep(5)
