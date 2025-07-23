import discord
from discord import app_commands
from discord.ext import commands

PRIMARY_GUILD_ID = 1308904661578813540  # 🌿 Ensure this matches your main bot config

class HelpPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="commands",
        description="Display all Rosethorn slash commands and their descriptions"
    )
    @app_commands.guilds(discord.Object(id=PRIMARY_GUILD_ID))  # 🪄 Instant guild-sync
    async def list_commands(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)  # 👈 Prevent Discord timeout

        guild = interaction.guild
        embed = discord.Embed(
            title="📜 Rosethorn Command Index",
            description="Below are the slash commands currently available in this realm:",
            color=discord.Color.from_rgb(113, 20, 23)
        )

        # 🌿 Includes commands scoped to this guild only
        guild_commands = await self.bot.tree.fetch_commands(guild=guild)

        for cmd in guild_commands:
            embed.add_field(
                name=f"/{cmd.name}",
                value=cmd.description or "*No description provided.*",
                inline=False
            )

        embed.set_footer(text="Rosethorn Bot | Command Reference")
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpPanel(bot))
