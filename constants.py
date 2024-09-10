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


MATCH_JSON_PATH = 'match_info/bracket_data.json'
MATCH_MUTATION_PATH = 'match_info/match_mutation.json'

LOCATION_LIST_PATH = 'utils/location_list.json'

ROUND_PATH = 'match_info/match_round.txt'

FLAG_PATH = "utils/flags"

P1_GAMERTAG_PATH = 'match_info\player_1_info\player_1_gamertag.txt'
P2_GAMERTAG_PATH = 'match_info\player_2_info\player_2_gamertag.txt'

P1_SCORE_PATH = 'match_info\player_1_info\player_1_score.txt'
P2_SCORE_PATH = 'match_info\player_2_info\player_2_score.txt'

P1_ID_PATH = 'match_info/player_1_info/player_1_id.txt'
P2_ID_PATH = 'match_info/player_2_info/player_2_id.txt'

P1_FLAG_PATH = 'match_info/player_1_info/player_1_flag.png'
P2_FLAG_PATH = 'match_info/player_2_info/player_2_flag.png'




