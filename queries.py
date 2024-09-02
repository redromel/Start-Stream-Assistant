EVENT_QUERY = '''
query getEventId($slug: String) {
  event(slug: $slug) {
    id
    name
    phases{
      id
      name
    }
  }
},
'''
BRACKET_QUERY = '''
query ($phaseId: ID!, $page: Int!, $perPage: Int!) {
  phase(id: $phaseId) {

    
    name
    phaseOrder
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