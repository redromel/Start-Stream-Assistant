EVENT_QUERY = '''
query getEventId($slug: String) {
  tournament(slug: $slug){
    name
    id
    streamQueue{
      id
      stream{
        streamName
        streamLogo
      }
      sets{
        id
      }
    }  
    events{
      id
      name
      videogame{
        displayName
      }
      phases{
        id
        name
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
  phase(id: $phaseId) {
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
query($tournamentId: ID!){

  streamQueue(tournamentId: $tournamentId, includePlayerStreams: true){
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


'''
