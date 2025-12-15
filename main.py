import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1412370352067055671

intents = discord.Intents.none()
intents.guilds = True

bot = commands.Bot(command_prefix=None, intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    # copy global commands to guild
    bot.tree.copy_global_to(guild=guild)

    # sync to guild
    await bot.tree.sync(guild=guild)

    print(f"Synced commands to guild {GUILD_ID}")
    print(f"Logged in as {bot.user}")

# load all cog files
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())