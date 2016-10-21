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

def runTest(uid, placements):
    call(["rm", "-rf", baseDir + "/*"])
    call(["cp", jarDir + "/" + uid + ".jar", baseDir + "/injar.jar"])
    # TODO: Call actual program. This is '/srv/daemons/runfunc.groovy', but must be run as user 'mallory'
    try:
        fp = open(baseDir + "/out.txt")
        res1 = []
        for result in fp.readlines():
            res1.append(result.trim())
        fp.close()
    except:
        res1 = ["!!NO RESULTS!!"]

    try:
        fp = open(baseDir + "/debug.txt")
        res2 = fp.read().trim()
        fp.close()
    except:
        res2 = "No data."

    return (sorted(res1), res2)

def doTests(uid):
    for test in SOLUTIONS_ONE:
        result = runTest(uid, test[0])
        if len(result[0]) != 1 or result[0][0] != test[1]:
            return (False, "Input: %s\nExpecting: %s\nGot: %s\nAdditional debug information:\n%s\n" %(test[0], str([test[1]]), str(result[0]), result[1]))
    
    for test in SOLUTIONS_MULTIPLE:
        result = runTest(uid, test[0])
        if len(result[0]) != len(test) - 1 or result[0] != sorted(test[1:]):
            return (False, "Input: %s\nExpecting: %s\nGot: %s\nAdditional debug information:\n%s\n" %(test[0], str(test[1:]), str(result[0]), result[1]))

    return (True, "")

if __name__ == "__main__":
    while True:
        cnx = db.dbConnect("linkgame")
        cur = cnx.cursor()
        cur.execute(("SELECT * FROM tests;"))
        for (ID, uid, testStatus, debug) in cur:
            if testStatus == 0:
                result = doTests(uid)
                if result[0]:
                    cur.execute("UPDATE tests SET testStatus=1 WHERE uid=%s" %uid)
                else:
                    cur.execute("UPDATE tests SET testStatus=-1, debug=%s WHERE uid=%s", %(result[1], uid))
        sleep(5)
