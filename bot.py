import discord
import re
from random import randint
from discord.ext.commands import Bot

laserbot = Bot(command_prefix="!")

@laserbot.event
async def on_read():
    print("Client logged in")

@laserbot.command()
async def roll(*args):
    ret = []
    if len(args) != 1:
        return await laserbot.say("Invalid argument count. Expected: !roll XdY where X is number of dice and Y is dice sides")
    if not re.match("^[0-9]+d[0-9]+((k|kl)[0-9]+)?$", args[0]):
        return await laserbot.say("Invalid die format. Expected: !roll XdY where X is number of dice and Y is dice sides")
    command = args[0].split('d')
    numdice = int(command[0])
    numsides = int(command[1])
    for die in range(0, numdice):
        ret.append(randint(1, numsides))
    return await laserbot.say(ret)

laserbot.run("")
