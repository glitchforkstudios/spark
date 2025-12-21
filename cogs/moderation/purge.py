import discord
from discord import app_commands
from discord.ext import commands
import datetime
import io

LOG_CHANNEL_ID = 1450883211499409481

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="purge",
        description="Purge messages in the channel the command is used in"
    )
    @app_commands.describe(amount="Number of messages to check (max 100)")
    async def purge_all(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        # permission check
        if not interaction.user.get_role(1452102029240565852):
            await interaction.response.send_message(
                "You don't have permission to use this command",
                ephemeral=True
            )
            return
        
        channel = interaction.channel
        logChannel = interaction.guild.get_channel(LOG_CHANNEL_ID)

        if logChannel is None:
            await interaction.response.send_message(
                "Log channel not found",
                ephemeral=True
            )
            return
        
        messages = []
        logLines = []

        async for message in channel.history(limit=amount):
            messages.append(message)

            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            author = f"{message.author} ({message.author.id})"
            content = message.content or "[No text content]"

            logLines.append(
                f"[{timestamp}] {author}\n{content}\n"
            )

        if not messages:
            await interaction.response.send_message(
                "No messages found to delete",
                ephemeral=True
            )
            return
        
        # delete messages
        await channel.delete_messages(messages)

        # create log file in memory
        logText = "\n".join(logLines)
        logFile = io.BytesIO(logText.encode("utf-8"))
        logFile.seek(0)

        file = discord.File(
            fp=logFile,
            filename=f"purge-log_{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
        )

        # log embed
        embed = discord.Embed(
            title="Purge executed",
            colour=discord.Colour.from_str("#f1b50f"),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention,
            inline=True
        )
        embed.add_field(
            name="Channel",
            value=channel.mention,
            inline=True
        )

        embed.set_footer(
            text=f"{interaction.user.name} ran /{interaction.command.name}",
            icon_url=interaction.user.display_avatar.url
        )

        # send log
        await logChannel.send(embed=embed, file=file)

        # confirm to moderator
        await interaction.response.send_message(
            f"Deleted {len(messages)} messages",
            ephemeral=True
        )
            

async def setup(bot: commands.Bot):
    await bot.add_cog(Purge(bot))