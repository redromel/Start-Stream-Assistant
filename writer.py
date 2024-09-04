import json
import os
from nicegui import ui
import requests
from constants import *
from queries import PLAYER_QUERY
from query_parser import player_parse

def bracket_writer(set_data, setup=False):

  for set_data in set_data:
    
    dir = set_data['identifier']+"_"+set_data['fullRoundText']
    path = "bracket_info/"+dir

    if os.path.exists(path) == False:
     os.mkdir(path)

    playerCount = 1
    for match_data in set_data['slots']:

      if match_data['entrant'] != None:
        player = match_data['entrant']['name']
      else:
        player = ""

      if match_data['standing'] != None:
        score = match_data['standing']['stats']['score']['value']
        if score == -1:
          score = "DQ"
        if score == None:
          score = ""
      else:
        score = ""
      
      player_path = path+"/"+set_data['identifier']+"_player"+str(playerCount)+"_name.txt"
      score_path = path+"/"+set_data['identifier']+"_player"+str(playerCount)+"_score.txt"


      if setup == True:
        player = "Setup"
        score = "N"
      f = open(player_path,"w")
      f.write(player)
      f.close()

      f = open(score_path,"w")
      f.write(str(score))
      f.close()

      playerCount = playerCount + 1

def scoreboard_writer(set_data):
    
    path = "match_info/"
    player_count = 1 


    if is_final_phase(set_data) == False:
      round = set_data['set']['phaseGroup']['phase']['name']
    else:
      round = set_data['set']['fullRoundText']
      
    f = open(path+"/round.txt","w")
    f.write(str(round))
    f.close()


    for player_info in set_data['set']['slots']:

      player_path = path+"/player_"+str(player_count)+"_"
      player = player_info_builder(player_info)

      for info in player:
        f = open(player_path+info+".txt", "w")
        f.write(str(player[info]))
        f.close()

      player_count = player_count + 1

    return

      


def is_final_phase(set_data):
  phase_number = set_data['set']['phaseGroup']['phase']['phaseOrder']
  if phase_number <= TOTAL_PHASES:
    return True
  return False


def player_info_builder(entrant_data):
  print(json.dumps(entrant_data,indent=2))
  player = {}
  if entrant_data['entrant']['participants'][0]['user'] != None:
    player_id = entrant_data['entrant']['participants'][0]['user']['player']['id']
    
    location_gender_info = player_parse(get_player(player_id))


    player['gamertag'] = entrant_data['entrant']['name']
    player['genderPronoun'] = location_gender_info['genderPronoun']
    player['state'] = location_gender_info['location']['state']
    player['country'] = location_gender_info['location']['country']
    player['score'] = entrant_data['standing']['stats']['score']['value']

    if player['score'] == None:
      player['score'] = 0


  # Will only happen if person is not registered for start.gg
  else:
    player['gamertag'] = entrant_data['entrant']['name']
    player['genderPronoun'] = None
    player['state'] = None
    player['country'] = None
    player['score'] = entrant_data['standing']['stats']['score']['value']

    if player['score'] == None:
      player['score'] = 0

  return player



def get_player(player_id):
   player_vars = {'playerId': player_id}
   player_payload = {'query': PLAYER_QUERY, 'variables': player_vars}

   player_response = requests.post(url=API_URL,json=player_payload,headers=HEADER)

   return player_response