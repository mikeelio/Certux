import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingPermissions
import configparser
import mysql.connector
from datetime import date
from discord.utils import get
from discord.ext import tasks
from datetime import datetime
import time




class general(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear (self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def members (self, ctx):
        guild = ctx.guild
        for member in guild.members:
            print(member)



def setup(client):
    client.add_cog(general(client))
