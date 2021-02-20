import os, json
from libraries.player_handling import Player

default_merchant_temp_directory = 'data/merchants/temporary/'
default_merchant_directory = 'data/merchants/'

class Merchant:
    def __init__(self, player_id, merchant_id):
        self.player_id = player_id
        self.player = Player(self.player_id)
        self.id = merchant_id

    def get_merchant_name(self):
        '''Used to get the name of a merchant.'''
        self.coords = self.player.get_coords()
        with open(default_merchant_directory + str(self.coords[0]) + ',' + str(self.coords[1]) + '/' + str(self.id) + '.json', 'r') as merchant_file:
            self.merchant_data = json.load(merchant_file)
        return self.merchant_data['Name']

    def initiate_merchant(self):
        '''Used to start an interaction with a merchant.'''
        self.merchant_name = self.get_merchant_name()
        if os.path.isfile(default_merchant_temp_directory + str(self.player_id) + '.json'):
            with open(default_merchant_temp_directory + str(self.player_id) + '.json', 'r') as user_merchant_file:
                self.user_merchant_data = json.load(user_merchant_file)

            if self.user_merchant_data['Merchant'] != self.id: #if the player changed a merchant we start a new interaction
                self.user_merchant_data = {
                    'Choice': None,
                    'Merchant': self.id
                }
                with open(default_merchant_temp_directory + str(self.player_id) + '.json', 'w') as user_merchant_file:
                    json.dump(self.user_merchant_data, user_merchant_file)
                return self.merchant_name + ':\nAlright! Welcome traveler! What would you like to do?\n.buy - to buy an item\n.sell - to sell n item\n.exitmerchant - to exit a merchant interaction\n\n'
            else: #If the player is at the same merchant we tell them so
                if self.user_merchant_data['Choice'] == None:
                    return self.merchant_name + ':\nWhat would you like to do?\n.buy - to buy an item\n.sell - to sell n item\n.exitmerchant - to exit a merchant interaction\n\n'
                elif self.user_merchant_data['Choice'] == 'Buy':
                    return self.merchant_name + ':\nWell choose what item ya want with .buy <item>'
                elif self.user_merchant_data['Choice'] == 'Sell':
                    return self.merchant_name + ':\nWell choose what item ya want to sell with .sell <item>'
        else: #If the player just enetered a merchant we start the interaction.
            self.user_merchant_data = {
                'Choice': None,
                'Merchant': self.id
            }
            with open(default_merchant_temp_directory + str(self.player_id) + '.json', 'w') as user_merchant_file:
                json.dump(self.user_merchant_data, user_merchant_file)
            return self.merchant_name + ':\nAlright! Welcome traveler! What would you like to do?\n.buy - to buy an item\n.sell - to sell n item\n.exitmerchant - to exit a merchant interaction\n\n'

    def show_available_items_to_buy(self):
        '''Used to show the items a player can buy.'''
        self.merchant_name = self.get_merchant_name()
        self.coords = self.player.get_coords()
        #Get the data of the merchant the player is at
        with open(default_merchant_directory + str(self.coords[0]) + ',' + str(self.coords[1]) + '/' + str(self.id) + '.json', 'r') as merchant_file:
            self.merchant_data = json.load(merchant_file)

        self.message = self.merchant_name + ':\nCurrently I have:\n' #show all the items the merchant has to sell
        for item in self.merchant_data['Items']:
            with open('data/items/' + str(item) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.message += self.item_data['Name'] + ' - Price: ' + str(self.item_data['Buy Price']) + '\n'
        self.message += '\n(Do .buy <item> to buy)'
        self.user_merchant_data = {
            'Choice': 'Buy',
            'Merchant': self.id
        }
        with open(default_merchant_temp_directory + str(self.player_id) + '.json', 'w') as user_merchant_file:
            json.dump(self.user_merchant_data, user_merchant_file)
        return self.message

    def show_available_items_to_sell(self):
        '''Used to show items the player can sell.'''
        self.merchant_name = self.get_merchant_name()
        #Get the data of the player
        with open('data/players/'+str(self.player_id)+'.json', 'r') as user_file:
            self.user_data = json.load(user_file)

        self.message = self.merchant_name + ':\nYou can sell:\n'
        for item in self.user_data['Inventory']: #Get all the items from the players inventory
            with open('data/items/' + str(item) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            self.message += self.item_data['Name'] + ' - Price: ' + str(self.item_data['Sell Price']) + '\n'
        self.message += '\n(Do .sell <item> to sell)'
        self.user_merchant_data = {
            'Choice': 'Sell',
            'Merchant': self.id
        }
        with open(default_merchant_temp_directory + str(self.player_id) + '.json', 'w') as user_merchant_file:
            json.dump(self.user_merchant_data, user_merchant_file)
        return self.message

    def buy(self, item_b):
        '''Used to buy an item from a merchant.'''
        self.merchant_name = self.get_merchant_name()
        self.coords = self.player.get_coords()
        with open(default_merchant_directory + str(self.coords[0]) + ',' + str(self.coords[1]) + '/' + str(self.id) + '.json', 'r') as merchant_file:
            self.merchant_data = json.load(merchant_file)

        self.item_id = None
        for item in self.merchant_data['Items']: #We find the item and get its data
            with open('data/items/' + str(item) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if self.item_data['Name'] == item_b.title():
                self.item_id = item
                self.item_price = self.item_data['Buy Price']
        if self.item_id == None:
            return self.merchant_name + ':\nI don\'t have that...'
        if self.player.get_money() >= self.item_price: #If the player has enough money
            # After buying the item we give the player the item and take away the money
            self.player.add_item(self.item_id)
            self.player.modify_money(-1 * self.item_price)
            return self.merchant_name + ':\nSuccesfully bought the item.'
        else:
            return self.merchant_name + ':\nNot enough money!'

    def sell(self, item_s):
        '''Used to sell an item to a merchant.'''
        self.merchant_name = self.get_merchant_name()
        self.coords = self.player.get_coords()
        with open('data/players/' + str(self.player_id) + '.json', 'r') as user_file:
            self.user_data = json.load(user_file)

        self.item_id = None
        for item in self.user_data['Inventory']: #We find the item and get its data
            with open('data/items/' + str(item) + '.json', 'r') as item_file:
                self.item_data = json.load(item_file)
            if self.item_data['Name'] == item_s.title():
                self.item_id = item
                self.item_price = self.item_data['Sell Price']
        if self.item_id == None:
            return self.merchant_name + ':\nYou don\'t have that...'

        #After selling the item we give the player the money and take away the item
        self.player.remove_item(self.item_id)
        self.player.modify_money(self.item_price)
        return self.merchant_name + ':\nSuccessfully sold the item!'





