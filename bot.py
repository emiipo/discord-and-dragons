#imports
import discord, datetime
from discord.ext import commands

#constants
TOKEN = '' #This is the token to login into the bot account
TESTING_TOKEN = ''

#List of cogs. Cogs are external files that hold different functions for the bot.
cogs = ['cogs.story_system', 'cogs.character_creation', 'cogs.main_commands', 'cogs.merchant_system', 'cogs.fight_system', 'cogs.trade_system', 'cogs.reports']

#Making my own object of the bot from discord.py library so incase I need to I can add other functions.
class DungeonBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        '''Main bot object. This is used to play the game through discord.'''
        #Call in the constructor of the orginal bot
        super().__init__(*args, **kwargs)
        #Load external cogs
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('Failed to load extension ' + cog + '.')
                print(e)

    async def on_ready(self):
        '''Function that runs when the bot starts.'''
        #If we don't have it we set the uptime of the bot
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.now()

        #Print as what user we are logged in
        print('-' * 30)
        print('Logged in as:')
        print('Name: ' + self.user.name)
        print('ID: ' + str(self.user.id))
        print('-' * 30)

#Establish connection
bot = DungeonBot(command_prefix='.')
bot.run(TESTING_TOKEN)