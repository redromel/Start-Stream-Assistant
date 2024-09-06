from contextlib import contextmanager
import shutil
import httpx
from dotenv import load_dotenv
import os
from constants import *
from queries import *
from query_parser import *
from writer import bracket_writer, scoreboard_json_writer, scoreboard_writer, swap_players
import time
from nicegui import ui
import requests
import main


@contextmanager
def button_disable(button: ui.button):
    button.disable()
    try:
        yield
    finally:
        button.enable()


@contextmanager
def input_disable(input: ui.input):
    input.disable()
    try:
        yield
    finally:
        input.enable()


@contextmanager
def select_disable(select: ui.select):
    select.disable()
    try:
        yield
    finally:
        select.enable()


async def bracket_listner(switch: ui.switch, select: ui.select):

    print(select.value)
    phase_id = select.value
    bracket_vars = {"phaseId": phase_id, "page": 1, "perPage": 15}
    payload = {"query": BRACKET_GRAPHIC_QUERY, "variables": bracket_vars}

    with select_disable(select):
        try:
            async with httpx.AsyncClient() as client:

                response = await client.post(url=API_URL, json=payload, headers=HEADER)

                while switch.value == True:
                    response = await client.post(
                        url=API_URL, json=payload, headers=HEADER
                    )

                    while isinstance(response, int):
                        response = await client.post(
                            url=API_URL, json=payload, headers=HEADER
                        )
                        time.sleep(3)

                    set_data = bracket_parse(response)
                    bracket_writer(set_data)

                    if is_phase_complete(response) == True:
                        break
                    time.sleep(1)
        finally:
            switch.value = False


def extract_slug(url):

    prefix = 'start.gg/'
    if prefix in url:
        slug = url.split('start.gg/')[-1]
    else:
        slug = url

    suffix = slug.split('/', 2)

    if len(suffix) > 1:

        slug = '/'.join(suffix[:2])
        return slug
    else:
        return slug


async def get_tourney_info(button, tournament_url, event_dropdown, stream_dropdown):

    await get_events(button, tournament_url, event_dropdown)
    await get_streamers(stream_dropdown, tournament_url)


async def get_events(button, input, event_dropdown):
    slug = extract_slug(input.value)
    vars = {"slug": slug}
    payload = {"query": EVENT_QUERY, "variables": vars}

    try:
        with input_disable(input):
            with button_disable(button):
                async with httpx.AsyncClient() as client:
                    response = await client.post(url=API_URL, json=payload, headers=HEADER)
                    events = event_parse(response)
                    event_dropdown.set_options(events, value=list(events)[0])
                    event_dropdown.enable()
                    return
    except:
        ui.notify('Invalid Slug')


async def get_streamers(stream_dropdown, tournament_url):
    slug = extract_slug(tournament_url.value)
    vars = {"tourneySlug":  slug}
    payload = {"query": STREAM_QUERY, "variables": vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        streams = stream_parse(response)

        stream_list = []

        if streams == None:
            stream_list = ["No Streamers"]
            stream_dropdown.set_options(stream_list, value=stream_list[0])
            stream_dropdown.disable()
            print('hello')
            return
        for stream in streams:
            stream_list.append(stream["stream"]["streamName"])
        stream_dropdown.set_options(stream_list, value=stream_list)
        stream_dropdown.enable()


async def get_phases(event_dropdown, phase_dropdown):
    event_id = event_dropdown.value
    vars = {"eventId": event_id}
    payload = {"query": PHASE_QUERY, "variables": vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        phases = phase_parse(response)
        phase_dropdown.set_options(phases, value=list(phases)[0])
        phase_dropdown.enable()
        return

async def get_pools(phase_dropdown, pool_dropdown):
    phase_id = phase_dropdown.value
    vars = {'phaseId': phase_id}
    payload = {'query': POOL_QUERY, 'variables': vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=api_url, json=payload, headers=header)
        phases = pool_parse(response)
        pool_dropdown.set_options(phases, value=list(phases)[0])
        pool_dropdown.enable()
        return


def get_set(set_id):
    set_vars = {"setId": set_id}
    set_payload = {"query": SET_QUERY, "variables": set_vars}

    set_response = requests.post(url=API_URL, json=set_payload, headers=HEADER)
    response_json = set_response.json()
    data = response_json.get("data")
    return data


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
    match_button, round, player_1_input, player_1_score, player_2_input, player_2_score, stream_select
):
    
    if stream_select.value == [] or stream_select.value == 0:
        ui.notify("No Matches Available")
        return

    try:    
        scoreboard = get_scoreboard(stream_select.value)

        write_players_json(scoreboard, player_1_input, player_1_score, player_2_input, player_2_score)
        
        match_button.disable()
        round.disable()
        player_1_input.disable()
        player_2_input.disable()
    except:
        ui.notify("No Matches Available")
        return


async def swap_player_ui(
    round, player_1_input, player_1_score, player_2_input, player_2_score, match_button
):

    if match_button.enabled == False:
        scoreboard = swap_players()
        write_players_json(scoreboard, player_1_input, player_1_score, player_2_input, player_2_score)

        

        return
    else:
        swap_player_files()
        
        player_1_input.value, player_2_input.value = player_2_input.value, player_1_input.value
        player_1_score.value, player_2_score.value = player_2_score.value, player_1_score.value
        
        player_1_score.update()
        player_1_input.update()
        player_2_score.update()
        player_2_input.update()
            
    

async def write_players_json(scoreboard, player_1_input, player_1_score, player_2_input, player_2_score):
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


def swap_files(file1_path, file2_path):
    temp_file_path = file1_path + '.tmp'
    shutil.move(file1_path, temp_file_path)
    shutil.move(file2_path, file1_path)
    shutil.move(temp_file_path, file2_path)
    
    
async def change_text(input, path):
    with open(path, "w") as file:
        file.write(str(input))
    return

def swap_player_files():
    swap_files("match_info/player_1_gamertag.txt", "match_info/player_2_gamertag.txt")
    swap_files("match_info/player_1_score.txt", "match_info/player_2_score.txt")
    swap_files("match_info/player_1_id.txt", "match_info/player_2_id.txt")
    swap_files("match_info/player_1_state.png", "match_info/player_2_state.png")
    swap_files("match_info/player_1_country.png", "match_info/player_2_country.png")