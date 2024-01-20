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

  if message.content.startswith("!hello"):
    await message.channel.send("Hello!")

  if message.content.startswith("!info player"):
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

  # Detect names of gifs in user's comments.
  for (category, gif) in links.items():
    if category in message.content:
      await message.channel.send(gif[0])


client.run(os.environ['TOKEN'])