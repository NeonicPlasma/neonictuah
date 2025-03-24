import discord
from discord import *
from discord.ui import *
import os
import asyncio
import random
from game import *
from typing import *
from Helper.__text import *

class LargestNum(Minigame):

    def __init__(self, game: Game):
        super().__init__()

        self.game: Game = game

        self.game_active: bool = False
        self.game_rankings: list[Player] = []

        self.num_list: list[int] = []
        self.responses: Dict[Player, int] = {}

        self.answer: int

    async def start_minigame(self) -> None:
        
        self.game_active = True
        self.can_respond = [player for player in self.game.players.values()]

        # Create random numbers and buttons - generating a 4x4 grid
        button_view: View = View(timeout=90)
        for row in range(4):
            for i in range(4):

                # Generate random number, and make sure it is unique to all other numbers
                num: int = random.randint(100, 999)
                while num in self.num_list:
                    num: int = random.randint(100, 999)

                # Create button
                button: Button = ui.Button(style=ButtonStyle.blurple, label=f"{num}", custom_id=f"{i + row * 4}", row=row)
                button.callback = self.on_button_press
                button_view.add_item(button)

                self.num_list.append(num)

                # Check if the number is the current maximum
                if max(self.num_list) == num:
                    self.answer = num        

        # Create embed display
        embed = Embed(
            color=Colour.blurple(),
            title="Largest Number",
            description=f"Click on the button with the **largest number:**"
        )
        embed.set_footer(text=f"Round {self.game.round_num}")
        await self.game.channel.send("", embed=embed, view=button_view)

        await asyncio.sleep(10)
        if self.game_active:
            await self.end_responding(True)


    async def on_button_press(self, interaction: Interaction) -> None:

        i_response: InteractionResponse = interaction.response

        # Don't do any action if game already over
        if self.game_active == False:
            await i_response.defer()
            return

        # Find player that pressed button
        player: Player = self.game.players.get(interaction.user.id, None)
        if player == None:
            await i_response.send_message("You are not in this game!", ephemeral=True)
            return

        # Check if player is able to respond
        if player in self.responses:
            await i_response.send_message("You've already selected a button!", ephemeral=True)
            return
        
        # Process player input
        try:
            button_id: int = int(interaction.data["custom_id"])
            player_answer: int = self.num_list[button_id]

            # Record player's answer and prevent them from pressing another button
            self.responses[player] = player_answer

            # Check if player sent correct response
            if player_answer == self.answer:
                self.game_rankings.append(player)

            # Send response to player, including how fast they were to respond compared to others
            await i_response.send_message(f"You selected **{player_answer}**.\nYou were the **{get_rank_str(len(self.responses))}** to respond.", ephemeral=True)

        except ValueError:
            # Could not parse custom id into number
            await i_response.send_message("An error occured while handling your input: The button ID could not be parsed into an integer.", ephemeral=True)
        except IndexError:
            # Could not find number in num_list
            await i_response.send_message("An error occured while handling your input: The button ID was outside of the list.", ephemeral=True)
        
        # Check if all players have responded
        if len(self.responses) == len(self.game.players):
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