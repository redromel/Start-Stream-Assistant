# TODO:  Loser Identifier for Grands
# TODO:  Better Error Handling when querying
# TODO:  NiceGUI Implementation for fun
# TODO:  Find Stream implementation, pagination implementation

from dotenv import load_dotenv
import requests
from event_listner import *
from queries import *
from query_parser import *
from writer import *
from nicegui import ui
import event_listner


load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
# phase_id = 1749308
phase_id = 1188397
slug = 'tournament/genesis-9-1/event/melee-singles'
vars = {'slug': slug}
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 50}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': EVENT_QUERY, 'variables': vars}


def main():
  


  response = requests.post(url=api_url,json=payload,headers=header)
  phases = phase_parse(response)
  print(phases)


  # response_json = response.json()
  # data = response_json.get('data')
  # phase = data.get('phase')
  # sets = phase.get('sets')
  # nodes = sets.get('nodes')
  # print(nodes)
  
  
  slug_input = ui.input(label='start.gg event slug',placeholder='tournament/tournament-name/event/event-name').props('size=80').props('rounded outlined dense')

  ui.label().bind_text_from(slug_input, 'value')


  slug_button = ui.button('Submit', on_click=lambda e: get_phases(e.sender, slug_input, nameS))
  
  add_text = ui.button('Add Text', on_click=lambda: slug_input.set_value('hello world'))
  
  
  nameS = ui.select(options=['Insert Slug'],on_change=lambda e: print(e.value),value='Insert Slug')


  ui.button('hello',on_click=lambda e: ui.notify('WAZZUP'))
  texto = ui.input(label='Phase',placeholder='Phase')
  test_switch = ui.switch('Full Test',on_change=lambda e: bracket_listner(e.sender, nameS))
  ui.label('Top 8 Watcher on').bind_visibility_from(test_switch,'value')



if __name__ in {"__main__", "__mp_main__"}:
  main()
  ui.run()