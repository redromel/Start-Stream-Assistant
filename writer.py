import json
import os
from nicegui import ui
import requests
from constants import *
from queries import PLAYER_QUERY
from query_parser import player_parse
import shutil


def bracket_writer(set_data, setup=False):

    for set_data in set_data:

        dir = set_data["identifier"] + "_" + set_data["fullRoundText"]
        path = "bracket_info/" + dir

        if os.path.exists(path) == False:
            os.mkdir(path)

        playerCount = 1
        for match_data in set_data["slots"]:

            if match_data["entrant"] != None:
                player = match_data["entrant"]["name"]
            else:
                player = ""

            if match_data["standing"] != None:
                score = match_data["standing"]["stats"]["score"]["value"]
                if score == -1:
                    score = "DQ"
                if score == None:
                    score = ""
            else:
                score = ""

            player_path = (
                path
                + "/"
                + set_data["identifier"]
                + "_player"
                + str(playerCount)
                + "_name.txt"
            )
            score_path = (
                path
                + "/"
                + set_data["identifier"]
                + "_player"
                + str(playerCount)
                + "_score.txt"
            )

            if setup == True:
                player = "Setup"
                score = "N"
            f = open(player_path, "w")
            f.write(player)
            f.close()

            f = open(score_path, "w")
            f.write(str(score))
            f.close()

            playerCount = playerCount + 1


def scoreboard_json_writer(set_data):

    bracket_data = {}
    players = []
    path = "match_info/"

    if os.path.exists(path) == False:
        os.mkdir(path)

    if is_final_phase(set_data) == False:
        round = set_data["set"]["phaseGroup"]["phase"]["name"]
    else:
        round = set_data["set"]["fullRoundText"]

    bracket_data["id"] = set_data["set"]["id"]
    bracket_data["round"] = round

    for player_info in set_data["set"]["slots"]:
        player = player_info_builder(player_info)
        players.append(player)

    bracket_data["players"] = players
    bracket_json = json.dumps(bracket_data)

    f = open(path + "/bracket_data.json", "w")
    f.write(bracket_json)
    f.close()

    return bracket_json


def scoreboard_writer(bracket_json):

    bracket_data = json.loads(bracket_json)
    path = "match_info/"

    if os.path.exists(path) == False:
        os.mkdir(path)

    for match_data in bracket_data:
        match_path = path + "match_" + str(match_data) + ".txt"

        if not isinstance(bracket_data[match_data], list):
            f = open(match_path, "w")
            f.write(str(bracket_data[match_data]))
            f.close()

        else:

            player_count = 0
            for players in bracket_data[match_data]:
                player_count = player_count + 1
                for player_data in players:
                    player_path = (
                        path
                        + "player_"
                        + str(player_count)
                        + "_"
                        + player_data
                    )

                    if player_data == "state" or player_data == "country":
                      get_flag(players[player_data], player_path, player_data)

                        
                        
                    else:
                      f = open(str(player_path + ".txt"), "w")
                      f.write(str(players[player_data]))
                      f.close()

    return


def get_flag(location, destination_path, location_type):
    if location == None:
      f = open(str(destination_path + ".txt"), "w")
      f.write("None")
      f.close()
      return
    
    # prioritizes state before country
    flag_path = "state_flags_rounded/" + str(location).lower() + ".png"
    
    if location_type == 'state':
      flag_path = "state_flags_rounded/" + str(location).lower() + ".png"
    if location_type == 'country':
      code = get_code(location)
      
      flag_path = "country_flags_rounded/" + str(code).lower() + ".png"
  
    shutil.copy(flag_path,str(destination_path + ".png"))
    

def get_code(country):
  
  with open("countries.json","r") as file:
    countries_data = json.load(file)

  for countries in countries_data:
    if str(countries["name"]).lower() == str(country).lower():
      return str(countries["code"]).lower()
  
  
  




def is_final_phase(set_data):
    phase_number = set_data["set"]["phaseGroup"]["phase"]["phaseOrder"]
    if phase_number <= TOTAL_PHASES:
        return True
    return False


def player_info_builder(entrant_data):
    player = {}
    if entrant_data["entrant"]["participants"][0]["user"] != None:
        player_id = entrant_data["entrant"]["participants"][0]["user"]["player"]["id"]

        location_gender_info = player_parse(get_player(player_id))

        player["id"] = entrant_data["entrant"]["id"]
        player["gamertag"] = entrant_data["entrant"]["name"]
        player["genderPronoun"] = location_gender_info["genderPronoun"]
        player["state"] = location_gender_info["location"]["state"]
        player["country"] = location_gender_info["location"]["country"]
        player["score"] = entrant_data["standing"]["stats"]["score"]["value"]
        if player["score"] == None:
            player["score"] = 0

    # Will only happen if person is not registered for start.gg
    else:
        player["id"] = entrant_data["entrant"]["id"]
        player["gamertag"] = entrant_data["entrant"]["name"]
        player["genderPronoun"] = None
        player["state"] = None
        player["country"] = None
        player["score"] = entrant_data["standing"]["stats"]["score"]["value"]

        if player["score"] == None:
            player["score"] = 0

    return player


def get_player(player_id):
    player_vars = {"playerId": player_id}
    player_payload = {"query": PLAYER_QUERY, "variables": player_vars}

    player_response = requests.post(url=API_URL, json=player_payload, headers=HEADER)

    return player_response
