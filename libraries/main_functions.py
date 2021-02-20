import json, random, os
from libraries.player_handling import Player
from libraries.fight_handling import Fight

SPECIAL = [(0,0),(0,6),(6,6)]

def get_players_in_location(x, y, user_ID):
    '''Used to get all the users in the same area as the player.'''
    with open('data/location_data.json') as location_information: #Get information from location data
        location_data = json.load(location_information)
    players = []
    for player in location_data[str(x)+','+str(y)]: #If the players are in the same position we add them to the list
        if not player == user_ID:
            with open('data/players/'+str(player)+'.json','r') as player_info:
                neighbour_player = json.load(player_info)
                players.append(neighbour_player['Name'])
    return players

def display_stats(id):
    '''Used to display the players stats.'''
    player = Player(id)
    player_stats = player.get_stats()
    player_stats_increase = player.get_stats_increase()
    #We get the stats and extra stats and print it
    message = 'Your stats:\n'
    message += 'Health: ' + str(player_stats[0][0]) + '/' + str(player_stats[0][1]) + '     (+' + str(player_stats_increase[0]) + ')\n'
    message += 'Level: ' + str(player_stats[1]) + '\n'
    message += 'XP: ' + str(player_stats[2][0]) + '/' + str(player_stats[2][1]) + '\n'
    message += 'Damage: ' + str(player_stats[3][0]) + '-' + str(player_stats[3][1]) + '     (+' + str(player_stats_increase[1]) + ')\n'
    message += 'Defense: ' + str(player_stats[4]) + '     (+' + str(player_stats_increase[2]) + ')\n'
    message += 'Agility: ' + str(player_stats[5]) + '     (+' + str(player_stats_increase[3]) + ')\n'
    message += 'Luck: ' + str(player_stats[6]) + '     (+' + str(player_stats_increase[4]) + ')'
    return message

def use_item(item_name, player_id):
    '''Used so the player could use an item'''
    if os.path.isfile('data/merchants/temporary/' + str(player_id) + '.json'):
        message = 'Can\'t use an item while at a merchant!'
    elif os.path.isfile('data/enemies/' + str(player_id) + '.json'):
        message = 'While in a fight please use .item'
    else:
        if item_name == '': #If the player didn't specify what we display all items that the player can use
            message = 'You can use:\n'
            for item in show_available_items_to_use(player_id):
                message += item + '\n'
            message += '\n(To use an item please do .use <item>)'
            return message
        else:
            if item_name.title() in show_available_items_to_use(player_id)  and item_name.lower() != 'none': #If the item is not none and is in available items to use
                with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
                    user_data = json.load(user_file)
                for item in user_data['Inventory']: #we get the items id from the players inventory since we know they have it since it's been shown in show_available_items_to_use
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        item_data = json.load(item_file)
                    if item_data['Name'] == item_name.title():
                        item_id = item
                        break
                player = Player(player_id)
                if item_data['Effect'] == 'Heal': #If the effect is to heal
                    if item_data['Target'] == 'Player': #If the target is the player we heal the player
                        player.add_health(item_data['Heal Amount'])
                        message = 'Healed yourself by ' + str(item_data['Heal Amount']) + 'HP\n'
                    elif item_data['Target'] == 'Enemy': #If the target is the enemy we tell there is no enemy
                        message = 'This can only be used in a fight!\n'
                elif item_data['Effect'] == 'Damage': #If the effect is to damage
                    if item_data['Target'] == 'Player': #If the target is the player we damage the player
                        player.take_damage(item_data['Damage Amount'])
                        message = 'Damaged yourself by ' + str(item_data['Damage Amount']) + 'HP\n'
                    elif item_data['Target'] == 'Enemy': #If the target is the enemy we tell there is no enemy
                        message = 'This can only be used in a fight!\n'
                player.remove_item(item_id) #Remove the item from the players inventory
                if not player.is_alive(): #If player died after the item usage we tell them so
                    message += 'You died!.\n'
                    message += '\n\nTo respawn do .respawn'
                del player
                return message
            else:
                return 'Can\'t use that item...'
    return message

def unequip_item(item_name, player_id):
    '''Used to unequip an item'''
    if os.path.isfile('data/enemies/' + str(player_id) + '.json'):
        message = 'Can\'t unequip an item while in a fight'
    else:
        if item_name == '': #If the player didn't specify what we display all items that the player can unequip
            message = 'You can unequip:\n'
            for item in show_available_items_to_unequip(player_id):
                message += item + '\n'
            message += '\n(To unequip an item please do .unequip <item>)'
            return message
        else:
            if item_name.title() in show_available_items_to_unequip(player_id) and item_name.lower != 'none':
                with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
                    user_data = json.load(user_file)
                for item in user_data['Inventory']:
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        item_data = json.load(item_file)
                    if item_data['Name'] == item_name.title():
                        user_data[item_data['Type']] = -1
                        with open('data/players/' + str(player_id) + '.json', 'w') as user_file:
                            json.dump(user_data, user_file)
                        break
                return 'Successfully unequipped ' + item_name.title()
            else:
                return 'Can\'t unequip that item...'
    return message

def equip_item(item_name, player_id):
    '''Used to equip an item'''
    if os.path.isfile('data/enemies/' + str(player_id) + '.json'):
        message = 'Can\'t equip an item while in a fight'
    else:
        if item_name == '': #If the player didn't specify what we display all items that the player can equip
            message = 'You can equip:\n'
            for item in show_available_items_to_equip(player_id):
                message += item + '\n'
            message += '\n(To equip an item please do .equip <item>)'
            return message
        else:
            if item_name.title() in show_available_items_to_equip(player_id) and item_name.lower != 'none':
                with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
                    user_data = json.load(user_file)
                for item in user_data['Inventory']:
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        item_data = json.load(item_file)
                    print(item_name.title() + '    ' + item_data['Name'])
                    if item_data['Name'] == item_name.title():
                        user_data[item_data['Type']] = item
                        with open('data/players/' + str(player_id) + '.json', 'w') as user_file:
                            json.dump(user_data, user_file)
                        break
                return 'Successfully equipped ' + item_name.title()
            else:
                return 'Can\'t equip that item...'
    return message

def show_available_items_to_unequip(player_id):
    '''Used to show the player the items they can unequip.'''
    with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
        user_data = json.load(user_file)
    available_items = []
    if user_data['Weapon'] is not -1:
        with open('data/items/' + str(user_data['Weapon']) + '.json', 'r') as item_file:
            item_data = json.load(item_file)
        available_items.append(item_data['Name'])
    if user_data['Armour'] is not -1:
        with open('data/items/' + str(user_data['Armour']) + '.json', 'r') as item_file:
            item_data = json.load(item_file)
        available_items.append(item_data['Name'])
    if user_data['Accessory'] is not -1:
        with open('data/items/' + str(user_data['Accessory']) + '.json', 'r') as item_file:
            item_data = json.load(item_file)
        available_items.append(item_data['Name'])
    if len(available_items) == 0:
        available_items.append('None') #If the player doesn't have any items they can equip we print None
    return available_items

def show_available_items_to_equip(player_id):
    '''Used to show the player the items they can equip.'''
    with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
        user_data = json.load(user_file)
    available_items = []
    for item in user_data['Inventory']:
        with open('data/items/' + str(item) + '.json', 'r') as item_file:
            item_data = json.load(item_file)
        if item_data['Type'] == 'Weapon' or item_data['Type'] == 'Armour' or item_data['Type'] == 'Accessory':
            available_items.append(item_data['Name'])
    if len(available_items) == 0:
        available_items.append('None') #If the player doesn't have any items they can equip we print None
    return available_items

def show_available_items_to_use(player_id):
    '''Used to show the player the items they can use.'''
    with open('data/players/' + str(player_id) + '.json', 'r') as user_file:
        user_data = json.load(user_file)
    available_items = []
    for item in user_data['Inventory']: #All the items with type 'Effect' get returned withing a list
        with open('data/items/' + str(item) + '.json', 'r') as item_file:
            item_data = json.load(item_file)
        if item_data['Type'] == 'Effect':
            available_items.append(item_data['Name'])
    if len(available_items) == 0:
        available_items.append('None') #If the player doesn't have any items they can use we print None
    return available_items

def display_inventory(id):
    '''Used to display the players inventory.'''
    player = Player(id)
    player_inventory = player.get_inventory()
    message = 'Your inventory:\n'
    for item in player_inventory: #Get all the items in their inventory and return the list
        message += str(item) + '\n'
    return message

def display_equipment(id):
    '''Used to display the players equipment'''
    player = Player(id)
    return player.get_equipment()

def display_possible_merchants(id):
    '''Used to display all possible merchants the player can interact with.'''
    player = Player(id)
    coords = player.get_coords()
    del player
    if coords in SPECIAL: #If the player is in a city
        with open('data/merchants/'+str(coords[0])+','+str(coords[1])+'/general_data.json', 'r') as general_file:
            general_data = json.load(general_file)
        message = 'Available merchants:\n'
        for merchant in general_data['Merchants']: #Using this we display all the merchants according to the players position
            with open('data/merchants/'+str(coords[0])+','+str(coords[1])+'/'+str(merchant)+'.json', 'r') as merchant_file:
                merchant_data = json.load(merchant_file)
            message += merchant_data['Name'] + '\n'
        if message == 'Available merchants:\n':
            message += 'None\n'
        else:
            message += '\n(User .merchant <name> to choose a merchant)'
        return message
    else:
        return 'Sorry merchants can only be found in a city!'

def get_merchant_id(coords, name):
    '''Used to get the merchant ID from their name and location.'''
    with open('data/merchants/' + str(coords[0]) + ',' + str(coords[1]) + '/general_data.json', 'r') as general_file:
        general_data = json.load(general_file)
    for merchant in general_data['Merchants']: #check the merchants in a specific location
        with open('data/merchants/' + str(coords[0]) + ',' + str(coords[1]) + '/' + str(merchant) + '.json', 'r') as merchant_file:
            merchant_data = json.load(merchant_file)
        if merchant_data['Name'] == name.title():
            return merchant
    return None