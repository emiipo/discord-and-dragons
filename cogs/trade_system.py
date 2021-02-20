import discord
from discord.ext import commands
from libraries.trade_handling import Trade

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class trade_system:
    '''Commands for the trade system.'''
    def __init__(self, bot):
        self.bot = bot
        print('Trade System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def trade(self, ctx, *trader_name):
        '''Used to offer someone a trade.'''
        if len(trader_name) == 0: #If the user hasnt specified with whom to trade we tell them
            await ctx.author.send('To trade with someone do .trade <discord-name#id>\n(for example .trade user#1234 IT IS CASE SENSITIVE)')
        elif len(trader_name) > 0:
            self.trader = None
            self.name = ' '.join(trader_name)
            if self.name == str(ctx.author): #if uer trying to trade with themselves we tell its not possible
                await ctx.author.send('Can\'t trade with yourself!')
                return
            for user in self.bot.guilds[0].members:
                if str(user) == self.name:
                    self.trader = user
                    break
            if self.trader: #Send the other user a message saying someone wants to trade
                self.trade = Trade(ctx.author.id)
                self.message, self.trade_possible = self.trade.initiate_trade(self.trader)
                await ctx.author.send(self.message)
                del self.trade
                if self.trade_possible:
                    await self.trader.send(str(ctx.author) + ' has sent you a trade offer!\n(Type .tradeaccept to accept or .tradedecline to decline)')
            else: #if the user doesnt exist we tell them
                await ctx.author.send('That user doesn\'t exist. Try again!\n(IT IS CASE SENSITIVE)')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradeadd(self, ctx, *item_name):
        '''Used to add an item to a trade.'''
        if len(item_name) == 0:
            await ctx.author.send('Please specify what item to add!')
        elif len(item_name) > 0: #If the user specified what item to add we try adding it
            self.item_name = ' '.join(item_name)
            self.trade = Trade(ctx.author.id)
            self.message, self.inviter_id, self.trade_unconfirmed = self.trade.trade_add(self.item_name)
            await ctx.author.send(self.message)
            del self.trade
            if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
                for user in self.bot.guilds[0].members:
                    if user.id == self.inviter_id:
                        if self.trade_unconfirmed:
                            await user.send(str(ctx.author) + ' added ' + self.item_name.title() + ' to the trade offer!\nThis made you unconfirm the trade to prevent scamming.')
                        else:
                            await user.send(str(ctx.author) + ' added ' + self.item_name.title() + ' to the trade offer!')
                        break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def traderemove(self, ctx, *item_name):
        '''Used to remove an item from a trade.'''
        if len(item_name) == 0:
            await ctx.author.send('Please specify what item to remove!')
        elif len(item_name) > 0: #If the user is trying to remove an item
            self.item_name = ' '.join(item_name)
            self.trade = Trade(ctx.author.id)
            self.message, self.inviter_id, self.trade_unconfirmed = self.trade.trade_remove(self.item_name)
            await ctx.author.send(self.message)
            del self.trade
            if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
                for user in self.bot.guilds[0].members:
                    if user.id == self.inviter_id:
                        if self.trade_unconfirmed:
                            await user.send(str(ctx.author) + ' removed ' + self.item_name.title() + ' from the trade offer!\nThis made you unconfirm the trade to prevent scamming.')
                        else:
                            await user.send(str(ctx.author) + ' removed ' + self.item_name.title() + ' from the trade offer!')
                        break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradecheck(self, ctx):
        '''Used to check the items in the trade.'''
        self.trade = Trade(ctx.author.id)
        await ctx.author.send(self.trade.trade_check()) #Shows the information about the trade
        del self.trade

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradeaccept(self, ctx):
        '''Used to accept a trade offer.'''
        self.trade = Trade(ctx.author.id)
        self.message, self.inviter_id = self.trade.accept_trade() #The user accepts a trade sent to them
        await ctx.author.send(self.message)
        del self.trade
        if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
            for user in self.bot.guilds[0].members:
                if user.id == self.inviter_id:
                    await user.send('Your trade offer was accepted!\n------------\nChoices:\n.tradecheck - check items and gold in the trade\n.tradeadd <item> - add an item to trade\n.traderemove <item> - to remove an item\n.trademoney <amount> - add an amount of money (to deduct money make the amount negative)\n.tradeconfirm - to confirm the trade (both parties must do this for the trade to go through)\n.tradeuncofirm - to unconfirm the trade\n.tradecancel - to cancel the trade')
                    break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def trademoney(self, ctx, amount):
        '''Used to add/remove money to/from a trade.'''
        try: #Trying to convert the given money from str to int
            amount = int(amount)
        except ValueError:
            await ctx.author.send('Amount must be a number!')
        else:
            self.trade = Trade(ctx.author.id)
            self.message, self.inviter_id, self.trade_unconfirmed = self.trade.trade_money(amount) #Trade the money
            await ctx.author.send(self.message)
            del self.trade
            if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
                for user in self.bot.guilds[0].members:
                    if user.id == self.inviter_id:
                        if self.trade_unconfirmed:
                            if amount < 0:
                                await user.send(str(ctx.author) + ' deducted ' + str(-1*amount) + ' Gold from the trade offer!\nThis made you unconfirm the trade to prevent scamming.')
                            elif amount > 0:
                                await user.send(str(ctx.author) + ' added ' + str(amount) + ' Gold to the trade offer!\nThis made you unconfirm the trade to prevent scamming.')
                            break
                        else:
                            if amount < 0:
                                await user.send(str(ctx.author) + ' deducted ' + str(-1*amount) + ' Gold from the trade offer!')
                            elif amount > 0:
                                await user.send(str(ctx.author) + ' added ' + str(amount) + ' Gold to the trade offer!')
                            break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradedecline(self, ctx):
        '''Used to decline a trade.'''
        self.trade = Trade(ctx.author.id)
        self.message, self.inviter_id = self.trade.decline_trade() #Decline the trade
        await ctx.author.send(self.message)
        del self.trade
        if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
            for user in self.bot.guilds[0].members:
                if user.id == self.inviter_id:
                    await user.send('Your trade offer was declined!')
                    break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradeconfirm(self, ctx):
        '''Used to confirm a trade.'''
        self.trade = Trade(ctx.author.id)
        self.message, self.inviter_id, self.trade_done = self.trade.confirm_trade() #Accept a trae
        await ctx.author.send(self.message)
        del self.trade
        if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
            for user in self.bot.guilds[0].members:
                if user.id == self.inviter_id:
                    if self.trade_done:
                        await user.send('Trade completed!\n(Do .inventory to check your new items)')
                    else:
                        await user.send(str(ctx.author) + ' confirmed the trade!')
                    break

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradeunconfirm(self, ctx):
        '''Used to unconfirm a trade.'''
        self.trade = Trade(ctx.author.id)
        self.message, self.inviter_id = self.trade.unconfirm_trade() #Try to unconfirm the trade
        await ctx.author.send(self.message)
        del self.trade
        if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
            for user in self.bot.guilds[0].members:
                if user.id == self.inviter_id:
                    await user.send(str(ctx.author) + ' unconfirmed the trade!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def tradecancel(self, ctx):
        '''Used to cancel a trade.'''
        self.trade = Trade(ctx.author.id)
        self.message, self.inviter_id = self.trade.cancel_trade() #We try canceling the trade
        await ctx.author.send(self.message)
        del self.trade
        if self.inviter_id: #If it was successfull we get the other person they are trading to and we send them a message
            for user in self.bot.guilds[0].members:
                if user.id == self.inviter_id:
                    await user.send(str(ctx.author) + ' canceled the trade!')
                    break

def setup(bot):
    bot.add_cog(trade_system(bot))
