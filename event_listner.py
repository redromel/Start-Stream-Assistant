from contextlib import contextmanager
import httpx
from dotenv import load_dotenv
import os
from queries import *
from query_parser import *
from writer import *
import time
from nicegui import ui

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
phase_id = 1749308
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 100}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': BRACKET_QUERY, 'variables': vars2}

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
  vars2 = {"phaseId": phase_id, "page": 1, "perPage": 100}
  header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
  payload = {'query': BRACKET_QUERY, 'variables': vars2}
  

  with input_disable(input):
    # response = requests.post(url=api_url,json=payload,headers=header)
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

