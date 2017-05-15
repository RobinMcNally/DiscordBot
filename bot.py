import discord
import re
import json
import os.path
import sys
import urllib.request
import io
from random import randint
from discord.ext.commands import Bot
from PIL import Image

generic_error = "```I'm just a poor robot. Stop trying to break me!```"
ascii_grayscale = [
        '$','@','B','%','8','&','W','M','#','*',
        'o','a','h','k','b','d','p','q','w','m',
        'Z','O','0','Q','L','C','J','U','Y','X',
        'z','c','v','u','n','x','r','j','f','t',
        '/','\\','|','(',')','1','{','}','[',']',
        '?','-','_','+','~','<','>','i','!','l',
        'I',';',':',',','\"','^','`','\'','.',' '
]

def isInt(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False

#Bot function definitions
laserbot = Bot(command_prefix="!")

@laserbot.event
async def on_read():
    print("Client logged in")

@laserbot.command()
async def asciify(*args):
    if len(args) != 1:
        return await laserbot.say("```Expected single argument of type (Url)```")
    try:
        imagedata = io.BytesIO(urllib.request.urlopen(args[0]).read())
        im = Image.open(imagedata)
        #Convert to grayscale
        im = im.convert("L")
    except Exception as err:
        return await laserbot.say("```" + err + "```")


@laserbot.command()
async def roll(*args):
    breakdown = ['```']
    roll_total = 0
    realarg = ""
    if len(args) < 1:
        return await laserbot.say("```Invalid argument count. Expected: !roll XdY where X is number of dice and Y is dice sides\nExample input: !roll 1d4+1d6+1```")
    for argument in args:
        realarg += argument

    #Saving the keep and keep lowest sections for later: (?:(k|kl)([1-9]\d*))?
    #Section 1 = +, -, or empty string]
    sections = re.findall("(\+|-)?(?:(?:([1-9]\d*)d([1-9]\d*))|([1-9]\d*))", realarg)
    if len(sections) == 0:
        return await laserbot.say("```Invalid command. Expected: !roll XdY where X is number of dice and Y is dice sides\nExample input: !roll 1d4+1d6+1```")
    for section in sections:
        breakdown.append(section[0] + ' ')
        sectionval = 0
        if section[3] != '':
            sectionval = int(section[3])
            breakdown.append(section[3] + ' ')
        else:
            if (not isInt(section[1])) or int(section[1]) > 100 or int(section[1]) < 1:
                return await laserbot.say(generic_error)
            if (not isInt(section[2])) or int(section[2]) > 10000 or int(section[2]) < 1:
                return await laserbot.say(generic_error)
            breakdown.append(section[1] + 'd' + section[2] + "[")
            for die in range(0, int(section[1])):
                dieresult = randint(1, int(section[2]))
                sectionval += dieresult
                breakdown.append(str(dieresult) + ', ')
            breakdown[-1] = breakdown[-1].rstrip(', ')
            breakdown.append("] ");
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
    return await laserbot.say(retstring)

if __name__ == "__main__":
    if not os.path.isfile('OAuth.json'):
        print("Bot cannot execute without OAuth.json")
        sys.exit()

    with open('OAuth.json') as token_file:
        token_data = json.load(token_file)
        if 'OAuthToken' not in token_data:
            print("Malformed OAuth.json")
            sys.exit()
        OAuthToken = token_data['OAuthToken']

    laserbot.run(OAuthToken)
