import os
import discord
from covid import Covid
from discord.ext import commands
import wikipedia

DISCORD_KEY = os.getenv('DISCORD_KEY')

discord_client = commands.Bot(command_prefix='!')
covid = Covid(source="worldometers")

@discord_client.event
async def on_ready():
   print(f'{discord_client.user} is online')


#-----!COMMANDS-----#
@discord_client.command()
async def commands(ctx):
   await ctx.channel.send("- !info: displaysa summary of the Covid-19 virus\n"
   + "\n- !cases (country): displays the number of cases of selected country\n" 
   + "\n- !deaths (country): displays the number of deaths of selected country\n"
   + "\n- !recovered (country): displays the number of recovered people of selected country\n"
   + "\n- !tests (country): displays the number of people tested in selected country\n" 
   + "\n- !critical (country): displays the number of people in critical condition in selected country\n"
   + "\n- !rank: displays the rank of countries based on number of deaths") 


#-----!INFO-----#
@discord_client.command()
async def info(ctx):
   try:
      wiki_response = wikipedia.summary("Covid-19", sentences=13)
      await ctx.channel.send(wiki_response)
   except:
      await ctx.channel.send("Wikipedia api error")


#-----!CASES-----#
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


#-----!DEATHS-----#
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


#-----!RECOVERED-----#
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


#-----!TESTS-----#
@discord_client.command()
async def tests(ctx, *args):
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Total Tests in {country}: {int(cas['total_tests']):,}")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!CRITICAL-----#
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


#-----!RANK-----#
@discord_client.command()
async def rank(ctx, *args):
   try:
      if len(args) > 0:
         n = int(''.join(args))
         if n > 15:
            await ctx.channel.send(f"Number of listing can't be greater than 15.")

      else:
         n = 10

      # Rank by total deaths
      data = covid.get_data()
      deaths = sorted([(d['country'], d['deaths']) for d in data], key=lambda x: x[1], reverse=True)

      # Send the first 15
      out = "\n".join([f"{d[0]:<20} - {d[1]:<9,}" for d in deaths[:n]])
      await ctx.channel.send(out)
   except:
      await ctx.channel.send("Invalid Input")

discord_client.run(DISCORD_KEY)