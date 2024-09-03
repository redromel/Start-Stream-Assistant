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
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}


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

        response = await client.post(url=api_url,json=payload,headers=header)

        while switch.value==True:
          response = await client.post(url=api_url,json=payload,headers=header)
          
          while isinstance(response,int):
            response = await client.post(url=api_url,json=payload,headers=header)
            time.sleep(3)
          
          set_data = bracket_parse(response)
          bracket_writer(set_data)

          if is_phase_complete(response) == True:
            break
          time.sleep(1)
    finally:
      switch.value = False

async def get_phases(button, input, dropdown):
    slug = input.value
    vars = {'slug': slug}
    payload = {'query': EVENT_QUERY, 'variables': vars}
    
    try:
        with input_disable(input):
            with button_disable(button):
                async with httpx.AsyncClient() as client:
                    response = await client.post(url=api_url,json=payload,headers=header)
                    phases = phase_parse(response)
                    print(list(phases)[0])
                    TOTAL_PHASES = len(list(phases))
                    dropdown.set_options(phases, value = list(phases)[0])
                    print(TOTAL_PHASES)
                    ui.notify(TOTAL_PHASES)
                    return
    except:
        ui.notify('Invalid Slug')


def get_set(set_id):
    set_vars = {"setId": set_id}
    set_payload = {'query': SET_QUERY, 'variables': set_vars}

    set_response = requests.post(url=api_url,json=set_payload,headers=header)
    response_json = set_response.json()
    data = response_json.get('data')
    return data


def get_scoreboard():

  phase_id = 1749308
  phase_vars = {"phaseId": phase_id, "page": 1, "perPage": 30} 
  phase_payload = {'query': BRACKET_QUERY, 'variables': phase_vars}

  phase_response = requests.post(url=api_url,json=phase_payload,headers=header)
  
  set_data = bracket_parse(phase_response)


  for set in set_data:
    if set['stream'] != None and set['state'] == ONGOING:
      data = get_set(set['id'])
      scoreboard_writer(data)
      return
    
  print('no streamed matches')






