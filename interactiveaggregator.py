#! /usr/bin/env python
import sys
import simplejson
import curses
from fromdiff import parse_address, linear_parse_dict
from time import sleep
from collections import defaultdict
import mailbox

help_text = """ In the next screens, for each "From" address that was read from
the list you passed, you will be shown a set of potential matches. You can
choose to merge the "From" field into one of the others, and only one. The
matches are ordered for their similarity rank.
For each entry you are also told how many any other "From" was merged into it.

Hit any button to continue"""


def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(2, 2 + len(prompt_string) + 1, 60)
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
            simplejson.dump(aggregated_list, f, indent=4, sort_keys=True)
            f.close()
            break
        elif save == "n":
            return


def print_input_choice(y, x, screen, undo):

    screen.addstr(y, x, '"0-9" - merge into string')
    screen.addstr(y+1, x, 'space - see next choices')
    if undo:
        screen.addstr(y+2, x, 'u - undo last')
    else:
        screen.addstr(y+2, x, '- - nothing to undo (go to next)')
    screen.addstr(y+3, x, 'n - skip to next (do nothing)')
    screen.addstr(y+5, x, 's - (Save and) Exit')
    accepted_values = {}
    for i in "1234567890 usn":
        accepted_values[ord(i)] = i
    while True:
        ipt = screen.getch()
        if ipt not in accepted_values:
            screen.addstr(y+5, x,  'invalid option!')
        else:
            return accepted_values[ipt]


def start_curses(l):
    aggregated_list = {}
    undos = []
    i = 0
    screen.clear()
    screen.border(0)
    max_show = min(10, len(l)-1)
    for idx, i in enumerate(help_text.split("\n")):
        screen.addstr(3+idx, 2, i)
    screen.getch()
    idx = 0
    match_counter = defaultdict(int)
    old_entries = set()
    while idx < len(l):
        (key, value) = sorted(l.items(),
                              key=lambda(x): -max(y[0][0] for y in x[1]))[idx]
        candidate = key
        target_list = []
        ordered_matches = sorted(value, key=lambda(x): -x[0][0])
        for i in range(0, len(ordered_matches), max_show):
            screen.clear()
            # TODO print also how many merges were done in this string
            match_str = " (" + str(match_counter[key]) + " aggregated already)"
            y = 3
            screen.addstr(y, 2, str(idx) + "/" + str(len(l)) + ") "
                          + key + match_str)
            y += 2
            target_list = ordered_matches[i:i+max_show]
            if key not in old_entries:
                old_entries.add(key)
            for j in range(max_show):
                if i + j >= len(ordered_matches):
                    break
                k = ordered_matches[i + j]
                if k[3] in aggregated_list:
                    number = "X"
                else:
                    number = str(j)
                if k[3] not in old_entries:
                    matcher = "(-) "
                else:
                    matcher = "(" + str(match_counter[k[3]]) + ") "
                out_str = number + ") " + matcher \
                    + str(k[0][0])[0:3].rjust(3, " ")
                out_str += " " + str(k[0][1]) + "  " + k[3]
                screen.addstr(y + j, 7, out_str)
            y += max_show
            ipt = print_input_choice(y + 1, 7, screen, len(undos))
            if ipt == ' ':
                continue
            else:
                break
        screen.border(0)
        if ipt in "1234567890":
            aggregated_list[candidate] = target_list[int(ipt)]
            undos.append(candidate)
            match_counter[target_list[int(ipt)][3]] += 1
        if ipt == "u":  # should go back to previous one after undoing
            # undo last
            if len(undos) > 0:
                del aggregated_list[undos[-1]]
                undos.pop()
                idx -= 2  # one to go back, one because we will increment
            curses.endwin()
        if ipt == "s":
            if aggregated_list:
                save_results(aggregated_list)
            curses.endwin()
            return
        if ipt == "n":
            pass
        idx += 1
    save_results(aggregated_list)
    curses.endwin()


def parse_mbox(mbox_file):
    """ Parses a mailbox, extract From values """

    mbox = mailbox.mbox(mbox_file)
    if not mbox:
        print "Empty mbox, quitting"
        curses.endwin()
        sys.exit(1)
    address_dict = {}
    for message in mbox:
        from_field = unicode(message["From"],
                             'ISO-8859-2').encode('ascii', 'ignore')
        address_dict[str(from_field)] = parse_address(from_field)
    return address_dict


def main():
    """ This code will parse text file made of a list of elements of the kind
    [["firstname secondname, thirdname... <user@email.ext>"]... ], it will
    compute the differences between each copuple of entry, then it will present
    to a user-interface the ones that are the most similar ones and ask
    if they have to be merged. When done, it will save a json object with
    the dictionary {pseudonym1:realname, pseudonym2:realname ...} that
    can be used in various contexts"""

    if len(sys.argv) <= 1:
        print "please enter an mbox file to parse"
        curses.endwin()
        sys.exit()
    else:
        address_dict = parse_mbox(sys.argv[1])
    l = linear_parse_dict(address_dict, cut_size=100)
    start_curses(l)

screen = curses.initscr()
if __name__ == "__main__":
    main()
