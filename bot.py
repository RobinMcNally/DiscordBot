import discord
import re
import json
import os.path
import sys
from random import randint
from discord.ext.commands import Bot

if not os.path.isfile('OAuth.json'):
    print("Bot cannot execute without OAuth.json")
    sys.exit()

with open('OAuth.json') as token_file:
    token_data = json.load(token_file)
    if 'OAuthToken' not in token_data:
        print("Malformed OAuth.json")
        sys.exit()
    OAuthToken = token_data['OAuthToken']

laserbot = Bot(command_prefix="!")

@laserbot.event
async def on_read():
    print("Client logged in")

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

laserbot.run(OAuthToken)
