import json, os
from libraries import main_functions
from libraries.enemy_handling import Enemy
from libraries.player_handling import Player

default_directory = 'data/players/'
tutorial_directory = 'data/story/tutorial/'

class Story:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player = Player(self.player_id)

    def display_line(self, line_id):
        '''Used to display a story line.'''
        if os.path.isfile('data/enemies/' + str(self.player_id) + '.json'):
            return 'Can\'t do that while in a fight!'
        elif os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            return 'Can\'t do that while at a merchant!'
        elif os.path.isfile('data/trades/' + str(self.player_id) + '.json'):
            return 'Can\'t do that while in a trade!'

        with open(tutorial_directory+str(line_id)+'.json', 'r') as line_file:
            self.line_data = json.load(line_file)
        if 'Position' in self.line_data: #If the story requires a specific position we check if the player is there
            x, y = self.player.get_coords()
            if self.line_data['Position'] != [x, y]:
                return 'Seems like you are at the wrong position for that!'
        if self.line_data['Type'] == 'Text': #If the type of the line is just text we display it
            if '$player_name' in self.line_data['Line']:
                self.line_data['Line'] = self.line_data['Line'].replace('$player_name', self.player.get_name())
            self.set_story_id(self.line_data['Next']) #And set the new story id to the player
            return self.line_data['Line']
        elif self.line_data['Type'] == 'Condition': #If the type is a condition
            if self.line_data['Condition'] == 'Health': #If the condition for a specific health we check if the player has it
                if self.player.get_health() >= self.line_data['Health']:
                    if '$player_name' in self.line_data['True']: #If the line has the variables $player_name we change it into the players name
                        self.line_data['True'] = self.line_data['True'].replace('$player_name', self.player.get_name())
                    self.set_story_id(self.line_data['Next'])
                    if 'State' in self.line_data: #If there is a need to change the players state we do so
                        self.player.set_state(self.line_data['State'])
                    return self.line_data['True']
                else: #If the condfition hasnt been met
                    if '$player_name' in self.line_data['False']: #If the line has the variables $player_name we change it into the players name
                        self.line_data['False'] = self.line_data['False'].replace('$player_name', self.player.get_name())
                    return self.line_data['False']
            if self.line_data['Condition'] == 'Level': #If the condition for a specific level we check if the player has it
                if self.player.get_level() >= self.line_data['Level']:
                    if '$player_name' in self.line_data['True']: #If the line has the variables $player_name we change it into the players name
                        self.line_data['True'] = self.line_data['True'].replace('$player_name', self.player.get_name())
                    self.set_story_id(self.line_data['Next'])
                    if 'State' in self.line_data: #If there is a need to change the players state we do so
                        self.player.set_state(self.line_data['State'])
                    return self.line_data['True']
                else: #If the condfition hasnt been met
                    if '$player_name' in self.line_data['False']: #If the line has the variables $player_name we change it into the players name
                        self.line_data['False'] = self.line_data['False'].replace('$player_name', self.player.get_name())
                    return self.line_data['False']

    def get_story_id(self):
        '''Used to get the ID where the player is in the story.'''
        with open(default_directory+str(self.player_id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Story']

    def set_story_id(self, id):
        '''Used to change the players story id.'''
        with open(default_directory+str(self.player_id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Story'] = id
        with open(default_directory+str(self.player_id)+'.json', 'w') as user_file:
            json.dump(self.user_data, user_file)