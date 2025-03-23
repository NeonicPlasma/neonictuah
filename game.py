import discord
from discord import *
import os
import asyncio
import random
from typing import *


class Player():

    def __init__(self, member: Member, game: Game):

        self.user_id: int = member.id
        self.username: str = member.name

        self.game: Game = game
        self.score: int = 0
        self.score_history: set[int] = []


    def add_score(self, points: int, cap: bool) -> None:

        self.score += points
        
        score_goal: int = self.game.game_parameters.get("SCORE_GOAL")
        if cap and self.score >= score_goal:
            if self.game.game_parameters.get("END_ON_WIN", False) == True:
                self.score = self.game.game_parameters.get("SCORE_GOAL") - 1

    
    def mention(self) -> str:

        return f"<@{self.user_id}>"


class Game():

    def __init__(self, channel: TextChannel):

        self.channel: TextChannel = channel

        self.active: bool = False
        self.round_num: int = 0

        # Create list of players
        self.players: Dict[int, Player] = {}
        self.minigame_history: list[Player] = {}
        self.current_minigame: Minigame = None
        self.minigame_list: list[Minigame] = []

        # Game parameters
        self.game_parameters: dict[str, Any] = {
            "SCORING": [5, 2, 1], # The amount of points each placement gets after a minigame
            "SCORE_GOAL": 50, # Amount of points required to win
            "END_ON_WIN": False, # Whether you must end on a winning minigame to win
            "MINIGAME_DELAY": 5, # Amount of time to wait before next minigame
        }



    def add_player(self, member: Member) -> None:
        
        player: Player = Player(member, self)
        self.players[player.user_id] = player



    def remove_player(self, player: Player) -> None:

        self.players.pop(player.user_id)


    def set_minigames(self, minigames: list) -> None:

        self.minigame_list = minigames
        


    async def start_game(self) -> None:

        self.active = True

        await self.channel.send("**Game is starting!**")
        await self.channel.send("The first minigame will begin in 10 seconds!")
        await asyncio.sleep(10)

        await self.start_new_minigame()
        

    async def start_new_minigame(self) -> None:

        self.round_num += 1
        for player in self.players.values():
            player.minigame_info = {}

        # Choose a random minigame from list
        self.current_minigame = random.choice(self.minigame_list)(self)
        await self.current_minigame.start_minigame()


    async def on_message(self, message: Message) -> None:
        
        # Find the player object corresponding to the author of the message
        player_author: Player = self.players.get(message.author.id, None)

        # Check that a player is the one sending the message
        if (player_author == None):
            return
         
        if self.current_minigame != None:
            await self.current_minigame.on_message(message, player_author)



    async def end_minigame(self, player_placements: list) -> None:

        # Erase current minigame
        self.current_minigame = None

        # Add scores to players
        points: int
        placement: int
        point_gains: Dict[Player, int] = {}
        for placement, points in enumerate(self.game_parameters["SCORING"]):
            try:
                player_scoring: Player = player_placements[placement]
                player_scoring.add_score(points, placement == 0)
                point_gains[player_scoring] = points
            except IndexError:
                break

        # Post current leaderboard
        await self.post_leaderboard(point_gains)

        # Check if any player has reached score threshold
        plr: Player
        players_winning: list = [plr for plr in self.players.values() if plr.score >= self.game_parameters.get("SCORE_GOAL")]

        await asyncio.sleep(self.game_parameters["MINIGAME_DELAY"])

        if len(players_winning) > 0:
            await self.game_won(self.get_sorted_players()[0])
        else:
            # Start next minigame
            await self.start_new_minigame()


    
    def get_sorted_players(self) -> list[Player]:

        # Get players sorted
        players_by_points = list(self.players.values())
        players_by_points.sort(key = lambda p: p.score, reverse = True)
        return players_by_points


    
    async def post_leaderboard(self, point_gains: dict) -> None:

        players_sorted: list = self.get_sorted_players()
        leaderboard_strings = []

        current_score: int = 0
        rank: int = 0

        for i, player in enumerate(players_sorted):
            
            if (player.score < current_score):
                rank = i + 1
                current_score = player.score

            if player in point_gains:
                leaderboard_strings.append(f"{rank}. {player.mention()} - **{player.score}** (+{point_gains.get(player, 0)})")
            else:
                leaderboard_strings.append(f"{rank}. {player.mention()} - **{player.score}**")

        await self.channel.send("\n".join(leaderboard_strings))
    

    async def game_won(self, winning_player: Player) -> None:

        await self.channel.send(f"**{winning_player.mention()} has won!**")






class Minigame():

    def __init__(self):
        pass

    async def start_minigame(self) -> None:
        pass

    async def on_message(self, message: Message) -> None:
        pass
        