import discord
import os
from discord.ext import commands
import configparser
from datetime import date
from discord.utils import get
from discord.ext import tasks
from datetime import datetime
from mcrcon import MCRcon
import asyncio
from typing import Union

global moderator
global rcon_ip
global rcon_pass
global rcon_port

global reactions
global emoji
emoji = ['✅','❌']

class minecraft_rcon(commands.Cog):

    def __init__(self,client):
        self.client = client





    @commands.command()
    @commands.has_role("MCStaff")
    async def rcon(self, ctx, server_request, *,  command):

        def minecraft_commands(self, ctx, s, command):
            if 'ban' == s:
                command = f"{command} | Banned by {ctx.author}"
                return command
            elif 'pardon' == s:
                answer = command[2]
                output = f" Unbanned by {ctx.author}\nReason: {answer}"
                return output

        def rcon_server_grab(ctx, server):

            config = configparser.ConfigParser()
            config.read(f'./{server}.ini')
            rcon_ip  =  str(config.get('server_rcon','rcon_ip'))
            rcon_pass =  str(config.get('server_rcon','rcon_pass'))
            rcon_port =  int(config.get('server_rcon','rcon_port'))
            rcon_discord_id =  config.get('server_rcon','rcon_discord_id')


            if int(rcon_discord_id) == int(ctx.guild.id):
                return rcon_ip, rcon_pass, rcon_port, 1

        def check(r: discord.Reaction, u: Union[discord.Member,discord.User]):
            return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in ["\U00002705", "\U0000274c"]
        response=""

        def minecraft_ign_retrieve(ctx, server):
            config = configparser.ConfigParser()
            config.read(f'./{server}.ini')
            ign  =  str(config.get('server_staff_ign',f'{ctx.author}'))
            return ign

        moderator_commands = ["ban","ban-ip","mute","kick","whisper","message"]
        await ctx.channel.purge(limit = 1)
        s = command.split()[0]

        list = rcon_server_grab(ctx, server_request)
        admin = discord.utils.find(lambda r: r.name == 'Admin', ctx.guild.roles)
        moderator = discord.utils.find(lambda r: r.name == 'Moderator', ctx.guild.roles)
        rcon_ip  = list[0]
        rcon_pass = list[1]
        rcon_port = int(list[2])
        security = list[3]

        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")


        if security == 1:
            #mcr = MCRcon("127.0.0.1","test",25587)
            mcr = MCRcon(rcon_ip,rcon_pass,rcon_port)
            mcr.connect()

            embed = discord.Embed()
            embed.set_author(name="Certux - Rcon", icon_url = self.client.user.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="\u200b", value = f"RCON REQUEST BY STAFF: {ctx.author}")
            embed.add_field(name="\u200b", value = f"STAFF COMMAND REQUEST: {command}")
            embed.add_field(name="\u200b", value = f"                                ")
            embed.add_field(name="\u200b", value = f"PLEASE CONFIRM COMMAND BELOW ✅ OR ❌ within 10 seconds")
            embed.set_footer(text=f"CERTUX - RCON REQUEST ({timestamp})")
            reactions= await ctx.send(embed=embed)

            counter = 1
            for react in emoji:
                if counter == -1:
                    break
                await reactions.add_reaction(react)
                counter -=1

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = check, timeout = 10.0)
            except asyncio.TimeoutError:
                await ctx.channel.purge(limit = 1)
                await ctx.send(f"*{ctx.author}*, you didnt react with a ✅ or ❌ in 10 seconds. Request Denied")
            else:
                if str(reaction.emoji) ==  "\U00002705":
                    if admin in ctx.author.roles:
                        output = minecraft_commands(self, ctx, s, command)
                        response = mcr.command(f"{output}")
                    elif moderator in ctx.author.roles:
                        if s in moderator_commands:
                            output = minecraft_commands(self, ctx, s, command)
                            response = mcr.command(f"{output}")
                        else:
                            await ctx.send(f"{ctx.author.mention} Sorry but you dont have the permissions needed.")

                    ign = minecraft_ign_retrieve(ctx, server_request)

                    await ctx.channel.purge(limit = 1)
                    embed = discord.Embed()
                    embed.set_author(name="Certux - Rcon", icon_url = self.client.user.avatar_url)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.add_field(name="\u200b", value = f"RCON REQUEST BY STAFF: {ctx.author} / {ign}")
                    embed.add_field(name="\u200b", value = f"STAFF COMMAND REQUEST: {command}")
                    embed.add_field(name="\u200b", value = f"SERVER OUTPUT: {response}")
                    embed.set_footer(text=f"CERTUX - RCON REQUEST ({datetime.now()})")
                    reactions= await ctx.send(embed=embed)
                else:
                    await ctx.channel.purge(limit = 1)
                    await ctx.send(f"Request has been rejected by {ctx.author}")
                #await ctx.send(f"Staff: {ctx.author}\nInput: {command}\nOutput: {response}\nDate/Time: {datetime.now()}")




        else:
            await ctx.send(f"{ctx.author.mention} You have requested the wrong server/ unknown server")



def setup(client):
    client.add_cog(minecraft_rcon(client))
