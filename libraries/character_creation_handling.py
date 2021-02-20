from libraries.player_handling import Player
from libraries.story_handling import Story
import json, os

INVALID_CHARACTERS = ('!','@','#','$','%','^','&','*','(',')','_','+','/','\\','1','2','3','4','5','6','7','8','9','0','`','{','}')
BACKSTORIES = {'1':'A-INHABITANT','2':'A-NEWCOMER','3':'H-INHABITANT','4':'H-BANISHED','5':'NEUTRAL'}
START_POS = {'A-INHABITANT':(0,0),'A-NEWCOMER':(0,0),'H-INHABITANT':(0,6),'H-BANISHED':(0,6),'NEUTRAL':(6,6)}

class CreateCharacter:
    '''Used to handle character creation.'''
    def __init__(self, id):
        self.id = id
        self.player = Player(self.id)

    #Used to set the name in a temporary file
    def set_temp_name(self, name):
        #If the name is too short or too long we tell the player
        if len(name) < 2:
            return 'What? No no no... Your name can\'t be one letter...'
        elif len(name) > 25:
            return 'No no no... I don\'t believe you. That is an impossibly long name...'

        #If the name has bad characters we tell the player
        self.bad_char = []
        for char in INVALID_CHARACTERS:
            if char in name:
                print(char)
                self.bad_char.append(char)
        if len(self.bad_char) > 0:
            return 'What? A name can\'t have ' + ', '.join(self.bad_char)+'!'

        #If everything is ok we put it in the temporary file
        self.player.set_temp_name(name)
        return 'Ahh yes... Nice to meet you '+str(name)+'!'

    #used to set the backstory in a temporary file
    def set_temp_story(self, story_number):
        #we check if the story number is a good one if not we tell the player
        if story_number not in ('1', '2', '3', '4', '5'):
            return 'No... Please choose a valid backstory!'
        else:
            self.player.set_temp_story(BACKSTORIES[story_number])
            return 'Ahh yes I see! Good to know! Now enjoy your adventure!'

    #Used to create the user file
    def create_user(self):
        with open('data/players/temporary/'+str(self.id)+'.json', 'r') as temp_file: #We get all the temporary data we have
            self.temp_data = json.load(temp_file)
        #using it we use the function from player_handling and create the user file
        self.player.create_user_file(self.temp_data['Name'], self.temp_data['Backstory'], START_POS[self.temp_data['Backstory']])
        os.remove('data/players/temporary/'+str(self.id)+'.json') #we also remove the temporary file
        self.story = Story(self.id)
        #afterwards we tell the player we created their character and kick off the tutorial
        return 'Character created! Enjoy the game! Please do .help for more commands.\n------------\n' + self.story.display_line(self.story.get_story_id())
