import discord, os, json
from discord.ext import commands
from libraries.character_creation_handling import CreateCharacter
from libraries.embed import NPC
from libraries.player_handling import Player

#used to check if the command is executed in the channel #start-here or direct messages
async def in_start_channel_or_dm(ctx):
    return ctx.channel.id == 505028786492932106 or isinstance(ctx.channel, discord.DMChannel)

#Making the object for the cog
class character_creation:
    '''Commands for character creation.'''
    def __init__(self, bot):
        self.bot = bot
        print('Character Creation Loaded!')

    @commands.command()
    @commands.check(in_start_channel_or_dm)
    async def start(self, ctx):
        '''Used to start character creation.'''
        # if the message is in direct messages we don't delete it as we can't
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.delete()

        if os.path.isfile('data/players/'+str(ctx.author.id)+'.json'): #Check if a user file exists
            #If a user file exists we tell the player they are already playing the game
            await ctx.author.send('What? You can\'t do .start! You already are playing the game!')
        #Check if a temporary user file exists
        elif os.path.isfile('data/players/temporary/'+str(ctx.author.id)+'.json'):
            with open('data/players/temporary/'+str(ctx.author.id)+'.json', 'r') as temp_file: #we load the temporary file to check data
                self.temp_data = json.load(temp_file)
            if self.temp_data['Name'] == None: #If the user hasn't set their name we tell them to
                await ctx.author.send('Well if you are so eager to start please tell me your name?\n\n(Use .setname <name> to set your name.)')
            elif self.temp_data['Backstory'] == None: #If the user hasn't chosen their backstory we tell them to
                await ctx.author.send('Yes... Yes... So which background fits you the most again?\n\n(Use .setstory <number> to set your back story.)')
        else: #If the temporary user file doesn't exists we create it
            self.player = Player(ctx.author.id) #create the player object so we could manipulate player data and create a temporary player data file.
            self.player.create_temp_user_file()
            del self.player
            #send the user a message
            await ctx.author.send('Welcome to the land of Discord & Dragons! Enjoy your stay.\nLet\'s start with your name, shall we?\n\n(Use .setname <name> to set your name.)')

    @commands.command()
    @commands.check(in_start_channel_or_dm)
    async def setname(self, ctx, name=None):
        '''Used to set your name during character creation.'''
        # if the message is in direct messages we don't delete it as we can't
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.delete()

        # Check if a user file exists
        if os.path.isfile('data/players/' + str(ctx.author.id) + '.json'):
            # If a used file exists we tell the player that they can't set their name anymore
            await ctx.author.send('No no no... You can\'t change your name like that!')
            return
        #Check if user provided a name
        if name == None:
            await ctx.author.send('Please provide a name!')
            return

        # Check if a temporary user file exists
        if os.path.isfile('data/players/temporary/' + str(ctx.author.id) + '.json'):
            # we load the temporary file to check data
            with open('data/players/temporary/' + str(ctx.author.id) + '.json', 'r') as temp_file:
                self.temp_data = json.load(temp_file)
            if self.temp_data['Name'] == None: #If the users name isn't set we set it
                #Using the character creation handler we try to set the temporary name which will be used to the final user file.
                creation_handler = CreateCharacter(ctx.author.id)
                message = creation_handler.set_temp_name(name)
                del creation_handler
                await ctx.author.send(message)
                #If the user entered correct name we also post this message (we determine if to posts this checking if the returned message contains the name of the user.
                if ' '+ name +'!' in message:
                    await ctx.author.send(
                    '''
                    \n\n
                    Available backstories:
                    1.You are an inhabitant of this land from a young age
                    you freely took in the newcomers and are ready to protect
                    your homeland with them from the impending doom.
                        Faction: Alliance
                        
                    2.After the attack on your world you were one of the first
                    to flee to a new land and as payback to the people taking
                    you in you deem to protect it from the impending doom.
                        Faction: Alliance
                        
                    3.You are an inhabitant of this land from a young age,
                    after the newcomers came they brought the impending doom with them
                    and you ready to protect your land and get rid away of the newcomers even
                    though you've been cast away by the kind who supports these wretched animals. 
                        Faction: Horde
                        
                    4.You are one of the banished who were banished throufh the great banishing war,
                    although somehow the magic power of the impending doom brought you back
                    and you decided it's time to take back the kingdom from the king that banished
                    you. But at the same time you are ready to protect the world so you get
                    something to claim back.
                        Faction: Horde
                        
                    5..You have no memory of who you are but feel a strong connection
                    with the magic of the world. You are open to exploring the world
                    and finding out who you are. Although when the impending doom came
                    you deemed to protect the world and your secrets with it.
                        Faction: Both
                    '''
                    )
                    await ctx.author.send('\n\n(To set your backstory use .setstory <backstory number>)')
            else: #If the user name is set we change it
                # Using the character creation handler we try to set the temporary name which will be used to the final user file.
                creation_handler = CreateCharacter(ctx.author.id)
                await ctx.author.send(creation_handler.set_temp_name(name))
                del creation_handler
                if self.temp_data['Backstory'] == None: #If the user hasn't set their backstory we tell them to do so
                    await ctx.author.send('\n(Don\'t forget to choose your backstory using .setstory or change your name using .setname)')
                else: #If the user has set their backstory we tell them that they can finish character creation
                    await ctx.author.send('\n(To finish character creation type .ccfinish or you can use .setname or .setstory to change name or backstory)')
        else: #If no file exists for the player.
            await ctx.author.send('Please use .start to start character creation!')

    @commands.command()
    @commands.check(in_start_channel_or_dm)
    async def setstory(self, ctx, story_num=None):
        '''Used to set your backstory during character creation.'''
        # if the message is in direct messages we don't delete it as we can't
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.delete()

        # Check if a user file exists
        if os.path.isfile('data/players/' + str(ctx.author.id) + '.json'):
            # If a user file exists we tell the player that they can't set their backstory anymore
            await ctx.author.send('No no no... You can\'t change your backstory like that!')
            return
        #Check if user provided a backstory number
        if story_num == None:
            await ctx.author.send('Please provide a backstory number!')
            return

        if os.path.isfile('data/players/temporary/' + str(ctx.author.id) + '.json'): # Check if a temporary user file exists
            with open('data/players/temporary/' + str(ctx.author.id) + '.json', 'r') as temp_file: # we load the temporary file to check data
                self.temp_data = json.load(temp_file)
            if self.temp_data['Name'] == None: #If the users name isn't set we tell them to do so
                await ctx.author.send('No no... You see you need to give me your name first!\n\n(To do so use .setname <name>)')
            else: #If the name is set
                if self.temp_data['Backstory'] == None: #If the user doesn't have their back story set we set it
                    creation_handler = CreateCharacter(ctx.author.id)
                    message = creation_handler.set_temp_story(story_num)
                    del creation_handler
                    await ctx.author.send(message)
                    if 'adventure' in message: #If the message is correct it will contain the word adventure. This way we also post another needed message
                        await ctx.author.send('\n\n(To finish character creation do .ccfinish or you can still do .setname and .setbackstory to change name or backstory)')
                else: #Else if their backstory is set we change it
                    creation_handler = CreateCharacter(ctx.author.id)
                    await ctx.author.send(creation_handler.set_temp_story(story_num)+'\n\n(To finish character creation do .ccfinish or you can still do .setname and .setbackstory to change name or backstory)')
                    del creation_handler
        else: # If no file exists for the player.
            await ctx.author.send('Please use .start to start character creation!')

    @commands.command()
    @commands.check(in_start_channel_or_dm)
    async def ccfinish(self, ctx):
        '''Used to finish character creation.'''
        # if the message is in direct messages we don't delete it as we can't
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.delete()

        # Check if a user file exists
        if os.path.isfile('data/players/' + str(ctx.author.id) + '.json'): # If a user file exists we tell the player that they can't set their backstory anymore
            await ctx.author.send('No no no... You already finished making your character!')
        elif os.path.isfile('data/players/temporary/' + str(ctx.author.id) + '.json'): # Check if a temporary user file exists
            with open('data/players/temporary/' + str(ctx.author.id) + '.json', 'r') as temp_file: # we load the temporary file to check data
                self.temp_data = json.load(temp_file)
            if self.temp_data['Name'] == None: # If the user hasn't set their name we tell them to
                await ctx.author.send('Well if you are so eager to start please tell me your name?\n\n(Use .setname <name> to set your name.)')
            elif self.temp_data['Backstory'] == None: # If the user hasn't chosen their backstory we tell them to
                await ctx.author.send('Yes... Yes... So which background fits you the most again?\n\n(Use .setstory <number> to set your back story.)')
            else: #If everything is ok we create an actual user file
                creation_handler = CreateCharacter(ctx.author.id)
                await ctx.author.send(creation_handler.create_user())
                del creation_handler
                #Now we set the player the ranks they need in the server
                self.player = Player(ctx.author.id)
                self.coords = self.player.get_coords()
                del self.player
                self.player_role = discord.utils.get(self.bot.guilds[0].roles, name='Player')
                if self.coords == (0, 0):
                    self.role = discord.utils.get(self.bot.guilds[0].roles, name='City One')
                    for user in self.bot.guilds[0].members:
                        if ctx.author == user:
                            await user.add_roles(self.role, self.player_role)
                elif self.coords == (0, 6):
                    self.role = discord.utils.get(self.bot.guilds[0].roles, name='City Two')
                    for user in self.bot.guilds[0].members:
                        if ctx.author == user:
                            await user.add_roles(self.role, self.player_role)
                elif self.coords == (6, 6):
                    self.role = discord.utils.get(self.bot.guilds[0].roles, name='City Three')
                    for user in self.bot.guilds[0].members:
                        if ctx.author == user:
                            await user.add_roles(self.role, self.player_role)
        else: #If none of those files exist
            await ctx.author.send('Please use .start to start character creation!')


#Used to initialize the bot. Needed for discord.py
def setup(bot):
    bot.add_cog(character_creation(bot))
