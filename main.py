import pysmashgg
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'

slugs = "tournament/genesis-9-1/event/ultimate-singles"
vars = {"slug": slugs}
header = {"Authorization": "Bearer " + key}



query = '''
query getEventId($slug: String) {
  event(slug: $slug) {
    id
    name
    phaseGroups{
        phaseGroup
    }
  }
},

'''
payload = {'query': query, 'variables': vars}

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