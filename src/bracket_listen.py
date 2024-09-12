import os
import shutil
import time
import httpx
from nicegui import ui

from constants import API_URL, HEADER
from event_listner import select_disable
from queries import BRACKET_GRAPHIC_QUERY, PHASE_QUERY, POOL_QUERY
from query_parser import bracket_parse, is_phase_complete, phase_parse, pool_parse
from writer import bracket_writer

class Bracket_Listen():
    def __init__(self):
        
        with ui.grid(columns=4):
            self.event_select = ui.select(
                label="Select Event",
                options=["Insert Slug"],
                on_change=lambda e: get_phases(e, self.phase_select),
                value=None,
            ).classes("col-span-1 w-full")
            
            self.phase_select = ui.select(
                label="Select Phase",
                options=["Insert Slug"],
                on_change=lambda e: get_pools(e, self.pool_select),
                value=None,
            ).classes("col-span-1 w-full")
            
            self.pool_select = ui.select(
                label="Select Pool",
                options=["Insert Slug"],
                on_change=lambda e: print(e.value),
                value=None,
            ).classes("col-span-1 w-full")
            
            self.bracket_switch = ui.switch(
                "Get Bracket",
                on_change=lambda e: bracket_listner(
                    e.sender, self.pool_select
                ),
            ).classes("col-span-1 w-full").props("size=xl")
        
        
        self.event_select.disable()
        self.phase_select.disable()
        self.pool_select.disable()
            


async def get_phases(event_dropdown: ui.select, phase_dropdown: ui.select):
    event_id = event_dropdown.value
    vars = {"eventId": event_id}
    payload = {"query": PHASE_QUERY, "variables": vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        phases = phase_parse(response)
        phase_dropdown.set_options(phases, value=list(phases)[len(list(phases))-1])
        phase_dropdown.enable()
        return
    

async def get_pools(phase_dropdown: ui.select, pool_dropdown: ui.select):
    phase_id = phase_dropdown.value
    vars = {"phaseId": phase_id}
    payload = {"query": POOL_QUERY, "variables": vars}

    async with httpx.AsyncClient() as client:
        response = await client.post(url=API_URL, json=payload, headers=HEADER)
        phases = pool_parse(response)
        pool_dropdown.set_options(phases, value=list(phases)[len(list(phases))-1])
        pool_dropdown.enable()
        return


async def bracket_listner(switch: ui.switch, select: ui.select):

    phase_id = select.value
    bracket_vars = {"phaseId": phase_id, "page": 1, "perPage": 15}
    payload = {"query": BRACKET_GRAPHIC_QUERY, "variables": bracket_vars}

    # Clear Contents of the Bracket before listening
    bracket_path = os.path.join("src","bracket_info")
    if os.path.exists(bracket_path) and switch.value == True and phase_id != None:
        print("hello")
        for item in os.listdir(bracket_path):
            item_path = os.path.join(bracket_path, item)
            if os.path.isfile(item_path):
                os.remo(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
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
                        time.sleep(0.25)

                    set_data = bracket_parse(response)
                    bracket_writer(set_data)

                    if is_phase_complete(response) == True:
                        break

                    time.sleep(0.25)
        finally:
            time.sleep(0.25)
            switch.value = False