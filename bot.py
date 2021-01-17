import os
import discord
import wikipedia
from covid import Covid
from discord.ext import commands
from vaccine import Vaccine

DISCORD_KEY = os.getenv('DISCORD_KEY')

discord_client = commands.Bot(command_prefix='!')
covid = Covid(source="worldometers")
vaccine = Vaccine()
vaccine.update_last_indexes()

@discord_client.event
async def on_ready():
   print(f'{discord_client.user} is online')


#-----!COMMANDS-----#
@discord_client.command()
async def commands(ctx):
   # Lists all commands
   await ctx.channel.send("**• !info:** displays a summary of the Covid-19 virus\n"
   + "**• !cases (country)**: displays the number of active cases of selected country\n" 
   + "**• !deaths (country)**: displays the number of deaths of selected country\n"
   + "**• !recovered (country)**: displays the number of recovered people of selected country\n"
   + "**• !tests (country)**: displays the number of people tested in selected country\n" 
   + "**• !vaccines (country)**: displays the total number of vaccines administered in the selected country\n" 
   + "**• !critical (country)**: displays the number of people in critical condition in selected country\n"
   + "**• !rank (int)**: displays the top (param) rank of countries based on number of deaths\n"
   + "**• !total**: displays the global data across multiple criteria\n"
   + "**• !sam:** secret!") 


#-----!SAM-----#
@discord_client.command()
async def sam(ctx):
   # Sends pogsam emote
   try:
      await ctx.channel.send(file=discord.File('pogsam.png'))
   except:
      print('Error sending image')


#-----!INFO-----#
@discord_client.command()
async def info(ctx):
   # Sends short summary of Covid-19
   try:
      wiki_response = wikipedia.summary("Covid-19", sentences=13)
      await ctx.channel.send(wiki_response)
   except:
      await ctx.channel.send("Wikipedia api error")


#-----!CASES-----#
@discord_client.command()
async def cases(ctx, *args):
   # Sends number of cases of given country
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Cases in {country}: ***{int(cas['active']):,}***")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!DEATHS-----#
@discord_client.command()
async def deaths(ctx, *args):
   # Sends number of deaths of given country
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Deaths in {country}: ***{int(cas['deaths']):,}***")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!RECOVERED-----#
@discord_client.command()
async def recovered(ctx, *args):
   # sends number of deaths of given country
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Recoveries in {country}: ***{int(cas['recovered']):,}***")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!TESTS-----#
@discord_client.command()
async def tests(ctx, *args):
   # Sends the number of tests of a given country
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Total Tests in {country}: ***{int(cas['total_tests']):,}***")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!CRITICAL-----#
@discord_client.command()
async def critical(ctx, *args):
   # Sends the number of people in critical condition of a given country
   try:
      if args:
         country = ' '.join(args)
         cas = covid.get_status_by_country_name(f"{country}")
         await ctx.channel.send(f"Critical Cases in {country}: ***{int(cas['critical']):,}***")
      
      else:
         await ctx.channel.send(f"Give a country name")
   except:
      await ctx.channel.send("Invalid Country")


#-----!RANK-----#
@discord_client.command()
async def rank(ctx, *args):
   # Orders countries based off of number of deaths, param controls how many are listed
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
      out = "\n".join([f"{d[0]:<20} - ***{d[1]:<9,}***" for d in deaths[:n]])
      await ctx.channel.send(out)
   except:
      await ctx.channel.send("Invalid Input")


#-----!TOTAL-----#
@discord_client.command()
async def total(ctx):
   # Sends the number of people in critical condition of a given country
   try:
      total = {'Active Cases': covid.get_total_active_cases(), 'Confirmed Cases': covid.get_total_confirmed_cases(), 'Recovered': covid.get_total_recovered(), 'Deaths':covid.get_total_deaths()}

      out = []
      for key, value in total.items():
         out.append(f"***{key}***: {value:,}\n")

      await ctx.channel.send(''.join(out))
      
   except:
      await ctx.channel.send("Error")

#----!VACCINES----#
@discord_client.command()
async def vaccines(ctx, *args):
   try:
      if len(args) == 0:
         await ctx.channel.send("Usage: !vaccines <country_name>")
      
      else:
         country_name = args[0]

         # Do slies for countries

         if (m := vaccine.get_total_vaccinations(country_name)):
            await ctx.channel.send(f"Total Vaccines administered in {country_name}: ***{int(m):,}***")
         
         else:
            await ctx.channel.send(f"No information about {country_name}")
      
   except:
      await ctx.channel.send("Error fetching Vaccine Data")


discord_client.run(DISCORD_KEY)