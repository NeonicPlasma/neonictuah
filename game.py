import discord
from discord import *
import os
import asyncio



class Player():

    def __init__(self, member: Member):

        self.user_id: int = member.id
        self.username: str = member.name

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
        self.game_parameters: dict = {}


    def add_player(self, member: Member) -> None:
        
        player: Player = Player(member)
        self.players[player.user_id] = player


    def remove_player(self, player: Player) -> None:

        self.players.pop(player.user_id)
        

    async def start_game(self) -> None:

        await channel.send("The first minigame will begin in 10 seconds!")
        await asyncio.sleep(10)
        

    async def begin_minigame(self) -> None:

        self.round_num += 1



    async def on_message(self, message: Message) -> None:
        pass





class Minigame():

    async def on_message(self, message: Message) -> None:
        pass

