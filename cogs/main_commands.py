import discord, libraries.main_functions, os, random, json
from discord.ext import commands
from libraries.player_handling import Player
from libraries.fight_handling import Fight

SPECIAL = [(0,0),(0,6),(6,6)]
INACCESSABLE = [(1,0),(5,0),(6,0),(1,1),(3,1),(6,1),(1,3),(4,3),(5,3),(0,4),(3,4),(4,4),(5,4),(1,6),(4,6)]

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class main_commands:
    '''Main commands.'''
    def __init__(self, bot):
        self.bot = bot
        print('Main Commands Loaded!')

    #Command used to send the player a map with their location
    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def map(self, ctx):
        '''Used to display the map and players in the same area.'''
        self.player = Player(ctx.author.id)
        self.player.save_map() #using this we save a map in a specific directory
        self.x, self.y = self.player.get_coords()
        self.players = libraries.main_functions.get_players_in_location(self.x, self.y, ctx.author.id) #using this we also get other players in the same location
        del self.player
        message = '--------------------\nPlayers in your area:\n' #We send all the players in the area
        for player in self.players:
            message += player+'\n'
        file = discord.File('data/players/maps/'+str(ctx.author.id)+'.png') #We load and send the map with tile explanations
        await ctx.author.send(file=file)
        await ctx.author.send(':yellow_heart: - Tile to which you can move to.\n:white_large_square: - Empty tile.\n:green_heart: - Player position.\n:red_circle: - City.')
        await ctx.author.send(message)

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def stats(self, ctx):
        '''Used to display user stats.'''
        await ctx.author.send(libraries.main_functions.display_stats(ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def inventory(self, ctx):
        '''Used to display user inventory.'''
        await ctx.author.send(libraries.main_functions.display_inventory(ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def statsinventory(self, ctx):
        '''Used to display user stats and inventory.'''
        await ctx.author.send(libraries.main_functions.display_stats(ctx.author.id))
        await ctx.author.send('-----------------')
        await ctx.author.send(libraries.main_functions.display_inventory(ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def equipment(self, ctx):
        '''Used to show equipment.'''
        await ctx.author.send(libraries.main_functions.display_equipment(ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def equip(self, ctx, *item_name):
        '''Used to equip an item.'''
        self.item_name = ' '.join(item_name)
        await ctx.author.send(libraries.main_functions.equip_item(self.item_name, ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def unequip(self, ctx, *item_name):
        '''Used to unequip an item.'''
        self.item_name = ' '.join(item_name)
        await ctx.author.send(libraries.main_functions.unequip_item(self.item_name, ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def use(self, ctx, *item_name):
        '''Used to use an item.'''
        self.item_name = ' '.join(item_name)
        await ctx.author.send(libraries.main_functions.use_item(self.item_name, ctx.author.id))

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def move(self, ctx, *coordinates):
        '''Used to move in the world.'''
        if os.path.isfile('data/enemies/' + str(ctx.author.id) + '.json'): #If in a fight user cant move
            await ctx.author.send('Can\'t move while in a fight!')
        elif os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'): #If at a merchant user cant move
            await ctx.author.send('Can\'t move while at a merchant! Do .exitmerchant first')
        else:
            self.player = Player(ctx.author.id)
            if self.player.get_state() == 'Tutorial': #We check if the player is in the tutorial. if they are we tell them they cant move yet
                await ctx.author.send('Arthas: What? Don\'t go anywhere yet!')
                return
            self.player_state = self.player.is_alive()
            del self.player
            if self.player_state: #If player is alive we proceed with moving
                if len(coordinates) == 0: #If the player doesnt provide enough arguments we tell them
                    await ctx.author.send('Pleae provide an X and Y coordinate.')
                elif len(coordinates) == 1:
                    await ctx.author.send('Please provide two coordinates.')
                elif len(coordinates) == 2: #If the player provide the righ amount of arguments x and y in this case
                    int_coordinates = []
                    try: #since the arguments are string we convert them into integers
                        int_coordinates.append(int(coordinates[0]))
                        int_coordinates.append(int(coordinates[1]))
                    except ValueError:
                        await ctx.author.send('Coordinates must be a number.') #if the provided coordinates arent numbers we tell the player so
                        return
                    self.player = Player(ctx.author.id)
                    if self.player.get_coords() == (int_coordinates[0], int_coordinates[1]):
                        await  ctx.author.send('You are already here.')
                        return
                    self.agility = self.player.get_agility()
                    self.x, self.y = self.player.get_coords()
                    del self.player
                    #using this we set the min and max coordinates the player can move to
                    #if it goes out of range we set it in range
                    self.min_x = self.x - self.agility
                    if self.min_x < 0:
                        self.min_x = 0
                    self.max_x = self.x + self.agility
                    if self.max_x > 6:
                        self.max_x = 6
                    self.min_y = self.y - self.agility
                    if self.min_y < 0:
                        self.min_y = 0
                    self.max_y = self.y + self.agility
                    if self.max_y > 6:
                        self.max_y = 6
                    #We check if the player entered good coordinates
                    if self.min_x <= int_coordinates[0] <= self.max_x and self.min_y <= int_coordinates[1] <= self.max_y and (int_coordinates[0], int_coordinates[1]) not in INACCESSABLE:
                        self.fight_chance = random.randrange(0, 101) #using this we check for a random fight chance
                        self.player = Player(ctx.author.id)
                        if self.fight_chance-self.player.get_luck() > 60: #If player gets in a fight we store their wanted coordinates in a temp file
                            self.move_data = {
                                'X': int_coordinates[0],
                                'Y': int_coordinates[1]
                            }
                            with open('data/players/move/' + str(ctx.author.id) + '.json', 'w') as move_file:
                                json.dump(self.move_data, move_file)
                            self.fight = Fight(ctx.author.id)
                            await ctx.author.send(self.fight.initiate_fight()) #And we start a fight
                            del self.fight
                        else: #If the player doesnt get in a fight we change their coordinates
                            self.message = self.player.move(int_coordinates[0], int_coordinates[1])
                            await ctx.author.send(self.message)
                            if self.message == 'Successfully moved!':
                                self.player.save_map()
                                file = discord.File('data/players/maps/' + str(ctx.author.id) + '.png')
                                await ctx.author.send(file=file)
                                await self.update_ranks(ctx, self.player.get_coords())
                    else: #if they didnt enter good coordinates we tell them
                        await ctx.author.send('Wrong coordinates!')
                elif len(coordinates) > 2: #If the player provides too many arguments we tell them its too much
                    await ctx.author.send('Too many arguments!')
            else: #If player is dead we tell they cant move
                await ctx.author.send('Can\'t move while dead. Do .respawn')

    async def update_ranks(self, ctx, coords):
        '''Used to updated the rank of a user depending on their position'''
        # We get the roles from the server
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

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def respawn(self, ctx):
        '''Used to respawn when dead.'''
        if os.path.isfile('data/enemies/' + str(ctx.author.id) + '.json'): #if user in a fight we tell them
            await ctx.author.send('Can\'t respawn while in a fight!')
        elif os.path.isfile('data/merchants/temporary/' + str(ctx.author.id) + '.json'): #If user at a merchant we tell them
            await ctx.author.send('Can\'t respawn while at a merchant!')
        elif os.path.isfile('data/trades/' + str(ctx.author.id) + '.json'): #If user in a trade we tell them
            await ctx.author.send('Can\'t respawn while in a trade!')
        else:
            self.player = Player(ctx.author.id)
            if self.player.is_alive(): #If player is alive we tell them they can't respawn
                await ctx.author.send('Not dead can\'t respawn!')
            else:
                self.player.add_health(100000) #Set the player health a massive amount. The player helath will be set to their possible maximum
                self.death_fee = int(self.player.get_money()*0.075) #Calculate a respawn fee
                self.player.modify_money(-1 * self.death_fee) #deduct the respawn fee
                self.player.reset_position() #Reset the players position to their starting city
                await ctx.author.send('Respawned! It cost you ' + str(self.death_fee) + ' Gold.\nAnd brought you back to your starting position!')
                self.player.save_map() #send the player a map of their new position
                file = discord.File('data/players/maps/' + str(ctx.author.id) + '.png')
                await ctx.author.send(file=file)
                await self.update_ranks(ctx, self.player.get_coords())
            del self.player

def setup(bot):
    bot.add_cog(main_commands(bot))