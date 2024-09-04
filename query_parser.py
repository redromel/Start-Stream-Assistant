import json



def bracket_parse(response):

    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        phase = data.get('phase')
        sets = phase.get('sets')
        nodes = sets.get('nodes')
        # print(json.dumps(data,indent=2))
        set_json = json.dumps(nodes)
        set_data = json.loads(set_json)

        return set_data

    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def event_parse(response):
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        event = data.get('tournament')
        events = event.get('events')
        set_json = json.dumps(events)
        set_data = json.loads(set_json)

        bracket_ids = {}

        # !I know its bad practice to do multiple things for a function, but the query has already been called
        tournament_json = json.dumps(event)
        tournament_data = json.loads(tournament_json)
        tournament_id = tournament_data['id']
        

        for name in set_data:
            bracket_ids[name['id']] = name['name']

        return bracket_ids
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def phase_parse(response):
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        event = data.get('event')
        phases = event.get('phases')
        set_json = json.dumps(phases)
        set_data = json.loads(set_json)

        bracket_ids = {}

        for name in set_data:
            bracket_ids[name['id']] = name['name']

        return bracket_ids
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def is_phase_complete(response):

    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        phase = data.get('phase')
        phase_json = json.dumps(phase)
        phase_data = json.loads(phase_json)

        if phase_data['state'] == 'COMPLETED':
            return True
        return False

    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def player_parse(response):
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        player = data.get('player')
        user = player.get('user')
        # print(json.dumps(data,indent=2))
        set_json = json.dumps(user)
        set_data = json.loads(set_json)

        return set_data
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def stream_parse(response):
    if response.status_code == 200:
        response_json = response.json()


        data = response_json.get('data')
        tourney = data.get('tournament')
        stream_queue = tourney.get('streamQueue')
        stream_json = json.dumps(stream_queue)
        stream_data = json.loads(stream_json)

        return stream_data
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code


def get_page_info(response):
    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get('data')
        phase = data.get('phase')
        sets = phase.get('sets')
        page_info = sets.get('pageInfo')
        page_total = page_info.get('total')

        page_json = json.dumps(page_total)
        page_data = json.loads(page_json)
        return page_data
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return response.status_code
