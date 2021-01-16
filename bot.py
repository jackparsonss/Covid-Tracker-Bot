import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_KEY = os.getenv('DISCORD_KEY')

discord_client = commands.Bot(command_prefix='!')

@discord_client.event
async def on_ready():
   print(f'{discord_client.user} is online')

@discord_client.command()
async def hello(ctx):
   await ctx.channel.send("world")


discord_client.run(DISCORD_KEY)