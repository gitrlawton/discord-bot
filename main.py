from nextcord.ext import commands
import asyncio
import json
import nextcord
import os
import schedule
import threading
import time

from Functions import player_info, check_game_today, player_stats


intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)

channel_id = os.environ['CHANNEL_ID']
authorization = os.environ['API_KEY']

headers = {
    "Authorization": str(authorization)
}


# Load the gifs from our json file.
with open("gifs.json") as file:
  links = json.load(file)

## -------------------------API CALLS--------------------------- ##

## ---------------------INSTANCE VARIABLES---------------------- ##

player_information = player_info.player_info()
player_statistics = player_stats.player_stats()
game_today = check_game_today.check_game_today()

  

##--------------------------SCHEDULING---------------------------##

async def send_midnight_message():
  channel = bot.get_channel(int(channel_id))
  await channel.send(game_today)

# async def send_game_start_reminder():
#   channel = bot.get_channel(int(channel_id))
#   await channel.send( )

def schedule_midnight_message():
  loop = asyncio.get_event_loop()
  loop.create_task(send_midnight_message())

# def schedule_game_start_reminder():
#   loop = asyncio.get_event_loop()
#   loop.create_task( )







## --------------------------EVENTS------------------------------ ##


@bot.event
async def on_ready():
  print("Bot is ready")

  channel = bot.get_channel(int(channel_id))

  # Let the users in chat know about the !help command.
  await channel.send("Type !help for a list of commands.")

  # Schedule the messages to be sent out.
  schedule.every().day.at("07:00").do(schedule_midnight_message)
  
  # Run the scheduler in the background
  while True:
      schedule.run_pending()
      await asyncio.sleep(1)


  

@bot.event
async def on_message(message):
  if message.content.startswith("!"):
    # Message is a command. Do not process it here.
    await bot.process_commands(message)
  else:
    # Message is not a command. Check it for gif keywords.
    for (category, gif) in links.items():
      if category in message.content:
        await message.channel.send(gif[0])

## --------------------------COMMANDS---------------------------- ##



@bot.command(name = "gametoday", help = "Returns if there is a Miami Heat game today.")
async def GameToday(context):
  await context.send(game_today)

@bot.command(name = "playerinfo", help = "Returns Jimmy Butler's player profile")
async def PlayerInfo(context):
  await context.send(player_information)

@bot.command(name = "playerstats", help = "Returns Jimmy Butler's current season stats.")
async def PlayerStats(context):
  await context.send(player_statistics)

## -------------------------END COMMANDS------------------------- ##

bot.run(os.environ['TOKEN'])