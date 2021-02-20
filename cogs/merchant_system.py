import discord, libraries.main_functions, os, json
from discord.ext import commands
from libraries.player_handling import Player
from libraries.merchant_handling import Merchant

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class merchant_system:
    '''Commands for merchant interactions.'''
    def __init__(self, bot):
        self.bot = bot
        print('Merchant System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def merchant(self, ctx, *merchant_name):
        '''Used to start an interaction with a merchant.'''
        #Check if user is in a fight or a trade
        if os.path.isfile('data/enemies/' + str(ctx.author.id) + '.json'):
            await ctx.author.send('Can\'t access a merchant while in a fight!')
            return
        elif os.path.isfile('data/trades/' + str(ctx.author.id) + '.json'):
            await ctx.author.send('Can\'t access a merchant while in a trade!')
            return

        if len(merchant_name) == 0: #if there was no merchant name we display all possible merchants if the user is in a city or possibilities if the user is at a merchant
            if os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'):
                with open('data/merchants/temporary/' + str(ctx.author.id) + '.json', 'r') as user_merchant_file:
                    self.user_merchant_data = json.load(user_merchant_file)
                if self.user_merchant_data['Choice'] == None:
                    await ctx.author.send('What would you like to do?\n.buy - to buy an item\n.sell - to sell n item\n.exitmerchant - to exit a merchant interaction\n\n')
                elif self.user_merchant_data['Choice'] == 'Buy':
                    await ctx.author.send('Well choose what item ya want with .buy <item>')
                elif self.user_merchant_data['Choice'] == 'Sell':
                    await ctx.author.send('Well choose what item ya want to sell with .sell <item>')
            else:
                await ctx.author.send(libraries.main_functions.display_possible_merchants(ctx.author.id))
        elif len(merchant_name) == 1: #If entered a good merchant name we start the merchant interaction by creating a temp file
            self.player = Player(ctx.author.id)
            self.merchant_id = libraries.main_functions.get_merchant_id(self.player.get_coords(), merchant_name[0])
            del self.player
            if self.merchant_id == None:
                await ctx.author.send('That merchant isn\'t here...')
            else:
                self.merchant = Merchant(ctx.author.id, self.merchant_id)
                await ctx.author.send(self.merchant.initiate_merchant())
                del self.merchant
        elif len(merchant_name) > 1: #If entered more than one merchant name we tell it's too many arguments
            await ctx.author.send('Too many arguments!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def buy(self, ctx, *item_name):
        '''Used to buy an item from a merchant.'''
        if os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'):
            if len(item_name) == 0: #If didn't specify an item we display all the possible ones
                with open('data/merchants/temporary/' + str(ctx.author.id) + '.json', 'r') as user_merchant_file:
                    self.user_merchant_data = json.load(user_merchant_file)
                self.merchant = Merchant(ctx.author.id, self.user_merchant_data['Merchant'])
                await ctx.author.send(self.merchant.show_available_items_to_buy())
                del self.merchant
            elif len(item_name) > 0: #If specifies the item we buy it. Remove money rom player inventory and add it to player inventory
                self.item = ' '.join(item_name)
                with open('data/merchants/temporary/' + str(ctx.author.id) + '.json', 'r') as user_merchant_file:
                    self.user_merchant_data = json.load(user_merchant_file)
                self.merchant = Merchant(ctx.author.id, self.user_merchant_data['Merchant'])
                await ctx.author.send(self.merchant.buy(self.item))
                del self.merchant
        else: #if not at a merchant we tell the user
            await ctx.author.send('You aren\'t at a merchant. Can\'t do that!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def sell(self, ctx, *item_name):
        '''Used to sell an item to a merchant.'''
        if os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'):
            if len(item_name) == 0: #If no arguments provided we show the user all items possible to sell
                with open('data/merchants/temporary/' + str(ctx.author.id) + '.json', 'r') as user_merchant_file:
                    self.user_merchant_data = json.load(user_merchant_file)
                self.merchant = Merchant(ctx.author.id, self.user_merchant_data['Merchant'])
                await ctx.author.send(self.merchant.show_available_items_to_sell())
                del self.merchant
            elif len(item_name) > 0: #If there is an item name we sell it and remoe from the player
                self.item = ' '.join(item_name)
                with open('data/merchants/temporary/' + str(ctx.author.id) + '.json', 'r') as user_merchant_file:
                    self.user_merchant_data = json.load(user_merchant_file)
                self.merchant = Merchant(ctx.author.id, self.user_merchant_data['Merchant'])
                await ctx.author.send(self.merchant.sell(self.item))
                del self.merchant
        else: #if not at a merchant we tell the player so
            await ctx.author.send('You aren\'t at a merchant. Can\'t do that!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def exitmerchant(self, ctx):
        '''Used to exit the interaction with a merchant.'''
        if os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'):
            await ctx.author.send('Well see you next time traveller!')
            os.remove('data/merchants/temporary/' + str(ctx.author.id) + '.json') #Exit the merchant and delete the temporary file
        else:
            await ctx.author.send('You aren\'t at a merchant. Can\'t do that!')

def setup(bot):
    bot.add_cog(merchant_system(bot))