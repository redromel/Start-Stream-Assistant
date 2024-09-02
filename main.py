# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun

from dotenv import load_dotenv
import requests
from event_listner import bracket_listner
from queries import *
from query_parser import *
from writer import *
from nicegui import ui


load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
phase_id = 1749308
slug = 'tournament/py-testing-tourney-2/event/top-8-testing'
vars = {'slug': slug}
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 100}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': EVENT_QUERY, 'variables': vars}


def main():
  

  response = requests.post(url=api_url,json=payload,headers=header)
  phases = phase_parse(response)
  print(phases)


  nameS = ui.select(phases,on_change=lambda e: print(e.value))

  ui.button('hello',on_click=lambda e: ui.notify('WAZZUP'))
  texto = ui.input(label='Phase',placeholder='Phase')
  test_switch = ui.switch('Full Test',on_change=lambda e: bracket_listner(e.sender, texto))
  ui.label('Top 8 Watcher on').bind_visibility_from(test_switch,'value')



if __name__ in {"__main__", "__mp_main__"}:
  main()
  ui.run()