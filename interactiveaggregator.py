#! /usr/bin/env python
import sys
import simplejson
from os import system
import curses


from  diffFrom import *
from time import sleep

screen = curses.initscr()

def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def saveResults(aggregatedList):
    save = "Y"
    while True:
        save = get_param("Save results? [Y/n]:")
        if save == "Y":
            filename = get_param("Enter Filename:")
            try:
                f = open(filename, "w")
            except IOError:
                screen.clear()
                error = "ERROR: Can not open "+filename+" for writing!"
                screen.addstr(2, 2, error)
                screen.refresh()
                sleep(2)
                continue
            simplejson.dump(aggregatedList, f)
            f.close()
            break
        elif save == "n":
            return
 
def startCurses(l, fromDict):
    aggregatedList = {}
    undos = []
    i = 0
    while i < len(l):
        v = l[i]
        screen.clear()
        if v[3] in aggregatedList:
            leftElement = "1*)"
            screen.addstr(7, 4, "X - 1) has been already merged,"+\
                 "can not merge it again")
        elif v[3] in aggregatedList.values(): 
            leftElement = "1+)"
            screen.addstr(7, 4, "X - something has been "\
                "merged in 1. You don't want to merge 1 into 2")
        else:
            leftElement = "1)"
            screen.addstr(7, 4, "1 - Merge 1 into 2")

        if v[4] in aggregatedList:
            rightElement = "2*)"
            screen.addstr(8, 4, "X - 2) has been already merged,"+\
                 "can not merge into it again")
        elif v[4] in aggregatedList.values(): 
            leftElement = "2+)"
            screen.addstr(8, 4, "X - something has been "\
                "merged in 2. You don't want to merge it into 1")
        else:
            rightElement = "2)"
            screen.addstr(8, 4, "2 - Merge 2 into 1")

        leftElement += fromDict[v[3]]
        rightElement += fromDict[v[4]]

        screen.border(0)
        screen.addstr(2, 2, str(v[0][0])+": "+v[0][1])
        screen.addstr(3, 2, leftElement)
        screen.addstr(4, 2, rightElement)
        screen.addstr(9, 4, "3 - Do nothing")
        screen.addstr(10, 4, "4 - Undo last")
        screen.addstr(11, 4, "5 - Exit")
        screen.refresh()
    
        x = screen.getch()
    
        if x == ord('1'):
            curses.endwin()
            aggregatedList[v[3]] = v[4]
            undos.append(v[3])
        if x == ord('2'):
            curses.endwin()
            aggregatedList[v[4]] = v[3]
            undos.append(v[4])
        if x == ord('4'):
            #undo last
            if i > 0:
                del aggregatedList[undos[-1]]
                undos.pop()
                i -= 2
            else :
                i -= 1
            curses.endwin()
        if x == ord('5'):
            saveResults(aggregatedList)
            curses.endwin()
            return 
        i += 1
    saveResults(aggregatedList)
    curses.endwin()




def main():
    """ This code will parse text file made of a list of elements of the kind
    [["firstname secondname, thirdname... <user@email.ext>"]... ], it will
    compute the differences between each copuple of entry, then it will present 
    to a user-interface the ones that are the most similar ones and ask
    if they have to be merged. When done, it will save a json object with
    the dictionary {pseudonym1:realname, pseudonym2:realname ...} that
    can be used in various contexts"""
    
    if len(sys.argv) == 1:
        print "please enter a json file to parse"
        sys.exit()
    else:
        try:
            f = open(sys.argv[1], "r")
        except:
            print >> sys.stderr, "Could not open file", sys.argv[1]
            sys.exit(1)
        try:
            nameList = simplejson.load(f)
        except simplejson.JSONDecodeError:
            print >> sys.stderr, "The file specified in the pseudonymfile",\
                    "option is a malformed JSON!"
            sys.exit(1)

    parsedAddressDict = {}
    addressDict = {}
    for s in nameList:
        sId = repr(s)
        parsedAddressDict[sId] = parseAddress(s)
        addressDict[sId] = s
        
    l = parseDict(parsedAddressDict, cutSize=100)
    startCurses(l, addressDict)

if __name__ == "__main__":
    main()

