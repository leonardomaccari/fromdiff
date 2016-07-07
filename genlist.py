#! /usr/bin/env python
import sys
import random
import simplejson


def random_line(f, size):
    # skip header
    next(f)
    wlist = []
    for i in range(max(1000, size*2)):
        try:
            wlist.append(next(f))
        except StopIteration:
            break
    random.shuffle(wlist)
    return wlist[:size]

try:
    wordlist = open("/usr/share/dict/linux.words", "r")
except:
    print "please configure a wordlist in the script"
    sys.exit(1)

random.seed()
random_words = random_line(wordlist, 10)
random_letters = list("qwertyuiopasdfghjklzxcvbnm")
counter = 0
from_list = []
while True:
    newLine = []
    for i in range(4):
        rndw = random.randint(0, len(random_words)-1)
        w = random_words[rndw]
        stri = list(filter(str.isalnum, w).encode("ascii", "ignore"))
        rnd = random.randint(0, len(stri)-1)
        stri[rnd] = random_letters[rnd % len(random_letters)]
        newLine.append("".join(stri))

    from_list.append('"'+newLine[0] + " " + newLine[1]+'" ' +
                     "<"+newLine[2] + "@" + newLine[3] + ".com>")
    counter += 1
    if counter >= 10:
        break
print simplejson.dumps(from_list)
