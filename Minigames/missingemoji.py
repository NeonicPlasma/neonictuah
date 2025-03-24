from discord import *
from discord.ui import *

import asyncio
import random
import copy
from typing import *

from game import *
from Helper.__text import *
from Helper.__sets import EMOJI_LIST

class MissingEmoji(Minigame):

    def __init__(self, game: Game):
        super().__init__()

        self.game: Game = game

        self.game_active: bool = False
        self.game_rankings: list[Player] = []

        self.emoji_selection: list[str] = []
        self.answer: str

        self.responses: Dict[Player, int] = {}

    async def start_minigame(self) -> None:
        
        self.game_active = True
        self.can_respond = [player for player in self.game.players.values()]

        # Generate list of 8 unique emojis
        emoji_list: list[str] = copy.deepcopy(EMOJI_LIST)
        for i in range(8):
            self.emoji_selection.append(emoji_list.pop(random.randint(0, len(emoji_list) - 1)))

        # Select a random emoji in the list to not appear
        self.answer = random.choice(self.emoji_selection)

        # Make sure that the answer does not appear in the string sent to players
        emojis_in_string: list[str] = copy.deepcopy(self.emoji_selection)
        emojis_in_string.remove(self.answer)

        # Generate string to show players
        emoji_string_list: list[str] = copy.deepcopy(emojis_in_string)

        while len(emoji_string_list) < 40:
            
            # Add a random emoji to the emoji line
            emoji_string_list.append(random.choice(emojis_in_string))

        # Shuffle around emojis
        random.shuffle(emoji_string_list)

        emoji_string: str = "\n".join(["".join(emoji_string_list[(i * 10):min((i + 1) * 10, len(emoji_string_list))]) for i in range(4)])

        # Create buttons with emojis - generating 2x4 grid
        button_view: View = View(timeout=90)
        for row in range(2):
            for i in range(4):

                emoji_index: int = i + row * 4

                # Create button
                button: Button = ui.Button(style=ButtonStyle.blurple, label="", emoji=f"{self.emoji_selection[emoji_index]}", custom_id=f"{emoji_index}", row=row)
                button.callback = self.on_button_press
                button_view.add_item(button)


        # Create embed display
        embed = Embed(
            color=Colour.blurple(),
            title="Missing Emoji",
            description=f"Click on the emoji **that does __NOT__ appear below:**\n\n{emoji_string}"
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
            player_answer: str = self.emoji_selection[button_id]

            # Record player's answer and prevent them from pressing another button
            self.responses[player] = player_answer

            # Check if player clicked on correct emoji
            if player_answer == self.answer:
                self.game_rankings.append(player)

            # Send response to player, including how fast they were to respond compared to others
            await i_response.send_message(f"You selected {player_answer}\nYou were the **{get_rank_str(len(self.responses))}** to respond.", ephemeral=True)

        except ValueError:
            # Could not parse custom id into number
            await i_response.send_message("An error occured while handling your input: The button ID could not be parsed into an integer.", ephemeral=True)
        except IndexError:
            # button_id was out of index
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