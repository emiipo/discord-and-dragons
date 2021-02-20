import discord, os
from discord.ext import commands

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class admin_system:
    '''Commands for fights'''
    def __init__(self, bot):
        self.bot = bot
        print('Administration System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def update_player_files(self, ctx, *item_name):
        yield

def setup(bot):
    bot.add_cog(admin_system(bot))