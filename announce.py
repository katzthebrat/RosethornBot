# announce.py
import discord
from discord import app_commands
from discord.ext import commands

STAFF_ROLE_ID = 1308905911489921124
PRIMARY_GUILD_ID = 1308904661578813540  # Replace with your guild ID

class Announce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send a styled announcement to a selected channel with optional image")
    @app_commands.describe(
        title="Title of the announcement",
        message="Main message content",
        channel="Channel to send the announcement",
        image_url="Optional image to include in the embed"
    )
    async def announce(self, interaction: discord.Interaction, title: str, message: str, channel: discord.TextChannel, image_url: str = ""):
        # Role check
        if not any(role.id == STAFF_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("You lack heraldic permissions.", ephemeral=True)

        # Build embed
        embed = discord.Embed(
            title=title,
            description=message,
            color=discord.Color.from_rgb(113, 20, 23)  # #711417
        )
        embed.set_footer(text="Rosethorn Announcement")
        embed.timestamp = discord.utils.utcnow()

        if image_url:
            embed.set_image(url=image_url)

        # Send to selected channel
        await channel.send(embed=embed)

        # Confirm quietly
        await interaction.response.send_message(f"📣 Announced in {channel.mention}.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Announce(bot))

    # 🔒 Guild-only sync to avoid duplicates
    GUILD = discord.Object(id=PRIMARY_GUILD_ID)
    bot.tree.copy_global_to(guild=GUILD)
    await bot.tree.sync(guild=GUILD)
