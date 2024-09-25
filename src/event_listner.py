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
        ui.notify("No API key detected in .env file",type="info")
        return
    await get_tourney_name(tournament_url, footer)
    await get_events(button, tournament_url, event_dropdown)
    await get_streamers(stream_dropdown, tournament_url)


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


async def get_streamers(stream_dropdown:ui.select, tournament_url:ui.input):
    slug = extract_slug(tournament_url.value)
    vars = {"tourneySlug": slug}
    payload = {"query": STREAM_QUERY, "variables": vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        streams = stream_parse(response)

        stream_list = []

        if streams == None:
            stream_list = ["No Streamers"]
            stream_dropdown.set_options(stream_list, value=stream_list[0])
            stream_dropdown.disable()
            return
        for stream in streams:
            stream_list.append(stream["stream"]["streamName"])
        stream_dropdown.set_options(stream_list, value=stream_list[0])
        stream_dropdown.enable()

async def send_mutation(mutation_vars):

    # don't send a mutation if they just swapped
    if mutation_vars == 0:
        return
    mutation_payload = {"query": SCOREBOARD_MUTATION, "variables": mutation_vars}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=mutation_payload, headers=HEADER)
