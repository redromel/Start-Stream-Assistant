# Start Stream Assistant
A python web-app built using NiceGUI that utilizes start.gg API in order to automatically fill in scoreboards and brackets using text files.  Built with OBS in mind in order to dock the Stream Assistant during events where screen space is limited
![enter image description here](https://cdn.discordapp.com/attachments/505825874491473927/1288398174834397204/image.png?ex=66f509ce&is=66f3b84e&hm=d42993378a1023aeb6af2ea24a7eef3a2360e361762450565b957ff36b5265c5&)

# What does it do?

The Start Stream Assistant allows the user to do two main things.  Automatically update a bracket graphic as the tournament goes on and automatically update and report the currently streamed match straight to start.gg.  This is done using text files that a streaming program like OBS can read to automatically update scores, names, and even flags on stream.  
# Setup
The zip file will contain a folder with the executable file and a .env file.  the .env file will have a blank spot where an API key can be input.

    smashgg_api = 'YOUR_API_KEY_HERE'
    
The program will still work without an API key however functionality will only be limited to using the scoreboard in manual input mode.

Place the folder in the place where you want to keep all of the text files for your choice of streaming program to read from later.  Once the program is run, it will automatically create the files needed in order for a scoreboard and a bracket graphic to be filled.  Your default web browser will also open with the program running under port 8080.  The Stream Assistant was built with being able to dock the web-app into OBS in mind
# How does it work?

The top of the Start Stream Assistant has an area to input the URL of the event you plan to run.  In order The Start Stream Assistant itself is divided into 2 sections.  the **Scoreboard** section and the **Bracket** section.  These 2 sections can be used at the same time.  

## Scoreboard
The scoreboard section is the only section that will work (albeit with limited functionality) without an API key.  Without a key, you can manually type in player, score, and round data right into the textboxes provided, as well as choose a flag or add in a custom flag for the players (how to do this will be discussed later).   Typing into the textboxes automatically updates a text file which OBS can read and automatically update on stream .  There is also a button that will clear all of the info as well as a button that will swap the two players.

![enter image description here](https://cdn.discordapp.com/attachments/505825874491473927/1288405101991694396/image.png?ex=66f51041&is=66f3bec1&hm=80a1a69874b110c84ec0b445af12e349866e301c04b05c2d1a951b16341962b4&)

If the stream assistant detects an API key then you have the option to put in a URL or slug to the event on on the top of the screen in order to pull up streamed matches.  Pressing the "Get Streamed Match" switch will grab any match that has the selected stream and is marked as started.  From there any changes to the score will not only update the score on the stream, but also live update the score on start.gg. 

![Updating the Scoreboard updates start.gg and the stream at the same time](https://cdn.discordapp.com/attachments/505825874491473927/1288405444838162526/image.png?ex=66f51093&is=66f3bf13&hm=efa452f3f76e9e4fda4b9c0ed2a337440634183b0d277e61d4778d5104feb176&)

 At the end of the set you can also report the score to start.gg to mark it as complete.  Note that for the updating and reporting specifically, the owner API Key must have access to edit and report matches in whatever event they are trying to report scores to, or else it will not work. 

![Option to Report Match](https://cdn.discordapp.com/attachments/505825874491473927/1288405566296821782/image.png?ex=66f510b0&is=66f3bf30&hm=9074f3b56f3f363ff1abfefb640609711ec21317da84c87d556c770b02f75163&)


### Flags

The flag dropdown menu has a list of every country and US state start.gg has in their system (Canadian provinces coming in a later update) as well as all of the pride flags.  If a player has a specified country or state in their bio, then the flag will be automatically fetched to be displayed on stream.  However, if there is a flag or any kind of logo (for example, team battles with custom logos or team logos) not in the system then there is an option to custom upload a file in order to accommodate everyone.  Due to the nature of the program, all custom flags will be lost once you close out of the program.

![Upload Custom Flag](https://cdn.discordapp.com/attachments/505825874491473927/1288405931712843847/image.png?ex=66f51107&is=66f3bf87&hm=d6f2e0b7c49418b48f2124c49f40e3bc9c4201e10d9540711878e42ef1af1525&)

## Bracket

The Bracket section is a lot simpler and requires an API Key in order to utilize.  After inputting the URL or slug of the tournament, a list of events, phases, and pools will populate.  Simply choose which Event, Phase, and Pool you want to have a bracket graphic for and click on the "Get Bracket" switch.  The switch will stay on until the bracket is complete or until it is manually turned off.  


Running this will give you a bunch of folders corresponding to the set of whatever bracket section you are trying to run.  For example if you are running a Top 8 bracket, it will have a file stating what game is being played and a folder for each set in Top 8 from which you can put them all into a bracket graphic.  As the bracket runs and matches complete, the Top 8 Bracket will automatically update.  This synergies well with the scoreboard section as once a score is reported during a Top 8, the bracket will automatically update. 

![The bracket is automatically updating](https://cdn.discordapp.com/attachments/505825874491473927/1288406417501323264/image.png?ex=66f5117b&is=66f3bffb&hm=4495b4ab841669b62a289907275da6a7f9b02c0baa650b5b7a86a18107143c34&)

For both the scoreboard and the bracket (bracket especially), it requires a lot of manual work in order to place everything where it belongs.  However, there is a lot of flexibility with how much can be added.  For the scoreboard, there is an option for pronouns as well which isn't being used in the same tournament I took the screenshots for.  For the bracket section, it is not limited to only Top 8, it can be a Top 24, Single-Elimination, etc.  (I have not tested a non-elimination style bracket like Swiss or Round Robin, and the Ladder format has proven to not work)



