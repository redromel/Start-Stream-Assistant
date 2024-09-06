import json
import os
from nicegui import ui
import requests
from constants import *
from event_listner import get_set
from queries import *
from query_parser import player_parse, stream_parse
import shutil
from PIL import Image

from writer import *

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

def get_scoreboard(stream_name):

    tourney_slug = "tournament/py-testing-tourney-2"
    stream_vars = {"tourneySlug": tourney_slug}
    stream_payload = {"query": STREAM_QUERY, "variables": stream_vars}

    stream_response = requests.post(url=API_URL, json=stream_payload, headers=HEADER)

    stream_data = stream_parse(stream_response)
    for stream in stream_data:
        if stream["stream"]["streamName"] == stream_name:
            for set in stream["sets"]:
                if set["state"] == ONGOING:
                    scoreboard = scoreboard_json_writer(get_set(set["id"]))
                    scoreboard_writer(scoreboard)
                    return scoreboard
    print("no streamed matches")

async def get_scoreboard_data(
    match_button,
    round,
    player_1_input,
    player_1_score,
    player_2_input,
    player_2_score,
    stream_select,
):

    if stream_select.value == [] or stream_select.value == 0:
        ui.notify("No Matches Available")
        return

    try:
        scoreboard = get_scoreboard(stream_select.value)

        write_players_json(
            scoreboard, player_1_input, player_1_score, player_2_input, player_2_score
        )

        match_button.disable()
        round.disable()
        player_1_input.disable()
        player_2_input.disable()
    except:
        ui.notify("No Matches Available")
        return


async def swap_player_ui(
    player_1_input, player_1_score, player_2_input, player_2_score, match_button
):

    if match_button.enabled == False:
        scoreboard = swap_players()
        write_players_json(
            scoreboard, player_1_input, player_1_score, player_2_input, player_2_score
        )

        return
    else:
        swap_player_files()

        player_1_input.value, player_2_input.value = (
            player_2_input.value,
            player_1_input.value,
        )
        player_1_score.value, player_2_score.value = (
            player_2_score.value,
            player_1_score.value,
        )

        player_1_score.update()
        player_1_input.update()
        player_2_score.update()
        player_2_input.update()


async def write_players_json(
    scoreboard, player_1_input, player_1_score, player_2_input, player_2_score
):
    player_1 = scoreboard["players"][0]
    player_2 = scoreboard["players"][1]
    round.value = scoreboard["round"]
    player_1_input.value = player_1["gamertag"]
    player_1_score.value = player_1["score"]
    player_2_input.value = player_2["gamertag"]
    player_2_score.value = player_2["score"]

    round.update()
    player_1_input.update()
    player_1_score.update()
    player_2_input.update()
    player_2_score.update()

async def change_text(input, path):
    with open(path, "w") as file:
        file.write(str(input))
    return

def swap_files(file1_path, file2_path):
    temp_file_path = file1_path + ".tmp"
    shutil.move(file1_path, temp_file_path)
    shutil.move(file2_path, file1_path)
    shutil.move(temp_file_path, file2_path)

def swap_player_files():
    swap_files("match_info/player_1_gamertag.txt", "match_info/player_2_gamertag.txt")
    swap_files("match_info/player_1_score.txt", "match_info/player_2_score.txt")
    swap_files("match_info/player_1_id.txt", "match_info/player_2_id.txt")
    swap_files("match_info/player_1_state.png", "match_info/player_2_state.png")
    swap_files("match_info/player_1_country.png", "match_info/player_2_country.png")