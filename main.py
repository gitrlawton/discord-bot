import asyncio
import datetime
import json
import nextcord
import os
import requests
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!", intents = intents)

channel_id = os.environ['CHANNEL_ID']

current_time = datetime.datetime.now()
today_date = str(current_time)[:10]


# Load the gifs from our json file.
with open("gifs.json") as file:
  links = json.load(file)

## ----------------------API CALLS------------------------------- ##

## PLAYER INFO ##

# Call the API and store the JSON
info_response = requests.get("https://www.balldontlie.io/api/v1/players/79")

# Get the values from the keys of the JSON and format them.
name = "Name: " + info_response.json()["first_name"] + " " + info_response.json()["last_name"]
height = "Height: " + str(info_response.json()["height_feet"]) + "'" + str(info_response.json()["height_inches"]) + '"'
position = "Position: " + info_response.json()["position"]
team = "Team: " + info_response.json()["team"]["full_name"]
weight = "Weight: " + str(info_response.json()["weight_pounds"]) + "lbs"

# Compile the formatted values into one string.
player_info = name + "\n" + height + "\n" + position + "\n" + team + "\n" + weight

## PLAYER STATS ##

# Call the API and store the JSON
stats_response = requests.get("https://www.balldontlie.io/api/v1/season_averages?season=2023&player_ids[]=79")

# Get the values from the keys of the JSON and format them.
season = "Season: " + str(stats_response.json()["data"][0]["season"]) + "-" + str(stats_response.json()["data"][0]["season"] + 1)
gamesPlayed = "Games Played: " + str(stats_response.json()["data"][0]["games_played"])
rawMinutes = str(stats_response.json()["data"][0]["min"])
minutes = "Minutes per game: " + rawMinutes[:2] + "." + rawMinutes[3:]
points = "Points per game: " + str(stats_response.json()["data"][0]["pts"])
rebounds = "Rebounds per game: " + str(stats_response.json()["data"][0]["reb"])
assists = "Assists per game: " + str(stats_response.json()["data"][0]["ast"])
steals = "Steals per game: " + str(stats_response.json()["data"][0]["stl"])
blocks = "Blocks per game: " + str(stats_response.json()["data"][0]["blk"])
turnovers = "Turnovers per game: " + str(stats_response.json()["data"][0]["turnover"])
fieldGoalPercentage = "Field Goal percentage: " + str(stats_response.json()["data"][0]["fg_pct"] * 100) + "%"
threePointPercentage = "Three Point percentage: " + str(stats_response.json()["data"][0]["fg3_pct"] * 100) + "%"
freeThrowPercentage = "Free Throw percentage: " + str(stats_response.json()["data"][0]["ft_pct"] * 100) + "%"

# Compile the formatted values into one string.
season_stats = season + "\n" + gamesPlayed + "\n" + minutes + "\n" + points + "\n" + rebounds + "\n" + assists + "\n" + steals + "\n" + blocks + "\n" + turnovers + "\n" + fieldGoalPercentage + "\n" + threePointPercentage + "\n" + freeThrowPercentage

# Call the API and store the JSON
game_today_response = requests.get(f"https://www.balldontlie.io/api/v1/games?dates[]={today_date}&team_ids[]=16")

today_game_data = game_today_response.json()["data"]

if len(today_game_data) == 1:
  if today_game_data[0]["home_team"]["id"] == 16:
    opponent = today_game_data[0]["visitor_team"]["full_name"]
    todays_game = "The Miami Heat are playing at home against the "     + opponent + " today."
  else:
    location = " at " + today_game_data[0]["home_team"]["city"]
    opponent = today_game_data[0]["home_team"]["full_name"]
    todays_game = "The Miami Heat are playing the " + opponent +         location + " today."
else:
  todays_game = "The Miami Heat do not play today."

## --------------------------EVENTS------------------------------ ##


@bot.event
async def on_ready():
  print("Bot is ready")

  channel = bot.get_channel(int(channel_id))

  # Let the users in chat know about the !help command.
  await channel.send("Type !help for a list of commands.")
  

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

## --------------------------COMMANDS----------------------------- ##

@bot.command(name = "gametoday", help = "Returns if there is a Miami Heat game today.")
async def GameToday(context):
  await context.send(todays_game)

@bot.command(name = "playerinfo", help = "Returns Jimmy Butler's player profile")
async def PlayerInfo(context):
  await context.send(player_info)

@bot.command(name = "playerstats", help = "Returns Jimmy Butler's current season stats.")
async def PlayerStats(context):
  await context.send(season_stats)

## -------------------------END COMMANDS-------------------------- ##

bot.run(os.environ['TOKEN'])