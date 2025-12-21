import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json
import aiohttp

class Embed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="embed",
        description="Send an embed from a JSON file"
    )
    @app_commands.describe(jsonFile="Valid embed JSON file")
    async def embed(self, interaction: discord.Interaction, jsonFile: discord.Attachment):
        if not interaction.user.get_role(1452102029240565852):
            await interaction.response.send_message(
                "You don't have permission to use this command",
                ephemeral=True
            )
            return

        if not jsonFile.filename.endswith(".json"):
            await interaction.response.send_message(
                "Please upload a valid '.json' file",
                ephemeral=True
            )
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get(jsonFile.url) as resp:
                data = await resp.json()

        if "embeds" not in data:
            await interaction.response.send_message(
                "JSON must contain an 'embeds' array",
                ephemeral=True
            )
            return
        
        embeds = [discord.Embed.from_dict(e) for e in data["embeds"]]

        await interaction.channel.send(
            content=data.get("content"),
            embeds=embeds
        )

        print(f'{interaction.user.name} ran /{interaction.command.name} at 'f'{datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}')
        await interaction.response.send_message(
            "Embed sent!",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Embed(bot))