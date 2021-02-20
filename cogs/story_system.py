import discord
from discord.ext import commands
from libraries.story_handling import Story

#used to check if the command is executed in the channel #bot-commands or direct messages
async def in_bot_commands_or_dm(ctx):
    return ctx.channel.id == 519104699211972640 or isinstance(ctx.channel, discord.DMChannel)

class story_system:
    '''Commands for the story system.'''
    def __init__(self, bot):
        self.bot = bot
        print('Story System Loaded!')

    @commands.command()
    @commands.check(in_bot_commands_or_dm)
    async def story(self, ctx):
        '''Used to progress the story'''
        self.story = Story(ctx.author.id)
        await ctx.author.send(self.story.display_line(self.story.get_story_id()))
        del self.story

def setup(bot):
    bot.add_cog(story_system(bot))
