#! /usr/bin/env python
import sys
import random
import simplejson

# just a random wordlist

wordlist = ["bromized", "unremaining", "missaid", "tardle", "Nickles",
            "forcibleness", "conveying", "anapanapa", "Kyne", "hooters",
            "cystophotography", "catabolically", "imaumbarah", "Crucianella",
            "exegetical", "isoperimetry", "Bobby", "whizgig",
            "benzophenoxazine", "overbearance", "probridge", "diamagnetically",
            "fleecers", "packinghouse", "Senecio", "sinuato-", "bevatrons",
            "supersecret", "irremissibility", "lightboard", "cooeyed",
            "ethanedithiol", "haliplid", "ullaged", "pre-Dutch", "acidotic",
            "apomixes", "sudden", "cawl", "circiter", "reuniters", "marks",
            "tripletree", "Maastricht", "phytoclimatology", "Piotr",
            "spirometer", "expiration", "self-focused", "pinko", "under-earth",
            "overmelted", "intendit", "razor-fish", "hypnotizes", "Sheeler",
            "multi", "Pterocarpus", "vascula", "Egwan", "subinduce",
            "athletes", "never-waning", "recodified", "volt-coulomb", "bagnut",
            "appointing", "gingerspice", "coeducationalism", "moonport",
            "beblister", "thermomotive", "undevastating", "blennophlogisma",
            "nontemperate", "ingeminated", "luteous", "prob", "romanization",
            "permissible", "subtribual", "pyromorphism", "peridot", "-genous",
            "bore", "swain", "dismutation", "ventriloque", "brigued",
            "encharged", "Jeth", "montjoye", "anticult", "mystifier",
            "ketimine", "tonality", "Eger", "Hohenstaufen", "Nicolette",
            "Chouteau"]


def random_line(f, size):
    wlist = []
    return wlist[:size]

random.seed()
random.shuffle(wordlist)
random_words = wordlist[:10]
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
