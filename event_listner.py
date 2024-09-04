from contextlib import contextmanager
import httpx
from dotenv import load_dotenv
import os
from constants import ONGOING
from queries import *
from query_parser import *
from writer import bracket_writer, scoreboard_writer
import time
from nicegui import ui
import requests
import main

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
header = {"Authorization": "Bearer " + key,
          'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}

tournament_id = 0


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
    payload = {'query': BRACKET_GRAPHIC_QUERY, 'variables': bracket_vars}

    with select_disable(select):
        try:
            async with httpx.AsyncClient() as client:

                response = await client.post(url=api_url, json=payload, headers=header)

                while switch.value == True:
                    response = await client.post(url=api_url, json=payload, headers=header)

                    while isinstance(response, int):
                        response = await client.post(url=api_url, json=payload, headers=header)
                        time.sleep(3)

                    set_data = bracket_parse(response)
                    bracket_writer(set_data)

                    if is_phase_complete(response) == True:
                        break
                    time.sleep(1)
        finally:
            switch.value = False


async def get_tourney_info(button, tourney_name, event_dropdown, stream_dropdown):

    await get_events(button, tourney_name, event_dropdown)
    await get_streamers(stream_dropdown, tourney_name)


async def get_events(button, input, dropdown):
    slug = input.value
    vars = {'slug': slug}
    payload = {'query': EVENT_QUERY, 'variables': vars}

    # try:
    with input_disable(input):
        with button_disable(button):
            async with httpx.AsyncClient() as client:
                response = await client.post(url=api_url, json=payload, headers=header)
                events = event_parse(response)

                print(tournament_id)
                dropdown.set_options(events, value=list(events))
                dropdown.enable()
                return
    # except:
    #     ui.notify('Invalid Slug')


async def get_streamers(stream_dropdown, tournament_slug):
    vars = {'tourneySlug':  tournament_slug.value}
    payload = {'query': STREAM_QUERY, 'variables': vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=api_url, json=payload, headers=header)
        streams = stream_parse(response)

        stream_list = []

        if streams == None:
            stream_list = ['No Streamers']
            stream_dropdown.set_options(stream_list, value=stream_list[0])
            stream_dropdown.disable()

            return
        for stream in streams:
            stream_list.append(stream['stream']['streamName'])
        stream_dropdown.set_options(stream_list, value=stream_list[0])
        stream_dropdown.enable()


async def get_phases(event_dropdown, phase_dropdown):
    event_id = event_dropdown.value
    vars = {'eventId': event_id}
    payload = {'query': PHASE_QUERY, 'variables': vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=api_url, json=payload, headers=header)
        phases = phase_parse(response)

        phase_dropdown.set_options(phases, value=list(phases)[0])
        phase_dropdown.enable()
        return


def get_set(set_id):
    set_vars = {"setId": set_id}
    set_payload = {'query': SET_QUERY, 'variables': set_vars}

    set_response = requests.post(url=api_url, json=set_payload, headers=header)
    response_json = set_response.json()
    data = response_json.get('data')
    return data


def get_scoreboard(stream_name):

    if tournament_id == 0:
        print("tournament not set")
        return

    tourney_id = 704088
    stream_vars = {'tournamentId':  tourney_id}
    stream_payload = {'query': STREAM_QUERY, 'variables': stream_vars}

    stream_response = requests.post(
        url=api_url, json=stream_payload, headers=header)

    stream_data = stream_parse(stream_response)
    for stream in stream_data:
        if stream['stream']['streamName'] == stream_name:
            for set in stream['sets']:
                if set['state'] == ONGOING:
                    print(set['id'])
                    scoreboard_writer(get_set(set['id']))
                    return
    print('no streamed matches')
