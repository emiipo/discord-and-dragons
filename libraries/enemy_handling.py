import json, random


default_user_directory = 'data/players/'
default_enemy_directory = 'data/enemies/'
default_regular_directory = 'data/enemies/templates/regular/'

class Enemy:
    '''Used for enemy handling.'''
    def __init__(self, id):
        self.id = id

    def add_health(self, amount):
        '''Used to add health to an enemy.'''
        with open(default_enemy_directory + str(self.id) + '.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        self.enemy_data['Current Health'] += amount #GEts the current health an adds a specific amount to it. If the amount is bigger than max possible we set it to the max
        if self.enemy_data['Current Health'] > self.enemy_data['Max Health']:
            self.enemy_data['Current Health'] = self.enemy_data['Max_Health']
        with open(default_enemy_directory + str(self.id) + '.json', 'w') as enemy_file:
            json.dump(self.enemy, enemy_file)

    def get_health(self):
        '''Used to get the health of an enemy.'''
        with open(default_enemy_directory + str(self.id) + '.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        return self.enemy_data['Current Health']

    def get_agility(self):
        '''Used to get the agility of an enemy.'''
        with open(default_enemy_directory + str(self.id) + '.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        return self.enemy_data['Agility']

    def do_damage(self):
        '''Used to make the enemy generate a random damage amount.'''
        with open(default_enemy_directory + str(self.id) + '.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        return random.randrange(self.enemy_data['Damage'][0], self.enemy_data['Damage'][1]) #We use the specified range of the damage to randomize the damage

    def take_damage(self, amount):
        '''Use to inflict damage to the enemy.'''
        with open(default_enemy_directory+str(self.id)+'.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        self.enemy_data['Current Health'] -= amount
        if self.enemy_data['Current Health'] < 0: #If the health goes below 0 we set it to 0
            self.enemy_data['Current Health'] = 0
        with open(default_enemy_directory+str(self.id)+'.json', 'w') as enemy_file:
            json.dump(self.enemy_data, enemy_file)

    def is_alive(self):
        '''Used to check if the enemy is alive.'''
        with open(default_enemy_directory+str(self.id)+'.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        if self.enemy_data['Current Health'] > 0:
            return True
        else:
            return False

    def get_run_chance(self):
        '''Used to get the run chance from an enemy.'''
        with open(default_enemy_directory + str(self.id) + '.json', 'r') as enemy_file:
            self.enemy_data = json.load(enemy_file)
        return self.enemy_data['Run chance']

    def create_enemy(self):
        '''Used to create an enemy file.'''
        with open(default_user_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        with open(default_regular_directory+'0.json', 'r') as enemy_file:
            self.template_enemy_data = json.load(enemy_file)

        self.level = self.user_data['Level'] + random.randrange(-2,2) #Set a random level to the enemy based on the players level
        if self.level < 0:
            self.level = 0
        if self.level > 13:
            self.level = 13

        self.health = random.randrange(self.template_enemy_data['Health'][str(self.level)][0], self.template_enemy_data['Health'][str(self.level)][1]) #Choose a random amount for the enemies health out of the health range for the specific level

        self.enemy_data = { #Create enemy data that will be stored in the enemy file
            'Name': 'Placeholder name',
            'Type': 'Orc',
            'Level': self.level,
            'Max Health': self.health,
            'Current Health': self.health,
            'Damage': self.template_enemy_data['Damage'][str(self.level)],
            'Agility': random.randrange(1, 3),
            'Run chance': random.randrange(20, 95),
        }

        with open(default_enemy_directory+str(self.id)+'.json', 'w') as enemy_file:
            json.dump(self.enemy_data, enemy_file)
