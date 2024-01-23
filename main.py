import discord
import requests, json
import os

intents = discord.Intents.all()
client = discord.Client(intents = intents)

# Load the gifs from gifs.json
with open("gifs.json") as file:
  links = json.load(file)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!help'):
    await message.channel.send("!help - Shows this message\n!info_player - Returns Jimmy Butler's player profile\nGIFs: [emo, cmon, take it, point, eyes, timeout, kiss, oh yeah, shots, what?]\n!stats_player - Returns Jimmy Butler's current season stats.")


  if message.content.startswith("!info_player"):
    # Call the API and store the JSON
    response = requests.get("https://www.balldontlie.io/api/v1/players/79")
    
    # Get the values from the keys of the JSON and format them.
    name = "Name: " + response.json()["first_name"] + " " + response.json()["last_name"]
    height = "Height: " + str(response.json()["height_feet"]) + "'" + str(response.json()["height_inches"]) + '"'
    position = "Position: " + response.json()["position"]
    team = "Team: " + response.json()["team"]["full_name"]
    weight = "Weight: " + str(response.json()["weight_pounds"]) + "lbs"
    
    # Send the formatted values to the discord channel.
    await message.channel.send(name)
    await message.channel.send(height)
    await message.channel.send(position)
    await message.channel.send(team)
    await message.channel.send(weight)

  if message.content.startswith("!stats_player"):
    response = requests.get("https://www.balldontlie.io/api/v1/season_averages?season=2023&player_ids[]=79")

    season = "Season: " + str(response.json()["data"][0]["season"]) + "-" + str(response.json()["data"][0]["season"] + 1)
    gamesPlayed = "Games Played: " + str(response.json()["data"][0]["games_played"])
    rawMinutes = str(response.json()["data"][0]["min"])
    minutes = "Minutes per game: " + rawMinutes[:2] + "." + rawMinutes[3:]
    points = "Points per game: " + str(response.json()["data"][0]["pts"])
    rebounds = "Rebounds per game: " + str(response.json()["data"][0]["reb"])
    assists = "Assists per game: " + str(response.json()["data"][0]["ast"])
    steals = "Steals per game: " + str(response.json()["data"][0]["stl"])
    blocks = "Blocks per game: " + str(response.json()["data"][0]["blk"])
    turnovers = "Turnovers per game: " + str(response.json()["data"][0]["turnover"])
    fieldGoalPercentage = "Field Goal percentage: " + str(response.json()["data"][0]["fg_pct"] * 100) + "%"
    threePointPercentage = "Three Point percentage: " + str(response.json()["data"][0]["fg3_pct"] * 100) + "%"
    freeThrowPercentage = "Free Throw percentage: " + str(response.json()["data"][0]["ft_pct"] * 100) + "%"

  await message.channel.send(season)
  await message.channel.send(gamesPlayed)
  await message.channel.send(minutes)
  await message.channel.send(points)
  await message.channel.send(rebounds)
  await message.channel.send(assists)
  await message.channel.send(steals)
  await message.channel.send(blocks)
  await message.channel.send(turnovers)
  await message.channel.send(fieldGoalPercentage)
  await message.channel.send(threePointPercentage)
  await message.channel.send(freeThrowPercentage)
  

  # Detect names of gifs in user's comments.
  for (category, gif) in links.items():
    if category in message.content:
      await message.channel.send(gif[0])


client.run(os.environ['TOKEN'])