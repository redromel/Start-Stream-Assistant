import os
from dotenv import load_dotenv


TOTAL_PHASES = 2
NOT_STARTED = 1
ONGOING = 2
COMPLETED = 3


load_dotenv()
KEY = os.getenv('smashgg_api')

API_URL = 'https://api.start.gg/gql/alpha'
HEADER = {"Authorization": "Bearer " + KEY, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}