import requests
import os

authorization = os.environ['API_KEY']
headers = {
    "Authorization": str(authorization)
}

def player_stats():
  # Call the API and store the JSON
  stats_response = requests.get("https://api.balldontlie.io/v1/season_averages?season=2023&player_ids[]=79", headers=headers)
  stats_dict = stats_response.json()
  stats_data = stats_dict["data"]
  
  
  # Get the values from the keys of the JSON and format them.
  season = "Season: 2023-2024"
  gamesPlayed = "Games played: " + str(stats_data[0]["games_played"])
  
  minutes = int(stats_data[0]["min"][:2])
  rawSeconds = int(stats_data[0]["min"][3:])
  seconds = round(rawSeconds / 60, 1)
  totalMinutes = "Minutes per game: " + str(minutes + seconds)
  points = "Points per game: " + str(round(stats_data[0]["pts"], 1))
  rebounds = "Rebounds per game: " + str(round(stats_data[0]["reb"], 1))
  assists = "Assists per game: " + str(round(stats_data[0]["ast"], 1))
  steals = "Steals per game: " + str(round(stats_data[0]["stl"], 1))
  blocks = "Blocks per game: " + str(round(stats_data[0]["blk"], 1))
  turnovers = "Turnovers per game: " + str(round(stats_data[0]["turnover"], 1))
  fieldGoalPercentage = "Field Goal percentage: " + str(round(stats_data[0]["fg_pct"] * 100, 1)) + "%"
  threePointPercentage = "Three Point percentage: " + str(round(stats_data[0]["fg3_pct"] * 100, 1)) + "%"
  freeThrowPercentage = "Free Throw percentage: " + str(round(stats_data[0]["ft_pct"] * 100, 1)) + "%"
  
  # Compile the formatted values into one string.
  season_stats = season + "\n" + gamesPlayed + "\n" + totalMinutes + "\n" + points + "\n" + rebounds + "\n" + assists + "\n" + steals + "\n" + blocks + "\n" + turnovers + "\n" + fieldGoalPercentage + "\n" + threePointPercentage + "\n" + freeThrowPercentage

  return season_stats