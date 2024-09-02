# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
from contextlib import contextmanager
import httpx
import requests
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

slugs = "tournament/genesis-9-1/event/ultimate-singles"
# phase_id = 1668044
phase_id = 1749308
vars = {"slug": slugs}
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 100}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': BRACKET_QUERY, 'variables': vars2}


@contextmanager
def disabe(button: ui.button):
  button.disable()
  try:
    yield
  finally:
    button.enable()

async def test_funct(button: ui.button):


  with disabe(button):
    # response = requests.post(url=api_url,json=payload,headers=header)
    async with httpx.AsyncClient() as client:

      response = await client.post(url=api_url,json=payload,headers=header)

      while is_phase_complete(response) == False:
        response = await client.post(url=api_url,json=payload,headers=header)
        
        while isinstance(response,int):
          response = await client.post(url=api_url,json=payload,headers=header)
          time.sleep(3)
        
        set_data = bracket_parse(response)
        
        bracket_writer(set_data)
        time.sleep(1)
    
    ui.notify("COMPLETE TASK")


def main():
  
  stringo = 'heheho'
  button = ui.button('test', on_click=lambda e: test_funct(e.sender))
  button = ui.button('Click me!', on_click=lambda e: ui.notify('hi'))

  
  # response = requests.post(url=api_url,json=payload,headers=header)
  # try:
  #   while is_phase_complete(response) == False:
  #     response = requests.post(url=api_url,json=payload,headers=header)
      
  #     while isinstance(response,int):
  #       response = requests.post(url=api_url,json=payload,headers=header)
  #       time.sleep(3)
      
  #     set_data = bracket_parse(response)
      
  #     bracket_writer(set_data)
  #     time.sleep(1)
  # except:
  #   print(set_data)
  
  # print("completed")
  
  # print(set_data)
  # print(set_data[0]['identifier'])

  # for set_data in set_data:

  #   print(set_data)

      




  # if response.status_code == 200:
  #   # Print the JSON response
  #   response_json = response.json()
  #   data = response_json.get('data')
  #   print(json.dumps(data, indent=2))
  #   # event = data.get("event")
  #   # print(json.dumps(event, indent=2))
  #   # dict_test = {
  #   #     "ID": event.get('id'),
  #   #     "Name": event.get('name')
  #   # }
  #   # print(dict_test['ID'])
  # else:
  #   print(f"Query failed with status code {response.status_code}")
  #   print(response.text)






if __name__ in {"__main__", "__mp_main__"}:
  main()
  ui.run()