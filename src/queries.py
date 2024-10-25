EVENT_QUERY = '''
query getEventId($slug: String) {
  tournament(slug: $slug){
    name
    id 
    events{
      id
      name
      phases{
        id
        name
        phaseGroups{
          nodes{
            id
            displayIdentifier
          }
        }
      } 
    }
  }
},
'''

PHASE_QUERY = '''
query($eventId: ID){
  event(id: $eventId){
    phases{
      name
      id
    }
  }
},
'''

POOL_QUERY = '''
query($phaseId: ID){
  phase(id: $phaseId){
    phaseGroups{
      nodes{
        id
        displayIdentifier
      }
    }
  }
},
'''

PLAYER_QUERY = '''

query($playerId: ID!){
  player(id: $playerId){
    gamerTag
    user{
      name
      genderPronoun
      location{
        city
        state
        country
      }
    }
    
  }

}
'''
BRACKET_GRAPHIC_QUERY = '''
query ($phaseId: ID!, $page: Int!, $perPage: Int!) {
  phaseGroup(id: $phaseId) {
    state
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ){
      pageInfo {
        total
      }
      nodes {
        event{
          videogame
          {
            name
          }
        }
        fullRoundText
        identifier  
        slots {
          entrant {
            name
          }
          standing{
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

BRACKET_QUERY = '''
query ($phaseId: ID!, $page: Int!, $perPage: Int!) {
  phase(id: $phaseId) {
    name
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
        id
        #... 1 = Not Started, 2 = Ongoing, 3 = Completed
        state
        stream{
          streamName
        }  
        slots {
          standing{
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

SET_QUERY = '''
query ($setId: ID!) {
  set(id: $setId){
    id
    event{
      phases{
        id
      }
    }
    phaseGroup{
      phase{
        name
        phaseOrder
      }
    }
    fullRoundText
    slots{
      entrant{
        name
        id
        participants{
          user{
            player{
              id
            }
          }
        }
      }
      standing{
        stats{
          score{
            value
          }
        }
      }
    }
  }
},

'''

STREAM_QUERY = '''
query($tourneySlug: String){

  tournament(slug: $tourneySlug){
    streamQueue{
      id
      stream{
        streamName
      }
      sets{
        id
        state
      }
    }
  }
},

'''

SCOREBOARD_MUTATION = '''
mutation ($setId: ID!, $winnerId: ID, $gameData: [BracketSetGameDataInput]){
  
  reportBracketSet(setId: $setId, winnerId: $winnerId, gameData: $gameData){
    id
    state
  }
},

'''
