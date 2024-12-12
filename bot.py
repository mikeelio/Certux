#Import classes
import discord
from discord.ext import commands
import os
from os import system
import time
import configparser
import shutil
import configparser
from discord.utils import get
import datetime
from discord.ext import tasks

#Setting up the bot
intents = discord.Intents.default()
intents.all()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    activity = discord.Activity(name='Coding Simulator', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print (client.user.name+' Bot is ready.')
    refresh.start()

#-------------------------------------------------------------------#
#-----------------------------[Commands]----------------------------#
#-------------------------------------------------------------------#


#Reload single command
@client.command()
async def reload(ctx, file=None):
    author = str(ctx.author.id)
    if author == owner_id:
        if file is None:
            await ctx.send("Hold up you forgot something")
            time.sleep(2)
            await ctx.channel.purge(limit=2)

        elif file == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.load_extension(f'cogs.{filename[:-3]}')

            await ctx.send("All Cogs have been reloaded")
            time.sleep(2)
            await ctx.channel.purge(limit=2)
            print("Bot was reloaded")
        else:
            client.unload_extension(f'cogs.{file}')
            await ctx.send(f"{file} has been unloaded.")
            time.sleep(2)
            client.load_extension(f'cogs.{file}')
            await ctx.send(f"{file} has been loaded.")
            time.sleep(2)
            await ctx.channel.purge(limit=4)
            print("Bot was reloaded")
    else:
        await ctx.send("Sorry but only mikeelio (THE OWNER) can run this command")


#loads all cogs at startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@tasks.loop(minutes=1)
async def refresh():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.reload_extension(f'cogs.{filename[:-3]}')
    e = datetime.datetime.now()
    e = e.strftime("%Y-%m-%d %I:%M:%S %p")

    print(f"Bot has refreshed at: {e} ")


#Assigns the bot to the token
config = configparser.ConfigParser()
config.read('../token.ini')
token = config.get('token', 'token')
owner_id = str(config.get('token','id'))
bot_id = str(config.get('token','bot_id'))

client.run(token)
