import os, json
from libraries.player_handling import Player

default_trade_directory = 'data/trades/'

class Trade:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player = Player(self.player_id)

    def initiate_trade(self, user):
        '''Used to initiate a trade.'''
        if not self.player.is_alive():
            return 'Can\'t trade while dead!\nPlease do .respawn!', False
        elif os.path.isfile('data/enemies/' + str(self.player_id) + '.json'):
            return 'Can\'t trade while in a fight!', False
        elif os.path.isfile('data/merchants/temporary/' + str(self.player_id) + '.json'):
            return 'Can\'t trade while at a merchant!', False
        elif os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            return 'Already sent/waiting or are in a trade! To cancel do .tradecancel or .tradedecline', False
        elif os.path.isfile(default_trade_directory + str(user.id) + '.json'):
            return 'The person you are sending an offer to is already in a trade!', False
        else: #Create trade data for both users
            self.trade_data_one = {
                'User': user.id,
                'Items': [],
                'Money': 0,
                'Status': 'Sent'
            }
            self.trade_data_two = {
                'User': self.player_id,
                'Items': [],
                'Money': 0,
                'Status': 'Waiting'
            }
            with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                json.dump(self.trade_data_one, trade_file)
            with open(default_trade_directory + str(user.id) + '.json', 'w') as trade_file:
                json.dump(self.trade_data_two, trade_file)
            return 'Sent a trade offer to ' + str(user) + '!', True #Tell that we sent the player a trade offer.

    def trade_check(self):
        '''Used to display what items and gold are in the trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Can\'t check trade info as it hasn\'t been accepted! To cancel do .tradecancel'
            if self.trade_data['Status'] == 'Waiting':
                return 'Can\'t check trade info as it hasn\'t been accepted! To accept do .tradeaccept'
            else:
                self.message = 'Your items:\n' #We dispaly what items the player has added in the trade
                if self.trade_data['Money'] > 0:
                    self.message += 'Gold: ' + str(self.trade_data['Money']) + '\n'
                self.trade_items = []
                self.temp_incrementor = {} #Using this for extra items we display xAmount
                for item in self.trade_data['Items']:
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        self.item = json.load(item_file)
                    if self.item['Name'] in self.trade_items:
                        self.temp_incrementor[self.item['Name']] += 1
                    else:
                        self.trade_items.append(self.item['Name'])
                        self.temp_incrementor[self.item['Name']] = 1
                for item in range(0, len(self.trade_items)):
                    if self.temp_incrementor[self.trade_items[item]] > 1:
                        self.trade_items[item] += ' x' + str(self.temp_incrementor[self.trade_items[item]])
                if len(self.trade_items) == 0 and self.trade_data['Money'] == 0:
                    self.message += 'None\n' #If there are no items or gold we display None
                else:
                    for item in self.trade_items:
                        self.message += item + '\n'

                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                self.message += '------------\nRecieving items:\n' #Using this we display the items the player would recieve
                if self.new_trade_data['Money'] > 0:
                    self.message += 'Gold: ' + str(self.new_trade_data['Money']) + '\n'
                self.new_trade_items = []
                self.new_temp_incrementor = {} #Using this for extra items we display xAmount
                for item in self.new_trade_data['Items']:
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        self.item = json.load(item_file)
                    if self.item['Name'] in self.new_trade_items:
                        self.new_temp_incrementor[self.item['Name']] += 1
                    else:
                        self.new_trade_items.append(self.item['Name'])
                        self.new_temp_incrementor[self.item['Name']] = 1
                for item in range(0, len(self.new_trade_items)):
                    if self.new_temp_incrementor[self.new_trade_items[item]] > 1:
                        self.new_trade_items[item] += ' x' + str(self.new_temp_incrementor[self.new_trade_items[item]])
                if len(self.new_trade_items) == 0 and self.new_trade_data['Money'] == 0:
                    self.message += 'None\n' #If there are no items or gold we display None
                else:
                    for item in self.new_trade_items:
                        self.message += item + '\n'

                return self.message
        else:
            return 'Not in a trade!'

    def trade_add(self, item_name):
        '''Used to add an item to a trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Trade needs to be accepted first! To cancel do .tradecancel', None, None
            if self.trade_data['Status'] == 'Trading':
                self.inventory = self.player.get_inventory_ids()
                self.item_id = None
                for item in self.inventory: #Check if the player added an item they have
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        self.item_data = json.load(item_file)
                    if self.item_data['Name'] == item_name.title():
                        self.item_id = item
                        break
                if self.item_id == None:
                    return 'You don\'t have that item!', None, None
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                self.trade_unconfirmed = False
                if self.new_trade_data['Status'] == 'Confirmed': #If the trade is confirmed we unconfirm it to prevent scams
                    self.new_trade_data['Status'] = 'Trading'
                    with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'w') as trade_file:
                        json.dump(self.new_trade_data, trade_file)
                    self.trade_unconfirmed = True
                self.trade_data['Items'].append(self.item_id) #add the item to the trade
                with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                    json.dump(self.trade_data, trade_file)
                self.player.remove_item(self.item_id) #remove it from the players inventory
                if self.trade_unconfirmed:
                    return 'Successfully added ' + item_name.title() + ' to the trade!\nThis made the other party to unconfirm to prevent from scamming.', self.trade_data['User'], self.trade_unconfirmed
                else:
                    return 'Successfully added ' + item_name.title() + ' to the trade!', self.trade_data['User'], self.trade_unconfirmed
            if self.trade_data['Status'] == 'Confirmed':
                return 'Can\'t add an item to a confirmed trade! To unconfirm do .tradeunconfirm', None, None
            if self.trade_data['Status'] == 'Waiting':
                return 'Trade needs to be accepted first! To accept do .tradeaccept', None, None
        else:
            return 'You aren\'t in a trade.', None, None

    def trade_remove(self, item_name):
        '''Used to remove an item from a trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Trade needs to be accepted first! To cancel do .tradecancel', None, None
            if self.trade_data['Status'] == 'Trading':
                self.inventory = self.player.get_inventory_ids()
                self.item_id = None
                for item in self.trade_data['Items']: #Check if the item is in the trade
                    with open('data/items/' + str(item) + '.json', 'r') as item_file:
                        self.item_data = json.load(item_file)
                    if self.item_data['Name'] == item_name.title():
                        self.item_id = item
                        break
                if self.item_id == None:
                    return 'That item isn\'t in the trade!', None, None
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                self.trade_unconfirmed = False
                if self.new_trade_data['Status'] == 'Confirmed': #If the trade is confirmed we unconfirm to prevent scams
                    self.new_trade_data['Status'] = 'Trading'
                    with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'w') as trade_file:
                        json.dump(self.new_trade_data, trade_file)
                    self.trade_unconfirmed = True
                self.trade_data['Items'].remove(self.item_id) #remove the item from the trade
                with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                    json.dump(self.trade_data, trade_file)
                self.player.add_item(self.item_id) #add it back to the players inventory
                if self.trade_unconfirmed:
                    return 'Successfully removed ' + item_name.title() + ' from the trade!\nThis made the other party to unconfirm to prevent from scamming.', self.trade_data['User'], self.trade_unconfirmed
                else:
                    return 'Successfully removed ' + item_name.title() + ' from the trade!', self.trade_data['User'], self.trade_unconfirmed
            if self.trade_data['Status'] == 'Confirmed':
                return 'Can\'t remove an item from a confirmed trade! To unconfirm do .tradeunconfirm', None, None
            if self.trade_data['Status'] == 'Waiting':
                return 'Trade needs to be accepted first! To accept do .tradeaccept', None, None
        else:
            return 'You aren\'t in a trade.', None, None

    def trade_money(self, amount):
        '''Used to add or remove oney to/from a trade'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Trade needs to be accepted first! To cancel do .tradecancel', None, None
            if self.trade_data['Status'] == 'Trading':
                if amount > self.player.get_money():
                    return 'You don\'t have enough gold!', None, None
                else:
                    if self.trade_data['Money'] + amount < 0: #Make sure the player cant make trade money amount less than 0
                        return 'Doing this would make the offered gold amount less than zero!', None, None
                    else:
                        with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                            self.new_trade_data = json.load(trade_file)
                        self.trade_unconfirmed = False
                        if self.new_trade_data['Status'] == 'Confirmed': #If the trade is confirmed we unconfirm it to prevent scams
                            self.new_trade_data['Status'] = 'Trading'
                            with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'w') as trade_file:
                                json.dump(self.new_trade_data, trade_file)
                            self.trade_unconfirmed = True
                        self.trade_data['Money'] += amount #add the money to the trade
                        with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                            json.dump(self.trade_data, trade_file)
                        self.player.modify_money(amount*-1) #remove the money from the player
                        if self.trade_unconfirmed:
                            if amount > 0:
                                return 'Successfully added ' + str(amount) + ' Gold to the trade!\nThis made the other party unconfirm the trade to prevent scamming.', self.trade_data['User'], self.trade_unconfirmed
                            elif amount < 0:
                                return 'Successfully deducted ' + str(-1*amount) + ' Gold from the trade!\nThis made the other party unconfirm the trade to prevent scamming.', self.trade_data['User'], self.trade_unconfirmed
                        else:
                            if amount > 0:
                                return 'Successfully added ' + str(amount) + ' Gold to the trade!', self.trade_data['User'], self.trade_unconfirmed
                            elif amount < 0:
                                return 'Successfully deducted ' + str(-1*amount) + ' Gold from the trade!', self.trade_data['User'], self.trade_unconfirmed
            if self.trade_data['Status'] == 'Confirmed':
                return 'Can\'t add money to a confirmed trade! To unconfirm do .tradeunconfirm', None, None
            if self.trade_data['Status'] == 'Waiting':
                return 'Trade needs to be accepted first! To accept do .tradeaccept', None, None
        else:
            return 'You aren\'t in a trade.', None, None

    def decline_trade(self):
        '''Used to decline a trade offer.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Can\'t decline a trade you sent! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Trading':
                return 'Can\'t decline a trade that is happening! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Confirmed':
                return 'Can\'t decline a trade that is happening! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Waiting':
                os.remove(default_trade_directory + str(self.trade_data['User']) + '.json')
                os.remove(default_trade_directory + str(self.player_id) + '.json')
                return 'Trade Declined!', self.trade_data['User']
        else:
            return 'You haven\'t been offered a trade.', None

    def accept_trade(self):
        '''Used to accept a trade offer.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Can\'t accept a trade you sent! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Trading':
                return 'Can\'t accept a trade that is happening! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Confirmed':
                return 'Can\'t accept a trade that is happening! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Waiting':
                self.trade_data['Status'] = 'Trading'
                with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                    json.dump(self.trade_data, trade_file)
                self.new_trade_data = self.trade_data.copy()
                self.new_trade_data['User'] = self.player_id
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'w') as trade_file:
                    json.dump(self.new_trade_data, trade_file)
                return 'Trade Accepted!\n------------\nChoices:\n.tradecheck - check items and gold in the trade\n.tradeadd <item> - add an item to trade\n.traderemove <item> - to remove an item\n.trademoney <amount> - add an amount of money (to deduct money make the amount negative)\n.tradeconfirm - to confirm the trade (both parties must do this for the trade to go through)\n.tradeunconfirm - to unconfirm the trade\n.tradecancel - to cancel the trade', self.trade_data['User']
        else:
            return 'You haven\'t been offered a trade.', None

    def confirm_trade(self):
        '''Used to confirm the trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Trade needs to be accepted first! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Trading':
                self.message = 'Trade confirmed!\n'
                self.trade_data['Status'] = 'Confirmed'
                with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                    json.dump(self.trade_data, trade_file)
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                if self.new_trade_data['Status'] == 'Confirmed': #We check if the other player has confirmed the trade if yes we add each player their money and items
                    self.trading_player = Player(self.trade_data['User'])
                    for item in self.trade_data['Items']:
                        self.trading_player.add_item(item)
                    self.trading_player.modify_money(self.trade_data['Money'])
                    del self.trading_player
                    with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                        self.new_trade_data = json.load(trade_file)
                    for item in self.new_trade_data['Items']:
                        self.player.add_item(item)
                    self.player.modify_money(self.new_trade_data['Money'])
                    os.remove(default_trade_directory + str(self.trade_data['User']) + '.json')
                    os.remove(default_trade_directory + str(self.player_id) + '.json')
                    self.message += '\nTrade completed!\n(Do .inventory to check your new items)'
                    return self.message, self.trade_data['User'], True
                else: #If the other player hasn't confirmed we say so.
                    self.message += 'Waiting for other party to confirm!'
                    return self.message, self.trade_data['User'], False
            if self.trade_data['Status'] == 'Confirmed':
                return 'Trade already confirmed! To unconfirm do .tradeunconfirm', self.trade_data['User']
            if self.trade_data['Status'] == 'Waiting':
                return 'Trade needs to be accepted first! To accept do .tradeaccept', None
        else:
            return 'You aren\'t in a trade.', None

    def unconfirm_trade(self):
        '''Used to unconfirm a trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                return 'Trade needs to be accepted first! To cancel do .tradecancel', None
            if self.trade_data['Status'] == 'Trading':
                return 'You need to confirm to be able to unconfirm. To confirm do .tradeconfirm!', None
            if self.trade_data['Status'] == 'Confirmed':
                self.trade_data['Status'] = 'Trading'
                with open(default_trade_directory + str(self.player_id) + '.json', 'w') as trade_file:
                    json.dump(self.trade_data, trade_file)
                return 'Unconfirmed the trade!', self.trade_data['User']
            if self.trade_data['Status'] == 'Waiting':
                return 'Trade needs to be accepted first! To accept do .tradeaccept', None
        else:
            return 'You aren\'t in a trade.', None

    def cancel_trade(self):
        '''Used to cancel a trade.'''
        if os.path.isfile(default_trade_directory + str(self.player_id) + '.json'):
            with open(default_trade_directory + str(self.player_id) + '.json', 'r') as trade_file:
                self.trade_data = json.load(trade_file)
            if self.trade_data['Status'] == 'Sent':
                os.remove(default_trade_directory + str(self.trade_data['User']) + '.json')
                os.remove(default_trade_directory + str(self.player_id) + '.json')
                return 'Canceled the trade!', self.trade_data['User']
            if self.trade_data['Status'] == 'Trading': #If the players are in trading status we also give them back their items.
                for item in self.trade_data['Items']:
                    self.player.add_item(item)
                self.player.modify_money(self.trade_data['Money'])
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                self.trading_player = Player(self.trade_data['User'])
                for item in self.new_trade_data['Items']:
                    self.trading_player.add_item(item)
                self.trading_player.modify_money(self.new_trade_data['Money'])
                del self.trading_player
                os.remove(default_trade_directory + str(self.trade_data['User']) + '.json')
                os.remove(default_trade_directory + str(self.player_id) + '.json')
                return 'Canceled the trade!', self.trade_data['User']
            if self.trade_data['Status'] == 'Confirmed': #If the players are in confirmed status we also give them back their items.
                for item in self.trade_data['Items']:
                    self.player.add_item(item)
                self.player.modify_money(self.trade_data['Money'])
                with open(default_trade_directory + str(self.trade_data['User']) + '.json', 'r') as trade_file:
                    self.new_trade_data = json.load(trade_file)
                self.trading_player = Player(self.trade_data['User'])
                for item in self.new_trade_data['Items']:
                    self.trading_player.add_item(item)
                self.trading_player.modify_money(self.new_trade_data['Money'])
                del self.trading_player
                os.remove(default_trade_directory + str(self.trade_data['User']) + '.json')
                os.remove(default_trade_directory + str(self.player_id) + '.json')
                return 'Canceled the trade!', self.trade_data['User']
            if self.trade_data['Status'] == 'Waiting':
                return 'To decline the trade please do .tradedecline', None
        else:
            return 'You aren\'t in a trade.', None