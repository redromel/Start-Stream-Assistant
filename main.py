# TODO:  Start putting things in other files
# TODO:  Loser Identifier for Grands
# TODO:  Find a Termination condition for top 8
# TODO:  Better Error Handling when querying
import requests
from dotenv import load_dotenv
import os
from queries import *
from query_parser import *
import time

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'

slugs = "tournament/genesis-9-1/event/ultimate-singles"
phase_id = 1749308
vars = {"slug": slugs}
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 100}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
payload = {'query': BRACKET_QUERY, 'variables': vars2}



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






        



def main():
  
  
  try:
    while True:
      response = requests.post(url=api_url,json=payload,headers=header)
      
      while isinstance(response,int):
        response = requests.post(url=api_url,json=payload,headers=header)
        time.sleep(3)
      
      set_data = bracket_parse(response)
      
      bracket_writer(set_data)
      time.sleep(1)
  except:
    print(set_data)
  
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






if __name__ == "__main__":
  main()