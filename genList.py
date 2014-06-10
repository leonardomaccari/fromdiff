#!/usr/bin/python

import sys
import random
import simplejson

def randomLine(f, size):
    line = next(f)
    wordlist = []
    wlist = list(enumerate(f))
    while True:
        rnd = random.randint(0, len(wlist))
        for l, v in wlist:
            if l == rnd:
                wordlist.append(v)
        if len(wordlist) > size:
            break
    return wordlist 

try:
    wordlist = open("/usr/share/dict/british-english", "r")
except:
    print "please configure a wordlist in the script"
    sys.exit(1)

random.seed()
randomWords = randomLine(wordlist, 10)
randomLetters = list("qwertyuiopasdfghjklzxcvbnm")
counter = 0
fromList = []
while True:
    newLine = []
    for i in range(4):
        rndw = random.randint(0,len(randomWords)-1)
        w = randomWords[rndw]
        stri = list(filter(str.isalnum, w).encode("ascii", "ignore"))
        rnd = random.randint(0,len(stri)-1)
        stri[rnd] = randomLetters[rnd%len(randomLetters)]
        newLine.append("".join(stri))

    fromList.append('"'+newLine[0] + " " + newLine[1]+'" '+\
        "<"+newLine[2] + "@" + newLine[3] + ".com>")
    counter += 1
    if counter >= 10:
        break
print simplejson.dumps(fromList)
