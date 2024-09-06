import json
import os
from nicegui import ui
import requests
from constants import *
from queries import PLAYER_QUERY, SET_QUERY, SET_QUERY
from query_parser import player_parse, stream_parse, stream_parse
import shutil
from PIL import Image


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


def player_info_builder(entrant_data, round, player_count):
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

    # If coming from Losers Bracket Grand Finals
    if round == "Grand Final" and player_count == 2:
        player["gamertag"] = entrant_data["entrant"]["name"] + " [L]"

    return player


def get_player(player_id):
    player_vars = {"playerId": player_id}
    player_payload = {"query": PLAYER_QUERY, "variables": player_vars}

    player_response = requests.post(url=API_URL, json=player_payload, headers=HEADER)

    return player_response


def get_flag(location, destination_path, location_type):

    flag_path = "state_flags_rounded/" + str(location).lower() + ".png"

    if location == None:
        transparent_image = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        transparent_image.save(str(destination_path + ".png"))
        return

    # prioritizes state before country

    if location_type == "state":
        flag_path = "state_flags_rounded/" + str(location).lower() + ".png"
    if location_type == "country":
        code = get_code(location)

        flag_path = "country_flags_rounded/" + str(code).lower() + ".png"

    shutil.copy(flag_path, str(destination_path + ".png"))


def set_flag(input):
    if input == "state":
        ...
    if input == "country":
        ...


def load_custom_flag(path, player_id): ...


def get_code(country):

    with open("countries.json", "r") as file:
        countries_data = json.load(file)

    for countries in countries_data:
        if str(countries["name"]).lower() == str(country).lower():
            return str(countries["code"]).lower()


def player_info_builder(entrant_data, round, player_count):
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

    # If coming from Losers Bracket Grand Finals
    if round == "Grand Final" and player_count == 2:
        player["gamertag"] = entrant_data["entrant"]["name"] + " [L]"

    return player


def get_player(player_id):
    player_vars = {"playerId": player_id}
    player_payload = {"query": PLAYER_QUERY, "variables": player_vars}

    player_response = requests.post(url=API_URL, json=player_payload, headers=HEADER)

    return player_response


def get_flag(location, destination_path, location_type):

    flag_path = "state_flags_rounded/" + str(location).lower() + ".png"

    if location == None:
        transparent_image = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        transparent_image.save(str(destination_path + ".png"))
        return

    # prioritizes state before country

    if location_type == "state":
        flag_path = "state_flags_rounded/" + str(location).lower() + ".png"
    if location_type == "country":
        code = get_code(location)

        flag_path = "country_flags_rounded/" + str(code).lower() + ".png"

    shutil.copy(flag_path, str(destination_path + ".png"))


def set_flag(input):
    if input == "state":
        ...
    if input == "country":
        ...


def load_custom_flag(path, player_id): ...


def get_code(country):

    with open("countries.json", "r") as file:
        countries_data = json.load(file)

    for countries in countries_data:
        if str(countries["name"]).lower() == str(country).lower():
            return str(countries["code"]).lower()


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

    player_count = 1
    for player_info in set_data["set"]["slots"]:
        player = player_info_builder(player_info, round, player_count)
        players.append(player)
        player_count = 1 + player_count

    bracket_data["players"] = players
    bracket_json = json.dumps(bracket_data)

    f = open(path + "/bracket_data.json", "w")
    f.write(bracket_json)
    f.close()

    return bracket_data


def scoreboard_writer(bracket_json):

    path = "match_info/"

    if os.path.exists(path) == False:
        os.mkdir(path)

    for match_data in bracket_json:
        match_path = path + "match_" + str(match_data) + ".txt"

        if not isinstance(bracket_json[match_data], list):
            f = open(match_path, "w")
            f.write(str(bracket_json[match_data]))
            f.close()

        else:

            player_count = 0
            for players in bracket_json[match_data]:
                player_count = player_count + 1
                for player_data in players:
                    player_path = (
                        path + "player_" + str(player_count) + "_" + player_data
                    )

                    if player_data == "state" or player_data == "country":
                        get_flag(players[player_data], player_path, player_data)

                    else:
                        f = open(str(player_path + ".txt"), "w")
                        f.write(str(players[player_data]))
                        f.close()

    return


async def mutation_writer(p1_score, p2_score, player_1, player_2):

    print(player_1)
    print(player_2)

    with open(MATCH_JSON_PATH, "r") as file:
        bracket_json = json.load(file)

    print(bracket_json)
    player = bracket_json["players"]
    setId = bracket_json["id"]
    p1_id = player[0]["id"]
    p2_id = player[1]["id"]

    gameNum = p1_score + p2_score

    # this would happen due to a name swap

    # first game
    if gameNum == 1:
        if p1_score > p2_score:
            winnerId = p1_id
        else:
            winnerId = p2_id
    else:
        with open(MATCH_MUTATION_PATH, "r") as file:
            mutation_json = json.load(file)
        winnerId = win_counter(mutation_json, p1_score, p2_score, p1_id, p2_id)

    if winnerId == p1_id:
        entrant1Score = 1
        entrant2Score = 0
    else:
        entrant1Score = 0
        entrant2Score = 1

    mutation = {}
    mutation["setId"] = setId
    match_data = {}
    mutation["gameData"] = []

    if gameNum == 0:
        match_data["gameNum"] = gameNum
        mutation["gameData"].append(match_data)
        return json.dumps(mutation)

    match_data["winnerId"] = winnerId
    match_data["gameNum"] = gameNum
    match_data["entrant1Score"] = entrant1Score
    match_data["entrant2Score"] = entrant2Score

    # first game, build new json file
    if gameNum == 1:
        mutation["gameData"].append(match_data)
        with open(MATCH_MUTATION_PATH, "w") as file:
            file.write(json.dumps(mutation))

        return json.dumps(mutation)

    else:
        with open(MATCH_MUTATION_PATH, "r") as file:
            mutation_json = json.load(file)

        mutation = check_mutation_conflicts(mutation_json, match_data, gameNum)
        with open(MATCH_MUTATION_PATH, "w") as file:
            file.write(json.dumps(mutation))

        return json.dumps(mutation)


def win_counter(mutation_json, p1_score, p2_score, p1_id, p2_id):

    games = mutation_json["gameData"]

    p1_prev_score = 0
    p2_prev_score = 0
    for game in games:
        if game["winnerId"] == p1_id:
            p1_prev_score = p1_prev_score + 1
        if game["winnerId"] == p2_id:
            p2_prev_score = p2_prev_score + 1

    if p1_score > p1_prev_score:
        return p1_id
    if p2_score > p2_prev_score:
        return p2_id

    return 0


def check_mutation_conflicts(mutation_json, match_data, gameNum):

    ui.notify(gameNum)
    mutation_match_data = mutation_json["gameData"]

    for matches in mutation_match_data:
        #  We always assume that the latest update is the most accurate, so if there is an old gameNum, we replace it with a new one
        if matches["gameNum"] == match_data["gameNum"]:
            matches = match_data

    if len(mutation_match_data) > gameNum:
        to_remove = len(mutation_match_data) - gameNum

        for x in range(to_remove):
            mutation_match_data.pop()

    if len(mutation_match_data) < gameNum:
        mutation_match_data.append(match_data)
    return mutation_json


def is_final_phase(set_data):
    phase_number = set_data["set"]["phaseGroup"]["phase"]["phaseOrder"]
    if phase_number <= TOTAL_PHASES:
        return True
    return False


def get_player_scores(set_data):

    bracket_data = {}
    players = []

    player_count = 1
    for player_info in set_data["set"]["slots"]:
        player = player_info_builder(player_info, round, player_count)
        players.append(player)
        player_count = 1 + player_count

    bracket_data["players"] = players
    bracket_json = json.dumps(bracket_data)
    return bracket_data


def get_set(set_id):
    set_vars = {"setId": set_id}
    set_payload = {"query": SET_QUERY, "variables": set_vars}

    set_response = requests.post(url=API_URL, json=set_payload, headers=HEADER)
    response_json = set_response.json()
    data = response_json.get("data")
    return data
async def mutation_writer(p1_score, p2_score,player_1,player_2):

    print(player_1)
    print(player_2)
    
    
    with open(MATCH_JSON_PATH, "r") as file:
        bracket_json = json.load(file)

    print(bracket_json)
    player = bracket_json['players']
    setId = bracket_json["id"]
    p1_id = player[0]['id']
    p2_id = player[1]['id']
    
    
    gameNum = p1_score + p2_score


    # this would happen due to a name swap

    
    # first game
    if gameNum == 1:
        if p1_score > p2_score:
            winnerId = p1_id
        else:
            winnerId = p2_id
    else:
        with open(MATCH_MUTATION_PATH, "r") as file:
            mutation_json = json.load(file)
        winnerId = win_counter(mutation_json, p1_score, p2_score, p1_id, p2_id)

    if winnerId == p1_id:
        entrant1Score = 1
        entrant2Score = 0
    else:
        entrant1Score = 0
        entrant2Score = 1


    mutation = {}
    mutation["setId"] = setId
    match_data = {}
    mutation["gameData"] = []
    
    if gameNum == 0:
        match_data["gameNum"] = gameNum
        mutation["gameData"].append(match_data)
        return json.dumps(mutation)

    match_data["winnerId"] = winnerId
    match_data["gameNum"] = gameNum
    match_data["entrant1Score"] = entrant1Score
    match_data["entrant2Score"] = entrant2Score





    # first game, build new json file
    if gameNum == 1:
        mutation["gameData"].append(match_data)
        with open(MATCH_MUTATION_PATH, "w") as file:
            file.write(json.dumps(mutation))
            
        return json.dumps(mutation)

    else:
        with open(MATCH_MUTATION_PATH, "r") as file:
            mutation_json = json.load(file)

        mutation = check_mutation_conflicts(mutation_json, match_data, gameNum)
        with open(MATCH_MUTATION_PATH, "w") as file:
            file.write(json.dumps(mutation))
        
        return json.dumps(mutation)
    
def win_counter(mutation_json, p1_score, p2_score, p1_id, p2_id):
    
    games = mutation_json['gameData']
    
    p1_prev_score = 0
    p2_prev_score = 0
    for game in games:
        if game['winnerId'] == p1_id:
            p1_prev_score = p1_prev_score + 1
        if game['winnerId'] == p2_id:
            p2_prev_score = p2_prev_score + 1
    
    if p1_score > p1_prev_score:
        return p1_id
    if p2_score > p2_prev_score:
        return p2_id
    
    return 0        


def check_mutation_conflicts(mutation_json, match_data, gameNum):

    ui.notify(gameNum)
    mutation_match_data = mutation_json["gameData"]

    for matches in mutation_match_data:
        #  We always assume that the latest update is the most accurate, so if there is an old gameNum, we replace it with a new one
        if matches["gameNum"] == match_data["gameNum"]:
            matches = match_data

    if len(mutation_match_data) > gameNum:
        to_remove = len(mutation_match_data) - gameNum   
        
        for x in range (to_remove):
            mutation_match_data.pop()
        
    if len(mutation_match_data) < gameNum:
        mutation_match_data.append(match_data)
    return mutation_json


def is_final_phase(set_data):
    phase_number = set_data["set"]["phaseGroup"]["phase"]["phaseOrder"]
    if phase_number <= TOTAL_PHASES:
        return True
    return False


def get_player_scores(set_data):

    bracket_data = {}
    players = []

    player_count = 1
    for player_info in set_data["set"]["slots"]:
        player = player_info_builder(player_info, round, player_count)
        players.append(player)
        player_count = 1 + player_count

    bracket_data["players"] = players
    bracket_json = json.dumps(bracket_data)
    return bracket_data



def get_set(set_id):
    set_vars = {"setId": set_id}
    set_payload = {"query": SET_QUERY, "variables": set_vars}

    set_response = requests.post(url=API_URL, json=set_payload, headers=HEADER)
    response_json = set_response.json()
    data = response_json.get("data")
    return data