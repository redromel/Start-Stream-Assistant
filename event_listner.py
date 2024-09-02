from contextlib import contextmanager
import httpx
from dotenv import load_dotenv
import os
from queries import *
from query_parser import *
from writer import *
import time
from nicegui import ui
import main

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
phase_id = 1749308
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



async def bracket_listner(switch: ui.switch, input: ui.input):

  phase_id = input.value
  bracket_vars = {"phaseId": phase_id, "page": 1, "perPage": 100}
  payload = {'query': BRACKET_QUERY, 'variables': bracket_vars}
  

  with input_disable(input):
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
                    dropdown.set_options(phases, value = list(phases)[0])
                    return
    except:
        ui.notify('Invalid Slug')
