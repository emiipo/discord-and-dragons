import os, json, random
from libraries.player_handling import Player
from libraries.enemy_handling import Enemy

default_fight_directory = 'data/enemies/'
default_player_directory = 'data/players/'

START_POS = {'A-INHABITANT':(0,0),'A-NEWCOMER':(0,0),'H-INHABITANT':(0,6),'H-BANISHED':(0,6),'NEUTRAL':(6,6)}

class Fight:
    '''Used for fight handling.'''
    def __init__(self, player_id):
        self.player_id = player_id
        self.player = Player(self.player_id)
        self.enemy = Enemy(self.player_id)

    def initiate_fight(self):
        '''Used to start a fight.'''
        if os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            return 'Can\'t initiate fight while at a merchant! Do .exitmerchant first'
        elif os.path.isfile(default_fight_directory + str(self.player_id) + '.json'):
            return 'Already in a fight!'
        else: #If the user can fight
            self.enemy.create_enemy() #create the enemy file
            self.message = ':crossed_swords: Got in a fight! :crossed_swords:'
            self.message += self.display_health() + '------------\n' #display the health
            if self.does_player_go_first(): #determine who goes first
                self.message += 'Player turn!\nChoice:\n.attack - attack the enemy\n.item <item> - use an item\n.run - try and run away' #If it's the players turn we display their choices
            else:
                self.message += self.enemy_choice() #If not we give the enemy a way to attack
                if self.player.is_alive(): #If the player is still alive after the enemies attack we give them their choices
                    self.message += 'Player turn!\nChoice:\n.attack - attack the enemy\n.item <item> - use an item\n.run - try and run away'
                else: #If the player died we tell them so and remove the enemy
                    self.message += 'You died! Good luck next time.\n'
                    self.message += '\n\nTo respawn do .respawn'
                    os.remove(default_fight_directory + str(self.player_id) + '.json')
            return self.message

    def check_for_player_move(self):
        '''Used to check if the player decided to move prior to the fight.'''
        if os.path.isfile('data/players/move/' + str(self.player_id) + '.json'):
            with open('data/players/move/' + str(self.player_id) + '.json', 'r') as move_file:
                self.move_data = json.load(move_file)
            self.message = self.player.move(self.move_data['X'], self.move_data['Y']) #If the player had to move we change their position
            os.remove('data/players/move/' + str(self.player_id) + '.json')
            return self.message
        return ' '

    def does_player_go_first(self):
        '''Used to determine if the player goes first in the fight.'''
        #We compare the enemeis and players agilities. The higher one goes first. If they are the same we pick at random
        if self.player.get_agility() > self.enemy.get_agility():
            return True
        elif self.player.get_agility() < self.enemy.get_agility():
            return False
        else:
            return random.choice((True, False))

    def attack(self):
        '''Used to attack the enemy.'''
        if os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            self.message = 'Can\'t fight while at a merchant!'
        elif os.path.isfile(default_fight_directory + str(self.player_id) + '.json'):
            self.player_damage = self.player.do_damage() #generate the player damage
            self.enemy.take_damage(self.player_damage) #inflict it to the enemy
            self.message = 'Player attacks with ' + str(self.player_damage) + ' damage!'
            self.message += self.display_health() #show everyones health
            self.message += '------------\n'
            if self.enemy.is_alive(): #if the enemy is still alive
                self.message += self.enemy_choice() #we make the enemy inflict damage
                if self.player.is_alive(): #If player is still alive after that we show them their choices
                    self.message += 'Player turn!\nChoice:\n.attack - attack the enemy\n.item <item> - use an item\n.run - try and run away'
                else: #If player died we tell them so
                    self.message += 'You died! Good luck next time.\n'
                    self.message += '\n\nTo respawn do .respawn'
                    os.remove(default_fight_directory + str(self.player_id) + '.json')
            else: #If the enemy died we congratule the player
                self.message += 'You won! Good job.\n'
                self.message += self.player.add_xp(random.randrange(23, 125)) #We give the player a random xp amount
                self.money_amount = random.randrange(1, 8)
                self.message += 'Earned ' + str(self.money_amount) + ' gold.' #We also give the player a random gold amount
                self.player.modify_money(self.money_amount)
                os.remove(default_fight_directory + str(self.player_id) + '.json')
                self.message += '\n' + self.check_for_player_move() #Check if the player tried moving prior to the fight
        else:
            self.message = 'You aren\'t in a fight!'
        return self.message

    def run(self):
        '''Used to try and run away from a fight.'''
        if os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            self.message = 'Can\'t fight while at a merchant!'
        elif os.path.isfile(default_fight_directory + str(self.player_id) + '.json'):
            self.run = random.randrange(0, 101) #generate a random chance of the player trying to run away
            if self.run + self.player.get_luck() > self.enemy.get_run_chance(): #We also add the luck to the players roll. If their run chacne is bigger
                self.message = 'Ran away successfully!'
                os.remove(default_fight_directory + str(self.player_id) + '.json') #the player runs away and we get rid of the enemy
                self.message += '\n' + self.check_for_player_move() #We also check if the player tried moving prior to the fight
            else:
                self.message = 'Couldn\'t run away!\n' #If the player couldn't run away we tell them so
                self.message += self.enemy_choice() #Then its the enemies turn
                if self.player.is_alive(): #If player is still alive after that we give them their choices
                    self.message += 'Player turn!\nChoice:\n.attack - attack the enemy\n.item <item> - use an item\n.run - try and run away'
                else: #If not we tell the player they died
                    self.message += 'You died! Good luck next time.\n'
                    self.message += '\n\nTo respawn do .respawn'
                    os.remove(default_fight_directory + str(self.player_id) + '.json')
        else:
            self.message = 'You aren\'t in a fight!'
        return self.message

    def show_available_items_to_use(self):
        '''Used to show items that can be used in battle.'''
        with open(default_player_directory + str(self.player_id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.available_items = []
        for item in self.user_data['Inventory']: #We check every item in the players inventory. If its of the type 'Effect' they can use it and we add it to the list
            with open('data/items/' + str(item) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if self.item_data['Type'] == 'Effect':
                self.available_items.append(self.item_data['Name'])
        if len(self.available_items) == 0:
            self.available_items.append('None') #If the player doesn't have any items they can use we print None
        return self.available_items #Return available items to use

    def use_item(self, item_name):
        '''Used to use an item.'''
        if os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            self.message = 'Can\'t fight while at a merchant!'
        elif os.path.isfile(default_fight_directory + str(self.player_id) + '.json'):
            if item_name == '': #If the player didn't enter an item name we show all the items they can use
                self.message = 'You can use:\n'
                for item in self.show_available_items_to_use():
                    self.message += item + '\n'
                self.message += '\n(To use an item please do .item <item>)'
                return self.message
            else:
                if item_name.title() in self.show_available_items_to_use() and item_name.lower() != 'none': #If the item is not none and in the available items list
                    with open(default_player_directory + str(self.player_id) + '.json', 'r') as user_file:
                        self.user_data = json.load(user_file)
                    for item in self.user_data['Inventory']: #we get the items id from the players inventory since we know they have it since it's been shown in show_available_items_to_use
                        with open('data/items/' + str(item) + '.json', 'r') as item_file:
                            self.item_data = json.load(item_file)
                        if self.item_data['Name'] == item_name.title():
                            self.item_id = item
                            break
                    if self.item_data['Effect'] == 'Heal': #If the effect is to heal
                        if self.item_data['Target'] == 'Player': #If the target is the player we heal the player
                            self.player.add_health(self.item_data['Heal Amount'])
                            self.message = 'Healed the player by ' + str(self.item_data['Heal Amount']) + 'HP\n'
                        elif self.item_data['Target'] == 'Enemy': #If the target is the enemy we heal the enemy
                            self.enemy.add_health(self.item_data['Heal Amount'])
                            self.message = 'Healed the enemy by ' + str(self.item_data['Heal Amount']) + 'HP\n'
                    elif self.item_data['Effect'] == 'Damage': #If the effect is to damage
                        if self.item_data['Target'] == 'Player': #If the target is the player we damage the player
                            self.player.take_damage(self.item_data['Damage Amount'])
                            self.message = 'Damaged the player by ' + str(self.item_data['Damage Amount']) + 'HP\n'
                        elif self.item_data['Target'] == 'Enemy': #If the target is the enemy we damage the enemy
                            self.enemy.take_damage(self.item_data['Damage Amount'])
                            self.message = 'Damaged the enemy by ' + str(self.item_data['Damage Amount']) + 'HP\n'
                    self.player.remove_item(self.item_id) #We rewmove the item from the players inventory
                    self.message += self.display_health() #Show everyones health
                    if self.player.is_alive(): #If player is still alive after that
                        if self.enemy.is_alive(): #If the enemy is still alive after that
                            self.message += '------------\n'
                            self.message += self.enemy_choice() #We make the enemy inflict damage
                            if self.player.is_alive(): #If player still alive after that we give them their choice
                                self.message += 'Player turn!\nChoice:\n.attack - attack the enemy\n.item <item> - use an item\n.run - try and run away'
                            else: #If the player is dead we tell them
                                self.message += 'You died! Good luck next time.\n'
                                self.message += '\n\nTo respawn do .respawn'
                                os.remove(default_fight_directory + str(self.player_id) + '.json')
                        else: #If the enemy is dead we tell the player won
                            self.message += 'You won! Good job.\n'
                            self.message += self.player.add_xp(random.randrange(23, 125)) #we give the player a random xp amount
                            self.money_amount = random.randrange(1, 8)
                            self.message += 'Earned ' + str(self.money_amount) + ' gold.' #We give the player a random gold amount
                            self.player.modify_money(self.money_amount)
                            os.remove(default_fight_directory + str(self.player_id) + '.json')
                            self.message += '\n' + self.check_for_player_move() #We check if the player was to move prior to the fight
                    else: #If not we tell them they died and delete the enemy
                        self.message += 'You died! Good luck next time.\n'
                        self.message += '\n\nTo respawn do .respawn'
                        os.remove(default_fight_directory + str(self.player_id) + '.json')
                    return self.message
                else:
                    return 'Can\'t use that item...'
        else:
            return 'Not in a fight.'


    def enemy_choice(self):
        '''Used so the enemy could do damage.'''
        self.enemy_damage = self.enemy.do_damage() - random.randrange(0, self.player.get_defense())
        if self.enemy_damage < 0:
            self.enemy_damage = 0
        self.player.take_damage(self.enemy_damage) #The damage is generated from the enemy and inflicted to the player
        self.message = 'Enemy attacks with ' + str(self.enemy_damage) + ' damage!'
        self.message += self.display_health()
        self.message += '------------\n'
        return self.message

    def display_health(self):
        '''Used to display health of the player and the enemy.'''
        self.message = '\nPlayer Health: ' + str(self.player.get_health()) + '\nEnemy Health: ' + str(self.enemy.get_health()) + '\n'
        return self.message