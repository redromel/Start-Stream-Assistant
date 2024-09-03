import os
from dotenv import load_dotenv


TOTAL_PHASES = 2
NOT_STARTED = 1
ONGOING = 2
COMPLETED = 3

load_dotenv()
key = os.getenv('smashgg_api')

api_url = 'https://api.start.gg/gql/alpha'
header = {"Authorization": "Bearer " + key, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}