import os
import discord
from covid import Covid
from discord.ext import commands

DISCORD_KEY = os.getenv('DISCORD_KEY')

discord_client = commands.Bot(command_prefix='!')
covid = Covid(source="worldometers")

@discord_client.event
async def on_ready():
   print(f'{discord_client.user} is online')

@discord_client.command()
async def commands(ctx):
   await ctx.channel.send("!cases (country): displays the number of cases of selected country\n" 
   + "!rank: displays the rank of countries based on number of cases \n" 
   + "!rate (country): displays the rate of change of cases of selected country\n"
   + "!deaths (country): displays the number of deaths of selected country"
   + "!recovered (country): displays the number of recovered people of selected country" )

@discord_client.command()
async def cases(ctx, *args):
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Cases in {country}: {int(cas['active']):,}")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")
   
@discord_client.command()
async def rank(ctx, *args):
   pass


@discord_client.command()
async def deaths(ctx, *args):
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Deaths in {country}: {int(cas['deaths']):,}")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


@discord_client.command()
async def recovered(ctx, *args):
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Recoveries in {country}: {int(cas['recovered']):,}")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


@discord_client.command()
async def critical(ctx, *args):
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Critical Cases in {country}: {int(cas['critical']):,}")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")

discord_client.run(DISCORD_KEY)