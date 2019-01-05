import re
from random import randint

def isInt(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False


def roll_backend(args):
    breakdown = ['```']
    roll_total = 0
    realarg = ""
    if len(args) < 1:
        return "```Invalid argument count. Expected: !roll XdY where X is number of dice and Y is dice sides\nExample input: !roll 1d4+1d6+1```"
    for argument in args:
        realarg += argument

    #Saving the keep and keep lowest sections for later: (?:(k|kl)([1-9]\d*))?
    #Section 1 = +, -, or empty string]
    sections = re.findall(r"(\+|-)?(?:(?:([1-9]\d*)d([1-9]\d*))|([1-9]\d*))", realarg)
    if len(sections) == 0:
        return "```Invalid command. Expected: !roll XdY where X is number of dice and Y is dice sides\nExample input: !roll 1d4+1d6+1```"
    for section in sections:
        breakdown.append(section[0] + ' ')
        sectionval = 0
        if section[3] != '':
            sectionval = int(section[3])
            breakdown.append(section[3] + ' ')
        else:
            if (not isInt(section[1])) or int(section[1]) > 100 or int(section[1]) < 1:
                return None 
            if (not isInt(section[2])) or int(section[2]) > 10000 or int(section[2]) < 1:
                return None
            breakdown.append(section[1] + 'd' + section[2] + "[")
            for _ in range(0, int(section[1])):
                dieresult = randint(1, int(section[2]))
                sectionval += dieresult
                breakdown.append(str(dieresult) + ', ')
            breakdown[-1] = breakdown[-1].rstrip(', ')
            breakdown.append("] ")
        if section[0] == '':
            roll_total = sectionval
        elif section[0] == '+':
            roll_total += sectionval
        else:
            roll_total -= sectionval
    retstring = ""
    for value in breakdown:
        retstring += str(value)
    retstring += "= " + str(roll_total) + "```"
    return retstring
