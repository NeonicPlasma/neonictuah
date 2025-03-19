import discord
from discord import *
import os
import asyncio



class Player():

    def __init__(self, user: User):

        self.user_id: int = user.id
        self.username: str = user.name

        self.game_info: dict = {}
        self.minigame_info: dict = {}




class Game():

    def __init__(self, channel: TextChannel):

        self.channel: TextChannel = channel

        self.active: bool = True
        self.round_num: int = 0

        # Create list of players
        self.players: dict = {}
        self.current_minigame: Minigame = None

        # Game parameters
        self.game_parameters = {}


    def set_players(self, players: set) -> None:
        
        # Clear the current player list
        self.players = {}

        # Add new players to list
        for player in players:
            self.players[player.id] = player


    async def start_game(self):

        await channel.send("The first minigame will begin in 10 seconds!")
        await asyncio.sleep(10)
        

    async def begin_minigame(self):

        self.round_num += 1



    async def on_message(self, message: Message) -> None:
        pass





class Minigame():

    async def on_message(self, message: Message) -> None:
        pass

