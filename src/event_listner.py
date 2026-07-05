from contextlib import contextmanager

import httpx
from dotenv import load_dotenv

from constants import *
from queries import *
from query_parser import *

from nicegui import ui



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


def extract_slug(url: str):

    prefix = "start.gg/"
    if prefix in url:
        slug = url.split("start.gg/")[-1]
    else:
        slug = url

    suffix = slug.split("/", 2)

    if len(suffix) > 1:

        slug = "/".join(suffix[:2])
        return slug
    else:
        return slug


async def get_tourney_info(
    button: ui.button, tournament_url: ui.input, event_dropdown: ui.select, stream_dropdown: ui.select, footer: ui.label
):

    if KEY == '' or KEY == None or KEY == 'YOUR_API_KEY_HERE':
        ui.notify("No API key detected in .env file", type="info")
        return
    await get_tourney_name(tournament_url, footer)
    await get_events(button, tournament_url, event_dropdown)


async def get_tourney_name(tournament_url: ui.input, footer: ui.label):
    slug = extract_slug(tournament_url.value)
    vars = {"slug": slug}
    payload = {"query": EVENT_QUERY, "variables": vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        tourney = tourney_parse(response)
        tourney_name = tourney["name"]
        footer.set_text(f"Tournament:  {tourney_name}")


async def get_events(button: ui.button, tournament_url: ui.input, event_dropdown: ui.select):
    slug = extract_slug(tournament_url.value)
    vars = {"slug": slug}
    payload = {"query": EVENT_QUERY, "variables": vars}

    try:
        with input_disable(tournament_url):
            with button_disable(button):
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url=API_URL, json=payload, headers=HEADER
                    )
                    events = event_parse(response)
                    event_dropdown.set_options(events, value=list(events)[0])
                    event_dropdown.enable()
                    return
    except:
        ui.notify("Invalid Slug", type="warning")


async def get_matches(stream_dropdown: ui.select, tournament_url, pool_id):
    print(pool_id)
    slug = extract_slug(tournament_url.value)
    stream_dropdown.disable()
    stream_list = await update_matches_stream(slug)
    pool_list = await update_matches_pool(pool_id)
    match_list = stream_list | pool_list
    
    if not match_list:
        match_list = ["No Matches Available"]
        stream_dropdown.set_options(match_list, value=stream_list[0])
        stream_dropdown.disable()
        return
    stream_dropdown.set_options(match_list)
    stream_dropdown.enable()

async def update_matches_stream(slug):
    vars = {"tourneySlug": slug}
    payload = {"query": STREAM_QUERY, "variables": vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        streams = stream_parse(response)

        stream_list = {}

        if streams == None:
            return stream_list
        for stream in streams:
            sets = stream["sets"]
            for set in sets:
                try:
                    player_1 = (set["slots"][0]["entrant"]["name"])
                    player_2 = (set["slots"][1]["entrant"]["name"])
                    event = (set["event"]["name"])

                    stream_list[set["id"]
                                ] = f"{event}『 {player_1} VS {player_2} 』/{stream['stream']['streamName']}"
                except:
                    pass

        # stream_dropdown.set_options(stream_list)
        return stream_list

async def update_matches_pool(pool_id):
    
    match_list = {}
    current_page = 1
    total_pages = 1
    while current_page <= total_pages:
        vars = {"phaseGroupId": pool_id, "page": current_page, "perPage": 50}
        payload = {"query": POOL_MATCH_QUERY, "variables": vars}
        async with httpx.AsyncClient() as client:
            response = await client.post(url=API_URL, json=payload, headers=HEADER)
        
        if current_page == 1:
            total_pages = page_parse(response)
        sets = pool_matches_parse(response)
        for set in sets:
            if set['stream'] == None and set['state'] != COMPLETED:
                try:
                    player_1 = (set["slots"][0]["entrant"]["name"])
                    player_2 = (set["slots"][1]["entrant"]["name"])
                    event = (set["event"]["name"])
                    match_list[set["id"]] = f"{event}『{player_1} VS {player_2}』"
                except:
                    pass
            
            
        current_page = current_page + 1
    return match_list

         
        


async def send_mutation(mutation_vars):

    # don't send a mutation if they just swapped
    if mutation_vars == 0:
        return
    mutation_payload = {"query": SCOREBOARD_MUTATION,
                        "variables": mutation_vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=mutation_payload, headers=HEADER)


async def start_select_match(set_id):
    match_vars = {"setId": set_id}
    mutation_payload = {"query": START_MATCH,
                        "variables": match_vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=mutation_payload, headers=HEADER)
        return response.json()
