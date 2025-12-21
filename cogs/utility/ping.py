import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check if the bot is alive"
    )
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Pong!",
            description="Bot is online and responding",
            colour=discord.Colour.from_str("#f1b50f"),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(
            name="Latency",
            value=f"{round(self.bot.latency * 1000)} ms"
        )

        embed.set_footer(
            text=f"{interaction.user.name} ran /{interaction.command.name}",
            icon_url=interaction.user.display_avatar.url
        )

        print(f'{interaction.user.name} ran /{interaction.command.name} at 'f'{datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}')
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))