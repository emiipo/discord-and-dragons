import json, random, libraries.map_rendering

#XP FORMULA int((level*prevlvl*2.5)/(1.75*(level-1))) WHEN XP FOR LEVEL 1 IS 100
LEVEL_XP = {1:100,2:285,3:610,4:1161,5:2073,6:3553,7:5921,8:9666,9:15534,10:24657,11:38746,12:60383,
            13:93449,14:143767,15:220051,16:335315,17:508960,18:769855,19:1160892,20:1745702,21:2618553,
            22:3918922,23:5852935,24:8724872,25:12983440,26:19289682,27:28616561,28:42394905,
            29:62727155,30:92700229,31:136843195,32:201796416,33:297289362,34:437568757,35:643483466,
            36:945526725,37:1388273366,38:2036848953,39:2986357487,40:4375615365,41:6407151070,
            42:9376318639,43:13713663315,44:20046551025,45:29288792081,46:42770934467,47:62429624843,
            48:91082735333,49:132828989027,50:193628263887,51:282144041663,52:410966111105,53:598384722213,
            54:870964285700,55:1267276077076,56:1843310657565,57:2680324170438,58:3896210573569,
            59:5661980882772,60:8225638086351,61:11946760077795,62:17346583719514,63:25180524754133,
            64:36543165176066,65:53020217331345,66:76908447117994,67:111533895171116,68:161712257390957,
            69:234414826890252,70:339731633174278,71:492264203170892,72:13139288295859,
            73:1032920000904716,74:1495813699940293,75:2165753426554478,76:3135185912726482,
            77:4537769084209382,78:6566715928911536,79:9501292278095446,80:13745088286575692,
            81:19881288414511268,82:28752480599469560,83:41575886581114520,84:60109715538960752,
            85:86893296272307216,86:125593671922998656,87:181505804938552864,88:262274397940766048,
            89:378935412609223680,90:547418734106422656,91:790715949264832640,92:1142007336457842944,
            93:1649172085257443840,94:2381293026331792896,95:3438037044096053248,
            96:4963181296740166656,97:7164115859877918720,98:10339961034875344896,
            99:14922101201933807616,100:21532613567004049408}
INACCESSABLE = [(1,0),(5,0),(6,0),(1,1),(3,1),(6,1),(1,3),(4,3),(5,3),(0,4),(3,4),(4,4),(5,4),(1,6),(4,6)]
SPECIAL = [(0,0),(0,6),(6,6)]
START_POS = {'A-INHABITANT':(0,0),'A-NEWCOMER':(0,0),'H-INHABITANT':(0,6),'H-BANISHED':(0,6),'NEUTRAL':(6,6)}

default_directory = 'data/players/'
temp_directory = 'data/players/temporary/'

class Player:
    def __init__(self, id):
        self.id = id

    def check_if_exists(self):
        '''Used to check if a player file exists.'''
        try:
            file = open(default_directory + str(self.id)+'.json','r')
        except FileNotFoundError:
            return False
        else:
            file.close()
            return True

    def save_map(self):
        '''Used to save a map with the players position.'''
        libraries.map_rendering.show_map(7, 7, INACCESSABLE, SPECIAL, self.get_coords(), self.id, self.get_agility())

    def add_xp(self, amount):
        '''Used to add xp to the player.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['XP'] += amount
        with open(default_directory+str(self.id)+'.json', 'w') as user_file:
            json.dump(self.user_data, user_file)
        self.message = self.check_for_levelup() #After giving xp we also check if the player leveled up!
        return 'Gained ' + str(amount) + 'XP\n' + self.message

    def check_for_levelup(self):
        '''Used to check if the player leveled up.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.temp_xp = self.user_data['XP']
        self.temp_level = self.user_data['Level']
        self.temp_damage = self.user_data['Damage']
        self.temp_health = self.user_data['Max Health']
        self.temp_defense = self.user_data['Defense']
        self.message = ''
        #After geting temporary variables of the players stats we check if the player has gained any extra stats
        while self.temp_xp >= LEVEL_XP[self.temp_level+1]:
            self.temp_level += 1
            #We generate random amounts of stats increase to add to the player
            self.damage_increase = random.randrange(1, 5)
            self.temp_damage[0] += self.damage_increase
            self.temp_damage[1] += self.damage_increase
            self.health_increase = random.randrange(1, 4)
            self.temp_health += self.health_increase
            self.defense_increase = random.randrange(1, 3)
            self.temp_defense += self.defense_increase
            self.message += 'Succesfully leveled up! New level: ' + str(self.temp_level) + '\n' #If the player leveled up we tell them about that.
        #Afterwards we add set the temp stats to the current stats. If the stats didnt change they staye the same
        self.user_data['Level'] = self.temp_level
        self.user_data['Damage'] = self.temp_damage
        self.user_data['Defense'] = self.temp_defense
        if self.user_data['Max Health'] != self.temp_health:
            self.user_data['Max Health'] = self.temp_health
            self.user_data['Current Health'] = self.temp_health
        with open(default_directory + str(self.id) + '.json', 'w') as user_file:
            json.dump(self.user_data, user_file)
        return self.message

    def get_health(self):
        '''Used to get the current health of the player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Current Health']

    def get_agility(self):
        '''Used to get the agility of the player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.extra_agility = 0 #Using this we also add extra agility from item effects.

        #OLD
        #for item in self.user_data['Inventory']:
        #    with open('data/items/' + str(item) + '.json', 'r') as item_file:
        #        self.item_data = json.load(item_file)
        #    if self.item_data['Type'] == 'Accessory':
        #        if 'Agility' in self.item_data:
        #            self.extra_agility += self.item_data['Agility']

        if self.user_data['Accessory'] is not -1:
            with open('data/items/' + str(self.user_data['Accessory']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if 'Agility' in self.item_data:
                self.extra_agility += self.item_data['Agility']

        return self.user_data['Agility'] + self.extra_agility

    def get_level(self):
        '''Used to get the current level of a player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Level']

    def get_coords(self):
        '''Used to get the current coordinates of the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        return (self.user_data['X'],self.user_data['Y'])

    def get_stats(self):
        '''Used to get current stats of the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        return ((self.user_data['Current Health'], self.user_data['Max Health']), self.user_data['Level'], (self.user_data['XP'], LEVEL_XP[self.user_data['Level']+1]), self.user_data['Damage'], self.user_data['Defense'], self.user_data['Agility'], self.user_data['Luck'])

    def get_stats_increase(self):
        '''Used to get stats increase from accessories.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.health_increase = 0
        self.damage_increase = 0
        self.defense_increase = 0
        self.agility_increase = 0
        self.luck_increase = 0

        #OLD
        #for item in self.user_data['Inventory']: #Check every item and see if it gives an extra increase
        #    with open('data/items/'+str(item)+'.json', 'r') as item_file:
        #        self.item_data = json.load(item_file)
        #    if self.item_data['Type'] == 'Weapon':
        #        self.damage_increase += self.item_data['Damage']
        #    elif self.item_data['Type'] == 'Armour':
        #        self.defense_increase += self.item_data['Defense']
        #    elif self.item_data['Type'] == 'Accessory':
        #        if 'Health' in self.item_data:
        #            self.health_increase += self.item_data['Health']
        #        if 'Damage' in self.item_data:
        #            self.damage_increase_increase += self.item_data['Damage']
        #        if 'Defense' in self.item_data:
        #            self.defense_increase_increase += self.item_data['Defense']
        #        if 'Agility' in self.item_data:
        #            self.agility_increase += self.item_data['Agility']
        #        if 'Luck' in self.item_data:
        #            self.luck_increase += self.item_data['Luck']

        if self.user_data['Weapon'] is not -1:
            with open('data/items/' + str(self.user_data['Weapon']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.damage_increase += self.item_data['Damage']
        if self.user_data['Armour'] is not -1:
            with open('data/items/' + str(self.user_data['Armour']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.defense_increase += self.item_data['Defense']
        if self.user_data['Accessory'] is not -1:
            with open('data/items/' + str(self.user_data['Accessory']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if 'Health' in self.item_data:
                self.health_increase += self.item_data['Health']
            if 'Damage' in self.item_data:
                self.damage_increase += self.item_data['Damage']
            if 'Defense' in self.item_data:
                self.defense_increase += self.item_data['Defense']
            if 'Agility' in self.item_data:
                self.agility_increase += self.item_data['Agility']
            if 'Luck' in self.item_data:
                self.luck_increase += self.item_data['Luck']

        return (self.health_increase, self.damage_increase, self.defense_increase, self.agility_increase, self.luck_increase)

    def add_item(self, item_id):
        '''Used to add an item to a players inventory.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Inventory'].append(item_id)
        with open(default_directory+str(self.id)+'.json', 'w') as user_file:
            json.dump(self.user_data, user_file)

    def remove_item(self, item_id):
        '''Used to remove an item from a players inventory.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Inventory'].remove(item_id)
        with open(default_directory+str(self.id)+'.json', 'w') as user_file:
            json.dump(self.user_data, user_file)

    def get_inventory(self):
        '''Used to get items from a players inventory.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.inventory = ['Gold: '+str(self.user_data['Money'])]
        self.temp_incrementor = {} #Using this if the player has multiple items it shows the xAmount
        for item in self.user_data['Inventory']:
            with open('data/items/'+str(item)+'.json','r') as item_file:
                self.item = json.load(item_file)
            if self.item['Name'] in self.inventory:
                self.temp_incrementor[self.item['Name']] += 1
            else:
                self.inventory.append(self.item['Name'])
                self.temp_incrementor[self.item['Name']] = 1
        for item in range(1, len(self.inventory)):
            if self.temp_incrementor[self.inventory[item]] > 1:
                self.inventory[item] += ' x' + str(self.temp_incrementor[self.inventory[item]])
        for item in range(1, len(self.inventory)):
            for item_id in self.user_data['Inventory']:
                with open('data/items/' + str(item_id) + '.json', 'r') as item_file:
                    self.item = json.load(item_file)
                if self.inventory[item].startswith(self.item['Name']):
                    self.inventory[item] = self.inventory[item] + ' - ' + self.item['Description']
                    break
        return self.inventory

    def get_inventory_ids(self):
        '''Used to get the ID's of inventory items.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Inventory']

    def get_equipment(self):
        '''Used to get the players equipment'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.message = 'Equipment:\n'
        if self.user_data['Weapon'] == -1:
            self.message += 'Weapon: None\n'
        else:
            with open('data/items/' + str(self.user_data['Weapon']) + '.json', 'r') as item_file:
                self.item = json.load(item_file)
            self.message += 'Weapon: ' + self.item['Name'] + ' (+' + str(self.item['Damage']) + ')\n'
        if self.user_data['Armour'] == -1:
            self.message += 'Armour: None\n'
        else:
            with open('data/items/' + str(self.user_data['Armour']) + '.json', 'r') as item_file:
                self.item = json.load(item_file)
            self.message += 'Armour: ' + self.item['Name'] + ' (+' + str(self.item['Defense']) + ')\n'
        if self.user_data['Accessory'] == -1:
            self.message += 'Accessory: None\n'
        else:
            with open('data/items/' + str(self.user_data['Accessory']) + '.json', 'r') as item_file:
                self.item = json.load(item_file)
            self.message += 'Accessory: ' + self.item['Name'] + ' (+' + str(self.item['Luck']) + ')\n'
        self.message += '(To equip something type .equip <item> or to unequip .unequip <item>)'
        return self.message


    def get_money(self):
        '''Used to get current money of the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Money']

    def get_name(self):
        '''Used to get the name of the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        return self.user_data['Name']

    def get_defense(self):
        '''Used to get the defense stat of the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.extra_defense = 0 #With this we get any extra defense from inventory items

        #OLD
        #for item in self.user_data['Inventory']:
        #    with open('data/items/' + str(item) + '.json', 'r') as item_file:
        #        self.item_data = json.load(item_file)
        #    if self.item_data['Type'] == 'Armour':
        #        self.extra_defense += self.item_data['Defense']
        #    if self.item_data['Type'] == 'Accessory':
        #        if 'Defense' in self.item_data:
        #            self.extra_defense += self.item_data['Defense']

        if self.user_data['Armour'] is not -1:
            with open('data/items/' + str(self.user_data['Armour']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.extra_defense += self.item_data['Defense']

        return self.user_data['Defense'] + self.extra_defense

    def modify_money(self, amount):
        '''Used to give or take away money to/from the player.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Money'] += amount
        with open(default_directory+str(self.id)+'.json','w') as user_file:
            json.dump(self.user_data, user_file)

    def reset_position(self):
        '''Used to reset the players position to their starting one.'''
        with open(default_directory+str(self.id)+'.json','r') as user_file:
            self.user_data = json.load(user_file)
        self.move(START_POS[self.user_data['Backstory']][0], START_POS[self.user_data['Backstory']][1])

    def move(self, new_x, new_y):
        '''Used to change the players position.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        #With this we set min and max coordinates
        min_x = 0
        max_x = 6
        min_y = 0
        max_y = 6
        #If the new coordinates are withing the range we set them
        if min_x <= new_x <= max_x and min_y <= new_y <= max_y and (new_x, new_y) not in INACCESSABLE:
            self.remove_from_location(self.user_data['X'], self.user_data['Y'])
            self.user_data['X'] = new_x
            self.user_data['Y'] = new_y
            with open(default_directory + str(self.id) + '.json', 'w') as user_file:
                json.dump(self.user_data, user_file)
            self.add_to_location(new_x, new_y)
            return 'Successfully moved!'
        else:
            return 'Wrong coordinates!'

    def add_to_location(self, x, y):
        '''We change where the player is in location data.'''
        with open('data/location_data.json','r') as location_file:
            self.location_data = json.load(location_file)

        self.location_data[str(x)+','+str(y)].append(self.id)

        with open('data/location_data.json', 'w') as location_file:
            json.dump(self.location_data, location_file)

    def remove_from_location(self, x, y):
        '''We change where the player is in location data.'''
        with open('data/location_data.json','r') as location_file:
            self.location_data = json.load(location_file)

        self.location_data[str(x)+','+str(y)].remove(self.id)

        with open('data/location_data.json', 'w') as location_file:
            json.dump(self.location_data, location_file)

    def add_health(self, amount):
        '''We add health to the player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Current Health'] += amount
        if self.user_data['Current Health'] > self.user_data['Max Health']: #If the amount is bigger than the max we set it to max
            self.user_data['Current Health'] = self.user_data['Max Health']
        with open(default_directory + str(self.id) + '.json', 'w') as user_file:
            json.dump(self.user_data, user_file)

    def get_luck(self):
        '''Used to get luck of the player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.extra_luck = 0 #Used to see if items add any extra luck

        #OLD
        #for item in self.user_data['Inventory']:
        #    with open('data/items/' + str(item) + '.json', 'r') as item_file:
        #        self.item_data = json.load(item_file)
        #    if self.item_data['Type'] == 'Accessory':
        #        if 'Luck' in self.item_data:
        #            self.extra_luck += self.item_data['Luck']

        if self.user_data['Accessory'] is not -1:
            with open('data/items/' + str(self.user_data['Accessory']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if 'Luck' in self.item_data:
                self.extra_luck += self.item_data['Luck']

        return self.user_data['Luck'] + self.extra_luck

    def do_damage(self):
        '''Used to generate random damage from the player.'''
        with open(default_directory + str(self.id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.extra_damage = 0 #Check if items add any extra damage

        #OLD
        #for item in self.user_data['Inventory']:
        #    with open('data/items/'+str(item)+'.json', 'r') as item_file:
        #        self.item_data = json.load(item_file)
        #    if self.item_data['Type'] == 'Weapon':
        #        self.extra_damage += self.item_data['Damage']
        #    if self.item_data['Type'] == 'Accessory':
        #        if 'Damage' in self.item_data:
        #            self.extra_damage += self.item_data['Damage']

        if self.user_data['Weapon'] is not -1:
            with open('data/items/' + str(self.user_data['Weapon']) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.extra_damage += self.item_data['Damage']

        return random.randrange(self.user_data['Damage'][0], self.user_data['Damage'][1]) + self.extra_damage

    def take_damage(self, amount):
        '''Used to inflict damage to the player'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        self.user_data['Current Health'] -= amount
        if self.user_data['Current Health'] < 0:
            self.user_data['Current Health'] = 0
        with open(default_directory+str(self.id)+'.json', 'w') as user_file:
            json.dump(self.user_data, user_file)

    def is_alive(self):
        '''Used to check if the player is alive.'''
        with open(default_directory+str(self.id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)
        if self.user_data['Current Health'] > 0:
            return True
        else:
            return False

    def create_temp_user_file(self):
        '''Used to create a temporary user file.'''
        self.temp_data = {
            'Name': None,
            'Backstory': None
        }
        with open(temp_directory+str(self.id)+'.json', 'w') as temp_file:
            json.dump(self.temp_data, temp_file)

    def set_temp_name(self, name):
        '''Used to set a temporary player name in the temporary file.'''
        with open(temp_directory+str(self.id)+'.json', 'r') as temp_file:
            self.temp_data = json.load(temp_file)
        self.temp_data['Name'] = name
        with open(temp_directory+str(self.id)+'.json', 'w') as temp_file:
            json.dump(self.temp_data, temp_file)

    def set_temp_story(self, backstory):
        '''Used to set a temporary player story in the temporary file.'''
        with open(temp_directory+str(self.id)+'.json', 'r') as temp_file:
            self.temp_data = json.load(temp_file)
        self.temp_data['Backstory'] = backstory
        with open(temp_directory+str(self.id)+'.json', 'w') as temp_file:
            json.dump(self.temp_data, temp_file)

    def set_state(self, state):
        '''Used to change the state of a player.'''
        with open(default_directory+str(self.id)+'.json', 'r') as temp_file:
            self.temp_data = json.load(temp_file)
        self.temp_data['State'] = state
        with open(default_directory+str(self.id)+'.json', 'w') as temp_file:
            json.dump(self.temp_data, temp_file)

    def get_state(self):
        '''Used to get the state of a player.'''
        with open(default_directory+str(self.id)+'.json', 'r') as temp_file:
            self.temp_data = json.load(temp_file)
        return self.temp_data['State']

    def create_user_file(self, name, backstory, cords):
        '''Used to create a user file.'''
        self.player_data = {
            'Name': name,
            'XP': 0,
            'Level': 0,
            'Backstory': backstory,
            'Story': 0,
            'State': 'Tutorial',
            'X': cords[0],
            'Y': cords[1],
            'Max Health': 6,
            'Current Health': 2,
            'Damage': (2, 4),
            'Defense': 4,
            'Agility': 2,
            'Luck': 4,
            'Money': 10,
            'Inventory': [0, 1],
            'Weapon': -1,
            'Armour': -1,
            'Accessory': -1,
        }
        with open(default_directory+str(self.id)+'.json','w') as user_file:
            json.dump(self.player_data, user_file)

        self.add_to_location(self.player_data['X'],self.player_data['Y'])

        #Increase totalPlayers
        with open('data/general_information.json','r') as general_file:
            self.general_data = json.load(general_file)

        self.general_data['TotalPlayers'] += 1

        with open('data/general_information.json','w') as general_file:
            json.dump(self.general_data, general_file)