import os

def bracket_writer(set_data, setup=False):

  for set_data in set_data:
    
    dir = set_data['identifier']+"_"+set_data['fullRoundText']
    path = "bracket_info/"+dir

    if os.path.exists(path) == False:
     os.mkdir(path)

    playerCount = 1
    for match_data in set_data['slots']:

      if match_data['entrant'] != None:
        player = match_data['entrant']['name']
      else:
        player = ""

      if match_data['standing'] != None:
        score = match_data['standing']['stats']['score']['value']
        if score == -1:
          score = "DQ"
        if score == None:
          score = ""
      else:
        score = ""
      
      player_path = path+"/"+set_data['identifier']+"_player"+str(playerCount)+"_name.txt"
      score_path = path+"/"+set_data['identifier']+"_player"+str(playerCount)+"_score.txt"


      if setup == True:
        player = "Setup"
        score = "N"
      f = open(player_path,"w")
      f.write(player)
      f.close()

      f = open(score_path,"w")
      f.write(str(score))
      f.close()

      playerCount = playerCount + 1