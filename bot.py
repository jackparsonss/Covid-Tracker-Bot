import os
import discord
from discord.ext import commands

DISCORD_KEY = os.getenv('DISCORD_KEY')

discord_client = commands.Bot(command_prefix='!')

@discord_client.event
async def on_ready():
   print(f'{discord_client.user} is online')

@discord_client.command()
async def commands(ctx):
   await ctx.channel.send("!cases (country): displays the number of cases of selected country\n" 
   + "!rank (country): displays the rank of selected country based on number of cases \n" 
   + "!rate (country): displays the rate of change of cases of selected country\n"
   + "!deaths (country) displays the number of deaths of selected country" )


discord_client.run(DISCORD_KEY)