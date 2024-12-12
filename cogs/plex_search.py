import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingPermissions
import configparser
from datetime import date
from discord.utils import get
from discord.ext import tasks
from datetime import datetime
import time




class plex_search(commands.Cog):

    def __init__(self,client):
        self.client = client
        
    def search_movies(title):
       movie_list = []
       title = ["21855: Avengers: Age of Ultron", "28128: Avengers: Infinity War"]
       i=0
       for n in title:
        movie_list.append(n.split(': ', 1)[1])
        i=i+1
        
       for n in movie_list:
        print (n)
            
    def get_file_info(directory):       
        list = []
        with open(f'{directory}', 'r') as file:
            for line in file:
                list.append(line.strip())
        return list    

    
    def list (directory):
       file_info = get_file_info (directory) # type: ignore
       list = [] 
       i=0
       for n in file_info:
            list.append(n.split(': ', 1)[1])
            i=i+1
       return list  

    def title_find (directory, movie_title):
        for n in directory:
            index = n.find(movie_title)
            if index == -1: 
                print("-1")
            else:
                return f"{movie_title} is on the plex server"
        return f"{movie_title} does not exist on the server. Please use !plex_request {movie_title}."
    
    
 
 
    @commands.command()
    async def plex_find (self, type, ctx):
        if type.lower() == "movie":
            info = list("movie_list.txt")
            found = title_find(info,ctx) # type: ignore
            await self.ctx.send(found)
        elif type.lower() == "tv":
            await self.ctx.send("")
        elif type.lower() == "anime":
            await self.ctx.send("")
        else:
            await self.ctx.send("List does not exist!! Current lists are Movie, Anime, TV")

    @commands.command()
    async def plex_list (self, type,):
        if type.lower() == "movie":
            info = list("movie_list.txt")
            await self.ctx.send(info)
        elif type.lower() == "tv":
            info = list("tv_list.txt")
            await self.ctx.send(info)
        elif type.lower() == "anime":
            info = list("anime_list.txt")
            await self.ctx.send(info)


def setup(client):
    client.add_cog(plex_search(client))
