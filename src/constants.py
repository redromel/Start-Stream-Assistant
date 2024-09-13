import os
import sys
from dotenv import load_dotenv


TOTAL_PHASES = 2
NOT_STARTED = 1
ONGOING = 2
COMPLETED = 3


load_dotenv()
KEY = os.getenv('smashgg_api')
CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')


API_URL = 'https://api.start.gg/gql/alpha'
HEADER = {"Authorization": "Bearer " + KEY, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}





if hasattr(sys, '_MEIPASS'):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

MATCH_JSON_PATH = os.path.join(base_dir,'utils','bracket_data.json')
MATCH_MUTATION_PATH = os.path.join(base_dir,'utils','match_mutation.json')
LOCATION_LIST_PATH = os.path.join(base_dir,'utils','location_list.json')
FLAG_PATH = os.path.join(base_dir,'utils','flags')





ROUND_PATH = os.path.join('src','match_info','match_round.txt')


P1_GAMERTAG_PATH = os.path.join('src','match_info','player_1_info','player_1_gamertag.txt')
P2_GAMERTAG_PATH = os.path.join('src','match_info','player_2_info','player_2_gamertag.txt')

P1_SCORE_PATH = os.path.join('src','match_info','player_1_info','player_1_score.txt')
P2_SCORE_PATH = os.path.join('src','match_info','player_2_info','player_2_score.txt')

P1_ID_PATH = os.path.join('src','match_info','player_1_info','player_1_id.txt')
P2_ID_PATH = os.path.join('src','match_info','player_2_info','player_2_id.txt')

P1_FLAG_PATH = os.path.join('src','match_info','player_1_info','player_1_flag.png')
P2_FLAG_PATH = os.path.join('src','match_info','player_2_info','player_2_flag.png')




