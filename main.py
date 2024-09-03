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
phase_id = 1749308
# phase_id = 1276356 
player_id = 16105
slug = 'tournament/genesis-9-1/event/melee-singles'
vars = {'slug': slug}

#keep iterating through pages until pageInfo = 0 and nodes = []
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 30}
vars3 = {'playerId': player_id}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': PLAYER_QUERY, 'variables': vars3}
payload2 = {'query': BRACKET_GRAPHIC_QUERY, 'variables': vars2}
payload3 = {'query': BRACKET_QUERY, 'variables': vars2}


def get_scoreboard():

  phase_id = 1749308
  phase_vars = {"phaseId": phase_id, "page": 1, "perPage": 30} 
  phase_payload = {'query': BRACKET_QUERY, 'variables': phase_vars}

  phase_response = requests.post(url=api_url,json=phase_payload,headers=header)
  
  set_data = bracket_parse(phase_response)

  # print(json.dumps(set_data,indent=2))
  # print(set_data[0])

  for set in set_data:
    if set['stream'] != None and set['state'] == 2:
      data = get_set(set['id'])
      print(json.dumps(data,indent=2))
      scoreboard_writer(data)

      
    # else:
    #    print('no streamed matches')


        

def main():
  

  # get_scoreboard()
  # response = requests.post(url=api_url,json=payload3,headers=header)
  # data = bracket_parse(response)
  # print(data)
  # bracket_writer(data)
  # response_json = response.json()
  # print(json.dumps(response_json,indent=2))
  # data = response_json.get('data')
  # phase = data.get('phase')
  # sets = phase.get('sets')
  # nodes = sets.get('nodes')
  # print(json.dumps(data,indent=2))
  
  # phases = phase_parse(response)
  # print(phases)




  # response_json = response.json()
  # data = response_json.get('data')
  # phase = data.get('phase')
  # sets = phase.get('sets')
  # nodes = sets.get('nodes')
  # print(nodes)
  
  
  # slug_input = ui.input(label='start.gg event slug',placeholder='tournament/tournament-name/event/event-name').props('size=80').props('rounded outlined dense')

  # ui.label().bind_text_from(slug_input, 'value')


  # slug_button = ui.button('Submit', on_click=lambda e: get_phases(e.sender, slug_input, nameS))
  
  # add_text = ui.button('Add Text', on_click=lambda: slug_input.set_value('hello world'))
  
  
  # nameS = ui.select(options=['Insert Slug'],on_change=lambda e: print(e.value),value='Insert Slug')


  # ui.button('hello',on_click=lambda e: ui.notify('WAZZUP'))
  # texto = ui.input(label='Phase',placeholder='Phase')
  # test_switch = ui.switch('Full Test',on_change=lambda e: bracket_listner(e.sender, nameS))
  # ui.label('Top 8 Watcher on').bind_visibility_from(test_switch,'value')



if __name__ in {"__main__", "__mp_main__"}:
  main()
  # ui.run()