import json
import os.path
import sys
import urllib.request
from features.roll_backend import roll_backend
from features.asciify_backend import asciify_backend
from discord.ext.commands import Bot

generic_error = "```I'm just a poor robot. Stop trying to break me!```"

#Bot function definitions
bot = Bot(command_prefix="!")

@bot.event
async def on_read():
    print("Client logged in")

@bot.command()
async def asciify(*args):
    return await bot.say("Asciify coming soon")
    

@bot.command()
async def roll(*args):
    return await bot.say(roll_backend(args))

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

    bot.run(OAuthToken)
