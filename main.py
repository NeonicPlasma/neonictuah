import discord
from discord import *
import os
from Helper.__config import CLIENT

from event import NewEvent

@CLIENT.event
async def on_ready():
    print("=====================================")
    print("Starting up neonictuah!")

    await CLIENT.add_cog(NewEvent(CLIENT))
    

# Startup bot
if __name__ == "__main__":
    CLIENT.run(os.getenv("CUBE_BOT_TOKEN"))