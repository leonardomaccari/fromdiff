# libraries for string comparision
from difflib import SequenceMatcher
import jellyfish as jf
# From: address parser
from email.utils import parseaddr
from collections import defaultdict


def diff_string(string1, string2, algorithm="RO"):
    """ deafults to Ratcliff-Obershelp.
    can be changed to Levenshtein algorithm
    1 == same string, 0 == no similarity. The two algorithms
    use a reversed  score scale, I have to rescale."""

    if algorithm == "LE":
        d = jf.levenshtein_distance(string1, string2)
        if d == 0:
            return 1
        else:
            return 1 - float(d)/max(len(string1), len(string2))
    elif algorithm == "RO":
        s = SequenceMatcher(None, string1, string2)
        r = s.ratio()
        return r
    else:
        raise Exception("Wrong algorithm chosen for difference match:"
                        + algorithm)


def parse_address(from_field):
    """ returns [firstname, secondname,...], "user", "domain"
    from a "From:" field."""

    # people use brackets in names, not allowed by rfc
    blacklist = "[](){}"
    clean_from = ""
    for s in from_field:
        if s not in blacklist:
            clean_from += s
    # split name, email
    (name, email) = parseaddr(clean_from)
    # cleanup the name from non alphanumeric chars, use only lowercase,
    # remove white spaces also so multiple names are treated as only one string
    # this should not impact Ratcliff/Obershelp
    clean_name = filter(str.isalnum, name).lower().encode("ascii", "ignore")

    return [clean_name, email.split("@")[0].lower(),
            email.split("@")[1].lower()]


def from_diff(left, right):
    """ Compares the similarity of two "From:" addresses, each one is in the
    form [firstname, secondname...], emailuser, emaildomain. The Idea is to
    compare separately the similitude between the names, the emails and return
    the maximun value
    """
    lname, luser, ldomain = left
    rname, ruser, rdomain = right

    match_dict = {
        0: "email->email",
        1: "name->name  ",
        2: "name->email ",
        3: "email->name "}
    # let's start with emails:

    # assumption: same email == same person
    if luser+"@"+ldomain == ruser+"@"+rdomain:
        return [1, match_dict[0]]

    # assumption: same users + different domain -> same person
    if luser == ruser:
        return [1, match_dict[0]]

    # assumption: domain doesn't mean correlation but influences the
    # metric, so compare only user
    email_diff_ratio = diff_string(luser, ruser)

    # diff names
    if ("".join(lname) and "".join(rname)):
        name_diff_ratio = diff_string("".join(lname), "".join(rname))
    else:
        name_diff_ratio = 0

    # cross differences
    cross_diff_1 = diff_string("".join(lname), ruser)
    cross_diff_2 = diff_string("".join(rname), luser)
    diffs = [email_diff_ratio, name_diff_ratio, cross_diff_1, cross_diff_2]
    max_value = max(diffs)
    return [max_value, match_dict[diffs.index(max_value)]]


def parse_list(from_list, cut_size=10):
    """from_List is a list of objects of the kind
    [[firstname, secondname, thirdname...], useremail, domainemail].
    This function returns a ranking of the Froms that are more similar"""

    diff_list = []
    for i in range(len(from_list)):
        fl = from_list[i]
        for j in range(i+1, len(from_list)):
            fr = from_list[j]
            diff_list.append([from_diff(fl, fr), fl, fr])

    return sorted(diff_list, key=lambda x: -x[0][0])[:cut_size]


def parse_dict(from_dict, cut_size=10):
    """from_dict is of the kind
    from_dict[ID] = [[firstname, secondname, thirdname...],
            useremail, domainemail].
    This function returns a ranking of the Froms that are more similar.
    This function differs from parse_list in that it takes a dictionary
    as an input, so the original string can be tracked back"""

    diff_list = []
    key_list = from_dict.keys()
    for i in range(len(key_list)):
        fl = from_dict[key_list[i]]
        for j in range(i+1, len(key_list)):
            fr = from_dict[key_list[j]]
            diff_list.append([from_diff(fl, fr), fl, fr,
                             key_list[i], key_list[j]])
    return sorted(diff_list, key=lambda x: -x[0][0])[:cut_size]


def linear_parse_dict(from_dict, cut_size=10):
    """from_dict is of the kind
    from_dict[ID] = [[firstname, secondname, thirdname...],
            useremail, domainemail].
    this function does the same of parse_dict but returns
    a dictionary with left_entry -> [
        [[match_score, kind_of_match], [parsed_left_entry],
         [parsed_right_entry], right_entry] ]
    that can be linearly analysed, instead that quadratically """

    diff_dict = defaultdict(list)
    for left in from_dict.keys():
        for right in from_dict.keys():
            if left == right:
                continue
            l_fields = from_dict[left]
            r_fields = from_dict[right]
            diff_dict[left].append([from_diff(l_fields, r_fields), l_fields,
                                   r_fields, right])
    return diff_dict




