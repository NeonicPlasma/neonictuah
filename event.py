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
        self.current_games = {}



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
        
        # Check if game already exists in this channel
        channel_id: int = ctx.channel.id
        if (ctx.channel.id in self.current_games):
            await ctx.send("Game already exists in this channel")
            return
        
        # Check if command was run in a text channel
        if ctx.channel.guild == None or (not isinstance(ctx.channel, dc.TextChannel)):
            await ctx.send("Games can only be ran in text channels!")
            return
        
        # Create game with the channel as a room, storing it in the games dictionary
        self.current_games[channel_id] = Game(ctx.channel)
        await ctx.send("Game has been created!")


    @game.command("join")
    async def game_join(self, ctx: cmd.Context):
        
        # Check if game currently running in this channel
        channel_id: int = ctx.channel.id
        current_game: Game = self.current_games.get(channel_id, None)
        if current_game == None:
            await ctx.send("No game running in this channel")
            return
    
        # Check if the game has already started
        if current_game.active == True:
            await ctx.send("Is already active")
            return
        
        # Check if this player is already in the game
        user_id: int = ctx.author.id
        if user_id in current_game.players:
            await ctx.send("You are already in this game")
            return
        
        # Add player to game
        current_game.add_player(ctx.author)
        await ctx.send(f"**{ctx.author.mention} has joined the game!** Current player count is **{len(current_game.players)}**.")
    

    @game.command("start")
    async def game_start(self, ctx: cmd.Context) -> None:
        
        channel_id: int = ctx.channel.id
        current_game: Game = self.current_games.get(channel_id, None)
        if (current_game == None):
            await ctx.send("No game running in this channel")
            return
    
        if current_game.active == True:
            await ctx.send("Is already active")
            return
        
        # Check if game has less than 2 players
        if len(current_game.players) < 2:
            await ctx.send("Not enough players")
            return
        
        # Start game
        await current_game.start_game()


