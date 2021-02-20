import discord
from discord.ext import commands

#Not used at all

class NPC:
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar

    async def send_message(self, ctx, dialog, footer=None):
        self.embed = discord.Embed(color=0xffffff)
        self.embed.set_thumbnail(url=self.avatar)
        self.embed.add_field(name=self.name, value=dialog, inline=True)
        await ctx.author.trigger_typing()
        if footer is not None:
            self.embed.set_footer(text=footer)
        await ctx.author.send(embed=self.embed)
