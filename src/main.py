import os
import json

from constants import SITENAMES
from keep_alive import keep_alive
from replit import db
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Successfully logged in as {}".format(bot.user))

@bot.event
async def on_message(message):
    
    await bot.process_commands(message)
    await message.channel.purge(limit=None, check=lambda msg: not msg.pinned)


@bot.command()
async def request(ctx, *args):

    request = ""
    for arg in args:
        request = request + " " + arg

    requests = db["requests"]
    requests[ctx.author.id] = request
    db["requests"] = requests

    await ctx.author.send("Your request has been added!")


@bot.command()
async def requests(ctx):
    requests = db["requests"]

    message = "Here are all the open requests:\n```"
    for key in requests:
        message = "{}\n{}: {}".format(message, bot.get_user(key),
                                      requests[key])
    message = message + "```"
    
    await ctx.channel.send(message)

@bot.command()
async def username(ctx, *args):
    prefix = "username_" + str(ctx.author.id) + "_"
    if  len(args) == 2:
      if args[0].lower() in SITENAMES:
        db[prefix + args[0].lower()] = args[1]
        await ctx.send(ctx.author.mention + " Your username on " + args[0].lower() + " is now saved as " + args[1] + ".")
        return 0

    if args[0] == "status":
      
      savedNamesKeys = db.prefix(prefix)
      if len(savedNamesKeys) == 0:
        await ctx.send(ctx.author.mention + " You haven't saved a username yet.")
      else:
        message = ctx.author.mention + " Here are your saved usernames for the different websites:"
        for sitename in SITENAMES:
          if prefix + sitename in savedNamesKeys:
            message += "\r\n" + sitename.capitalize() + " : " + db[prefix + sitename]
        await ctx.send(message)
      return 0
    await ctx.send(ctx.author.mention + " To use this command blablabla...") #TODO : add an actual help message 
    return 1

keep_alive()
bot.run(os.getenv("TOKEN"))
