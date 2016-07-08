#! /usr/bin/env python
import sys
from fromdiff import parse_list, parse_address
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
            json_list = simplejson.load(f)
        except simplejson.JSONDecodeError:
            print >> sys.stderr, "Could not parse JSON file", sys.argv[1]
            sys.exit(1)

    from_list = []
    for s in json_list:
        from_list.append(parse_address(s))
    l = parse_list(from_list)
    pp = pprint.PrettyPrinter()
    pp.pprint(l)


if __name__ == "__main__":
    main()
