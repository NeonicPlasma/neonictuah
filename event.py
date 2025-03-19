import discord as dc
from discord.ext import commands as cmd
from collections.abc import *
from typing import *

from game import Game

import os
import copy



class NewEvent(cmd.Cog):




    def __init__(self, client: dc.Client):

        self.bot: dc.Client = client
        self.current_game = None



    @cmd.Cog.listener("on_message")
    async def on_message(self, message: dc.Message):

        # Retrieve message information
        author: dc.Member = message.author
        channel: dc.TextChannel = message.channel


    @cmd.group("game")
    async def game(self, ctx: cmd.Context):
        pass
        
        
    @game.command("create")
    async def game_create(self, ctx: cmd.Context):
        
        if self.current_game != None:
            await ctx.send("There is currently an ongoing game! Wait until the current game is over.")
            return
        
        # 
        if ctx.channel.guild != None or (not isinstance(ctx.channel, dc.TextChannel)):
            await ctx.send("Games can only be ran in text channels!")
            return
        
        # Create game with the channel as a room
        self.current_game = Game(ctx.channel)
        await ctx.send("Game has been created!")


    @game.command("join")
    async def game_join(self, ctx: cmd.Context):
        
        if self.current_game == None:
            await ctx.send("There is currently no ongoing game")
            return
        
        game_channel: dc.TextChannel = self.current_game.channel
        if game_channel.id != ctx.channel.id:
            await ctx.send("There is currently no ongoing game in this channel")
            return
        
        


    @game.command("create")
    async def game_create(self, ctx: cmd.Context):
        await ctx.send("POKKEN 😭😭😭😭😭😭😭😭😭😭😭😭😭😭")


