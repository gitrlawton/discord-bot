import requests
import os

import datetime
import pytz

authorization = os.environ['API_KEY']
headers = {
    "Authorization": str(authorization)
}

def check_game_today():

  current_pst = datetime.datetime.now(pytz.timezone('US/Pacific'))
  today_date = str(current_pst)[:10]
  month = today_date[5:7]
  day = today_date[8:10]
  date_formatted = str(int(month)) + "/" + str(int(day)) + "/" + today_date[:4]
  
  game_today_response = requests.get(f"http://api.balldontlie.io/v1/games?dates[]={today_date}&team_ids[]=16", headers=headers)
  
  game_today_dict = game_today_response.json()
  today_game_data = game_today_dict["data"]
  
  
  if len(today_game_data) == 1:
    if today_game_data[0]["status"] == "Final":
      home_team_score = today_game_data[0]["home_team_score"]
      visitor_team_score = today_game_data[0]["visitor_team_score"]
      home_team_name = today_game_data[0]["home_team"]["name"]
      visitor_team_name = today_game_data[0]["visitor_team"]["name"]
      return f"There was a game earlier today.  The final score was {home_team_name} {home_team_score}, {visitor_team_name} {visitor_team_score}."
    raw_time_from_data = today_game_data[0]["status"][11:16]
    if raw_time_from_data[0:2] == "00":
      utc_24h_time_hours = 24
    else:
      utc_24h_time_hours = int(raw_time_from_data[0:2])
    minutes = raw_time_from_data[3:5]
    # Checking Daylight Savings Time or not.
    if str(current_pst.dst())[0] == "1":
      pacific_24h_time_hours = utc_24h_time_hours - 7
    else:
      pacific_24h_time_hours = utc_24h_time_hours - 8
    # Adjusting 24 hour time to 12 hour clock.
    time_of_day_indicator = "AM"
    if (pacific_24h_time_hours > 12):
      pacific_hour = pacific_24h_time_hours - 12
      time_of_day_indicator = "PM"
    else:
      pacific_hour = pacific_24h_time_hours
    # Formulate the today's game message.  
    if today_game_data[0]["home_team"]["id"] == 16:
      opponent = today_game_data[0]["visitor_team"]["full_name"]
      todays_game = "The Miami Heat are playing at home against the " + opponent + f" today ({date_formatted}) at " + str(pacific_hour) + ":" + minutes + f" {time_of_day_indicator} PST."
    else:
      location = " in " + today_game_data[0]["home_team"]["city"]
      opponent = today_game_data[0]["home_team"]["full_name"]
      todays_game = "The Miami Heat are playing the " + opponent +         location + f" today ({date_formatted}) at " + str(pacific_hour) + ":" + minutes + f" {time_of_day_indicator} PST."
  else:
    todays_game = f"The Miami Heat do not have a game today, {date_formatted}."
  
  return todays_game