import discord
from discord import *
import os
import asyncio
import random
from game import *

class Add(Minigame):

    def __init__(self, game: Game):
        super().__init__()

        self.game: Game = game

        self.game_active: bool = False
        self.can_respond: list = []
        self.game_rankings: list = []


    async def start_minigame(self) -> None:
        
        self.game_active = True
        self.num1: int = random.randint(1, 2)
        self.num2: int = random.randint(1, 2)
        self.answer: int = self.num1 + self.num2

        self.can_respond = [player for player in self.game.players.values()]

        embed = Embed(
            color=Colour.blurple(),
            title="Add Numbers",
            description=f"Type the answer to this equation:\n**{self.num1} + {self.num2}**"
        )
        embed.set_footer(text=f"Round {self.game.round_num}")

        await self.game.channel.send("", embed=embed)

        await asyncio.sleep(10)
        if self.game_active:
            await self.end_responding(True)


    async def on_message(self, message: Message, player_author: Player) -> None:

        # Check if player is able to respond
        if not player_author in self.can_respond:
            return
        
        if self.game_active == False:
            return
        
        # Disable player from responding again
        self.can_respond.remove(player_author)

        # Parse response into number
        response: str = message.content
        answer: int = None

        try:

            answer = int(response)
            # Check if player's answer matches correct answer
            if answer == self.answer:
                self.game_rankings.append(player_author)

        except ValueError:
            # Passing because not giving user a response
            pass

        # Check if all players have responded
        if len(self.can_respond) == 0:
            await self.end_responding(False)
        

    async def end_responding(self, time_out: bool) -> None:

        if self.game_active == False:
            return

        self.game_active = False
        string_list: list = []

        if time_out:
            string_list.append("**Time's up!** ")

        if len(self.game_rankings) == 0:
            string_list.append("**No one got the answer right!** ")
        else:
            string_list.append(f"{self.game_rankings[0].mention()} **was the first to answer correctly!** ")

        string_list.append(f"The answer was **{self.answer}**.")

        await self.game.channel.send("".join(string_list))
        await self.game.end_minigame(self.game_rankings)