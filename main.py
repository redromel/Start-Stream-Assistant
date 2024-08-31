
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'

slugs = "tournament/genesis-9-1/event/ultimate-singles"
phase_id = 1749308
vars = {"slug": slugs}
vars2 = {"phaseId": phase_id, "page": 1, "perPage": 11}
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}



query = '''
query getEventId($slug: String) {
  event(slug: $slug) {
    id
    name
    phases{
        id
        name
    }
    videogame{
        stages{
            name
        }
    }
  }
},

'''

query2 = '''
query PhaseSets($phaseId: ID!, $page: Int!, $perPage: Int!) {
  phase(id: $phaseId) {

    name
    id
    phaseOrder
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ){
      pageInfo {
        total
      }
      nodes {
        fullRoundText
        identifier
        id
        
        slots {
          id
          entrant {
            id
            name
          }
          standing{
            placement
            stats{
             score{
             #... This grabs the set score for players
              value
             }
            }
          }
        }
      }
    }
  }
},

'''

payload = {'query': query2, 'variables': vars2}

response = requests.post(url=api_url,json=payload,headers=header)

if response.status_code == 200:
    # Print the JSON response
    response_json = response.json()
    data = response_json.get('data')
    print(json.dumps(data, indent=2))
    # event = data.get("event")
    # print(json.dumps(event, indent=2))
    # dict_test = {
    #     "ID": event.get('id'),
    #     "Name": event.get('name')
    # }
    # print(dict_test['ID'])
else:
    print(f"Query failed with status code {response.status_code}")
    print(response.text)