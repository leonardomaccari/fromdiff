
#libraries for string comparision
from difflib import SequenceMatcher
import jellyfish as jf
# From address parser
from email.utils import parseaddr

def diffString(string1, string2, algorithm="RO"):
    """ deafults to Ratcliff-Obershelp.
    can be changed to Levenshtein algorithm
    1 == same string, 0 == no similarity. Thus, I have to
    change the output of Levenshtein"""

    if algorithm == "LE":
        d = jf.levenshtein_distance(string1, string2)
        if d == 0:
            return 1
        else: 
            return 1 - float(d)/max(len(string1), len(string2))
    elif algorithm=="RO":
        s = SequenceMatcher(None, string1, string2)
        r = s.ratio()
        return r
    else:
        raise Exception("Wrong algorithm chosen for difference match:"\
            +algorithm)



def parseAddress(fromField):
    """ returns [firstname, secondname,...], "user", "domain" 
    from a From: field."""

    # people use brackets in names, not allowed by rfc
    blacklist = "[](){}"
    cleanFrom = ""
    for s in fromField:
        if s not in blacklist:
            cleanFrom += s
    #split name, email
    (name, email) = parseaddr(cleanFrom)
    #cleanup the name from non alphanumeric chars, use only lowercase
    cleanName = filter(str.isalnum, name).lower().encode("ascii",
            "ignore").split(" ")

    return [cleanName, email.split("@")[0].lower(), 
            email.split("@")[1].lower()]

def diffFrom(left, right):
    """ Compares the similarity of two "From:" addresses, each one is 
    in the form [firstname, secondname...], emailuser, emaildomain. The Idea
    is to compare separately the similitude between the names, the emails
    and return the maximun value
    """
    
    lname = left[0]
    rname = right[0]
    luser = left[1]
    ruser = right[1]
    ldomain = left[2]
    rdomain = right[2]

    matchDict = {
            0: "emailSimilarity",
            1: "nameSimilarity",
            2: "name->email similarity",
            3: "email->name similarity"}
    #let's start with emails:

    # assumption: same email == same person
    if luser+"@"+ldomain == ruser+"@"+rdomain:
        return [1, matchDict[0]]
    # assumption: two different users + different domain -> same person
    if luser == ruser:
        return [1, matchDict[0]]
    # assumption: domain doesn't mean correlation but influences the 
    # metric, so remove it
    emailDiffRatio = diffString(luser, ruser)

    # diff names
    nameDiffRatio = diffString("".join(lname), "".join(rname))
    
    # cross differences

    crossDiff1 = diffString("".join(lname), ruser)
    crossDiff2 = diffString("".join(rname), luser)
     
    diffs = [emailDiffRatio, nameDiffRatio, crossDiff1, crossDiff2]
    maxValue = max(diffs)
    return [maxValue, matchDict[diffs.index(maxValue)]]


def parseList(fromList, cutSize = 10):
    """fromList is a list of the kind 
    From = [[firstname, secondname, thirdname...], useremail, domainemail]. 
    This function returns a ranking of the Froms that are more similar"""

    diffList = [] 
    for i in range(len(fromList)):
        fl = fromList[i]
        for j in range(i+1,len(fromList)):
            fr = fromList[j]
            diffList.append([diffFrom(fl,fr), fl, fr])

    
    return sorted(diffList, key = lambda x: -x[0][0])[:cutSize]


def parseDict(fromDict, cutSize = 10):
    """fromDict is of the kind 
    fromDict[ID] = [[firstname, secondname, thirdname...], 
            useremail, domainemail]. 
    This function returns a ranking of the Froms that are more similar.
    This function differs from parseList in that it takes a dictionary
    as an input, so the original string can be tracked back"""

    diffList = [] 
    keyList = fromDict.keys()
    for i in range(len(keyList)):
        fl = fromDict[keyList[i]]
        for j in range(i+1,len(keyList)):
            fr = fromDict[keyList[j]]
            diffList.append([diffFrom(fl,fr), fl, fr, keyList[i], keyList[j]])
    return sorted(diffList, key = lambda x: -x[0][0])[:cutSize]



