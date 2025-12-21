import discord
from discord import app_commands
from discord.ext import commands
import datetime

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Shows some info about this bot"
    )
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot info",
            description="Here is some info about Spark (me!)",
            colour=discord.Colour.from_str("#f1b50f"),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(
            name="About me",
            value=f"Spark is a utility bot for the GlitchFork Studios server. My goal is to keep the server managed, safe and enjoyable for all of our members.",
            inline=False
        )

        embed.add_field(
            name="My creator",
            value=f"Spark was created by **OverLack**, the founder of GlitchFork Studios. He also codes, maintains and hosts me all from within his own home.",
            inline=False
        )

        embed.set_footer(
            text=f"{interaction.user.name} ran /{interaction.command.name}",
            icon_url=interaction.user.display_avatar.url
        )

        embed.timestamp = datetime.datetime.now()

        print(f'{interaction.user.name} ran /{interaction.command.name} at 'f'{datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}')
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))