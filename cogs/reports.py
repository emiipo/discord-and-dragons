import discord, json
from discord.ext import commands

OWNER_ID = 83616065854115840

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class report():
    '''Commands for the report system.'''
    def __init__(self, bot):
        self.bot = bot
        print('Report System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def bug(self, ctx, *message):
        '''Used to report a bug to the creator.'''
        #Open the general bug file to determine the ID of this new bug
        with open('data/reports/bugs/general_data.json', 'r') as general_bug_file:
            self.general_bug_data = json.load(general_bug_file)
        self.general_bug_data['Amount'] += 1
        #Join up all arguments into one message
        message = ' '.join(message)
        #Create the bug data with the message
        self.bug_data = {
            'By': ctx.author.name,
            'Bug': message,
            'Status': 'Unresolved'
        }
        #Write the bug message to file for later use. Also increase total bug amount in the general file
        with open('data/reports/bugs/'+str(self.general_bug_data['Amount'])+'.json', 'w') as bug_file:
            json.dump(self.bug_data, bug_file)
        with open('data/reports/bugs/general_data.json', 'w') as general_bug_file:
            json.dump(self.general_bug_data, general_bug_file)
        #Thank the used for submitting the bug
        await ctx.author.send('Thank you for submitting a bug report!')
        #Using this we also send the bug to the creator.
        for user in self.bot.guilds[0].members:
            if OWNER_ID == user.id:
                await user.send('('+ctx.author.name+') BUG: ' + message)

def setup(bot):
    bot.add_cog(report(bot))
