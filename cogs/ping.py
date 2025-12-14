import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Check if the bot is alive")
    async def ping(self, ctx):
        await ctx.respond("Pong!")

def setup(bot):
    bot.add_cog(Ping(bot))