import discord, os
from discord.ext import commands
from libraries.enemy_handling import Enemy
from libraries.fight_handling import Fight
from libraries.player_handling import Player

default_fight_directory = 'data/enemies/'
SPECIAL = [(0,0),(0,6),(6,6)]

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class fight_system:
    '''Commands for fights'''
    def __init__(self, bot):
        self.bot = bot
        print('Fight System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    @commands.is_owner()
    async def startfight(self, ctx):
        '''Used to start a fight with a random enemy. TESTING & OWNER ONLY.'''
        self.fight = Fight(ctx.author.id)
        await ctx.author.send(self.fight.initiate_fight()) #Using this we call the initiate_fight function and whatever is returned we send to the user
        del self.fight

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def attack(self, ctx):
        '''Used to choose an option in a fight.'''
        self.fight = Fight(ctx.author.id)
        self.message = self.fight.attack()
        await ctx.author.send(self.message) #Using this we call the attack function and whatever is returned we send to the user
        del self.fight
        if 'Successfully moved!' in self.message: #if the string is in the message means the player was moving before so we send their new location
            self.player = Player(ctx.author.id)
            self.player.save_map()
            file = discord.File('data/players/maps/' + str(ctx.author.id) + '.png')
            await ctx.author.send(file=file)
            await self.update_ranks(ctx, self.player.get_coords())
            del self.player

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def run(self, ctx):
        '''Used to choose an option in a fight.'''
        self.fight = Fight(ctx.author.id)
        await ctx.author.send(self.fight.run()) #Using this we call the run function and whatever is returned we send to the user
        del self.fight

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def item(self, ctx, *item_name):
        '''Used to use an item during a fight.'''
        self.fight = Fight(ctx.author.id)
        self.item_name = ' '.join(item_name)
        self.message = self.fight.use_item(self.item_name)
        await ctx.author.send(self.message) #Using this we call the use_item function and whatever is returned we send to the user
        del self.fight
        if 'Successfully moved!' in self.message: #if the string is in the message means the player was moving before so we send their new location
            self.player = Player(ctx.author.id)
            self.player.save_map()
            file = discord.File('data/players/maps/' + str(ctx.author.id) + '.png')
            await ctx.author.send(file=file)
            await self.update_ranks(ctx, self.player.get_coords())
            del self.player

    async def update_ranks(self, ctx, coords):
        '''Used to update the ranks in the server according to the users position'''
        #We get the roles from the server
        self.city_one = discord.utils.get(self.bot.guilds[0].roles, name='City One')
        self.city_two = discord.utils.get(self.bot.guilds[0].roles, name='City Two')
        self.city_three = discord.utils.get(self.bot.guilds[0].roles, name='City Three')
        self.wilderness = discord.utils.get(self.bot.guilds[0].roles, name='Wilderness')
        if coords in SPECIAL: #If user went to a city we remove the wilderness role and give them a city role
            for user in self.bot.guilds[0].members:
                if ctx.author == user:
                    await user.remove_roles(self.wilderness)
                    if coords == (0, 0):
                        await user.add_roles(self.city_one)
                    elif coords == (0, 6):
                        await user.add_roles(self.city_two)
                    elif coords == (6, 6):
                        await user.add_roles(self.city_three)
        else: #If user went to wilderness we remove all city roles and give wilderness role
            for user in self.bot.guilds[0].members:
                if ctx.author == user:
                    await user.remove_roles(self.city_one, self.city_two, self.city_three)
                    await user.add_roles(self.wilderness)

def setup(bot):
    bot.add_cog(fight_system(bot))