#!/usr/bin/python
import sys
from diffFrom import *
import pprint
import simplejson

def main():
    """ Main to test the library, takes as input a file with each line
    of the type "firstname secondname thirdname... <user@domain> and
    performs similarity chacks on each line taken two by two """

    if len(sys.argv) == 1:
        print "please enter a file to parse"
        sys.exit()
    else:
        try:
            f = open(sys.argv[1])
        except:
            print >> sys.stderr, "Could not open file", sys.argv[1]
            sys.exit(1)
        try:
            jList = simplejson.load(f)
        except simplejson.JSONDecodeError:
            print >> sys.stderr, "Could not parse JSON file", sys.argv[1]
            sys.exit(1)

    fromList = []
    for s in jList:
        fromList.append(parseAddress(s))
    l = parseList(fromList)
    pp = pprint.PrettyPrinter()
    pp.pprint(l)
    



if __name__ == "__main__":
    main()

