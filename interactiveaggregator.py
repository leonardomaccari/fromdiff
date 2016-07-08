#! /usr/bin/env python
import sys
import simplejson
import curses
from fromdiff import parse_address, parse_dict
from time import sleep


def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input


def follow_path(d, step, path):
    # base step
    if d[step] not in d.keys():
        path.append(d[step])
        return path
    elif d[step] in path:
        screen.border(0)
        screen.clear()
        screen.addstr(2, 2, "Human Error! you have loops in your choice!")
        screen.refresh()
        curses.endwin()
        return
    path.append(d[step])
    return follow_path(d, d[step], path)


def clean_dict(d):
    i = 0
    while True:
        k = d.keys()[i]
        path = follow_path(d, k, [k])
        if len(path) > 2:
            screen.clear()
            question = "Do you want to merge this path? [Y/n]"
            screen.addstr(2, 2, "Do you want to merge this path? [Y/n]")
            path_string = path[0]
            for p in path[1:]:
                path_string += " --> "+p
            screen.addstr(3, 2, path_string)
            screen.refresh()
            input = screen.getstr(2, 2+len(question), 60)
            if input != "Y":
                continue
            else:
                root = path[-1]
                for p in path[:-1]:
                    d[p] = root
        i += 1
        if i >= len(d):
            break
    return d


def save_results(aggregated_list):
    save = "Y"
    while True:
        save = get_param("Save results? [y/n]:")
        if save == "y":
            cleanup = get_param("Do you want to remove multiple merges [y/n]?")
            if cleanup == "y":
                aggregated_list = clean_dict(aggregated_list)
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
            simplejson.dump(aggregated_list, f)
            f.close()
            break
        elif save == "n":
            return


def start_curses(l, from_dict):
    aggregated_list = {}
    undos = []
    i = 0
    while i < len(l):
        v = l[i]
        screen.clear()
        right_element = ""
        left_element = ""
        if v[3] in aggregated_list:
            left_element = "1*)"
            screen.addstr(7, 4, "X - 1) has been already merged," +
                          "you don't want to merge it again")
        elif v[3] in aggregated_list.values():
            left_element = "1+)"
            screen.addstr(7, 4, "1 - something has been "
                          "merged in 1.")
        else:
            left_element = "1)"
            screen.addstr(7, 4, "1 - Merge 1 into 2")

        if v[4] in aggregated_list:
            right_element = "2*)"
            screen.addstr(8, 4, "X - 2) has been already merged," +
                          "you don't want to merge it again")
        elif v[4] in aggregated_list.values():
            right_element = "2+)"
            screen.addstr(8, 4, "X - something has been "
                          "merged in 2")
        else:
            right_element = "2)"
            screen.addstr(8, 4, "2 - Merge 2 into 1")

        left_element += from_dict[v[3]]
        right_element += from_dict[v[4]]

        screen.border(0)
        screen.addstr(2, 2, str(v[0][0])+": "+v[0][1])
        screen.addstr(3, 2, left_element)
        screen.addstr(4, 2, right_element)
        screen.addstr(9, 4, "3 - Do nothing")
        screen.addstr(10, 4, "4 - Undo last")
        screen.addstr(11, 4, "5 - Save and Exit")
        screen.refresh()
        x = screen.getch()
        if x == ord('1'):
            curses.endwin()
            aggregated_list[v[3]] = v[4]
            undos.append(v[3])
        if x == ord('2'):
            curses.endwin()
            aggregated_list[v[4]] = v[3]
            undos.append(v[4])
        if x == ord('4'):
            # undo last
            if len(undos) > 0:
                del aggregated_list[undos[-1]]
                undos.pop()
                i -= 2
            else:
                i -= 1
            curses.endwin()
        if x == ord('5'):
            save_results(aggregated_list)
            curses.endwin()
            return
        i += 1
    save_results(aggregated_list)
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
        curses.endwin()
        sys.exit()
    else:
        try:
            f = open(sys.argv[1], "r")
        except:
            print >> sys.stderr, "Could not open file", sys.argv[1]
            sys.exit(1)
        try:
            name_list = simplejson.load(f)
        except simplejson.JSONDecodeError:
            print >> sys.stderr, "The file specified in the pseudonymfile",\
                "option is a malformed JSON!"
            sys.exit(1)

    parsed_address_dict = {}
    address_dict = {}
    for s in name_list:
        s_id = str(s)
        parsed_address_dict[s_id] = parse_address(s)
        address_dict[s_id] = s
    l = parse_dict(parsed_address_dict, cut_size=100)
    start_curses(l, address_dict)

screen = curses.initscr()
if __name__ == "__main__":
    main()
