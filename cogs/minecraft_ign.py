import discord
import os
from discord.ext import commands
import configparser
from datetime import date
from discord.utils import get
from discord.ext import tasks
from datetime import datetime
from pathlib import Path
from mcuuid import MCUUID
from mcrcon import MCRcon
import random
import string
import requests
import sqlite3

class minecraft_ign(commands.Cog):

    def __init__(self,client):
        self.client = client

    global sqliteConnection
    global cursor
    sqliteConnection = sqlite3.connect('mcbf.db')
    cursor = sqliteConnection.cursor()

    @commands.command()
    @commands.has_role("MCStaff")
    async def mine_ign(self, ctx, server_request, request, *,  ign=None):
        def rcon_server_grab(ctx, server):
            config = configparser.ConfigParser()
            config.read(f'./{server}.ini')
            rcon_ip  =  str(config.get('server_rcon','rcon_ip'))
            rcon_pass =  str(config.get('server_rcon','rcon_pass'))
            rcon_port =  int(config.get('server_rcon','rcon_port'))
            rcon_discord_id =  config.get('server_rcon','rcon_discord_id')

            if int(rcon_discord_id) == int(ctx.guild.id):
                return rcon_ip, rcon_pass, rcon_port, 1

        def db_checker():
            #Check if the user already has a minecraft account assignd to their discord ign

        def ign_uuid(ign):
            url = f'https://api.mojang.com/users/profiles/minecraft/{ign}?'
            response = requests.get(url)
            uuid = response.json()['id']
            return uuid
        def confirm_code(ctx, server_request):
            list = rcon_server_grab(ctx, server_request)
            rcon_ip  = list[0]
            rcon_pass = list[1]
            rcon_port = int(list[2])
            security = list[3]
    
            mcr = MCRcon(rcon_ip,rcon_pass,rcon_port)
            mcr.connect()
    
            num = 0
            code = ""
            while num != 4:
                code = code + random.choice(string.ascii_letters)
                code = code + str(random.randint(3, 9))
                num +=1
            response = mcr.command(f"msg {ign} Here is your code: {code}")
    
            if response == "No player was found":
                ctx.send(f"{ctx.author.mention} You have to be logged into the minecraft server to get your code")
            else:
                ctx.send(f"Check minecraft chat for your confirmation code and reply here!!!")
                confirm = self.client.wait_for("message")
    
                tries= 3
                while str(confirm.content) != str(code):
                    ctx.send(f"Code does not match, try again!!")
                    confirm = self.client.wait_for("message")
                    tries -=1
                    if tries == 0:
                        break


        if ign is None:
            await ctx.send(f"{ctx.author.mention} Please use the command again and include your Minecraft IGN")
        else:
            confirm_code(ctx, server_request)    
            if str(confirm.content) == str(code):
                if security == 1: # type: ignore
                    if request == "add":
                        uuid = ign_uuid(ign)
                        command = f"INSERT INTO Staff (discord_ign, discord_id, minecraft_ign, minecraft_uuid) VALUES ('{ctx.author}', '{ctx.author.id}', '{ign}', '{uuid}')"
                        db_command(command)
    
                        await ctx.send(f"You have registered {ign} to your discord account!!")
                    elif request == "remove":
                        file = Path(f'{server_request}.ini')
                        config = configparser.ConfigParser()
                        config.read(file)
                        config.set(f"server_staff_ign",f"{ctx.author}",f"")
                        config.write(file.open("w"))
                        await ctx.send(f"You have removed {ign} from your discord account!!")
                else:
                    await ctx.send(f"Looks like {ctx.author} used the incorrect server!!")
            else:
                await ctx.send("Sorry but you messed up too many times. \nPlease try again using the command!!")


    @commands.command()
    @commands.has_role("MCStaff")
    async def staff_ign(self, ctx, server_request, user: discord.Member=None):
        config = configparser.ConfigParser()
        config.read(f'./{server_request}.ini')
        rcon_discord_id =  config.get('server_rcon','rcon_discord_id')
        file = discord.File('cogs\mcbf\mcbf.jpg', filename='mcbf.jpg')


        if int(rcon_discord_id) == int(ctx.guild.id):
            security = 1

        if security == 1:



            config = configparser.ConfigParser()
            config.read(f'./{server_request}.ini')
            staff_list =  dict(config.items("server_staff_ign"))
            staff_list = str(staff_list)
            staff_list = staff_list.replace(',',"\n")
            staff_list = staff_list.replace(':',"->")
            staff_list = staff_list.replace("'"," ")
            staff_list = staff_list.replace("{","")
            staff_list = staff_list.replace("}","")

            timestamp = datetime.now()
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            embed = discord.Embed()
            embed.set_author(name=f"Certux - {server_request}", icon_url = self.client.user.avatar_url)
            embed.set_thumbnail(url='attachment://mcbf.jpg')

            embed.add_field(name="\u200b", value = f"Staff IGN",inline=False)
            embed.add_field(name="\u200b", value = f"Discord -- Minecraft IGN",inline=False)

            embed.add_field(name="\u200b", value = f"{staff_list}",inline=False)

            embed.add_field(name="\u200b", value = f"              ")
            embed.set_footer(text=f"CERTUX - {server_request} ({timestamp})")
            reactions= await ctx.send(file = file,embed=embed)


        else:
            await ctx.send(f"Looks like {ctx.author} used the incorrect server!!")

def setup(client):
    client.add_cog(minecraft_ign(client))
