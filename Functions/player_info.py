import requests
import os

authorization = os.environ['API_KEY']
headers = {
    "Authorization": str(authorization)
}

def player_info():
  # Call the API and store the JSON
  info_response = requests.get("http://api.balldontlie.io/v1/players/79", headers=headers)
  info_dict = info_response.json()
  info_data = info_dict["data"]
  
  
  # Get the values from the keys of the JSON and format them.
  name = "Name: " + info_data["first_name"] + " " + info_data["last_name"]
  height = "Height: " + info_data["height"][0] + "'" + info_data["height"][2:] + '"'
  position = "Position: " + info_data["position"]
  team = "Team: " + info_data["team"]["full_name"]
  weight = "Weight: " + info_data["weight"] + "lbs"
  
  # Compile the formatted values into one string.
  player_info = name + "\n" + height + "\n" + position + "\n" + team + "\n" + weight

  return player_info