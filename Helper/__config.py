from discord import *
from discord.ext.commands import Bot

PREFIX: str = "n/"

# Set intents
intents: Intents = Intents.default()
intents.members = True
intents.message_content = True

# Create client
CLIENT: Bot = Bot(command_prefix=PREFIX, intents=intents)
