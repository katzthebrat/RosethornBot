import discord
from discord import app_commands
from discord.ext import commands
import time
import psutil

PRIMARY_GUILD_ID = 1308904661578813540
HEARTBEAT_CHANNEL_ID = 1394659138591526992
START_TIME = time.time()

EXTENSIONS = [
    "events", "tickets", "twitchwatch", "thorn", "moderation", "application",
    "review_flow", "realm_membership", "help_panel", "rosenotes", "announce"
]

class Rosestatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rosestatus", description="View Rosethorn bot status, uptime, loaded extensions, and sync health")
    @app_commands.guilds(discord.Object(id=PRIMARY_GUILD_ID))
    async def rosestatus(self, interaction: discord.Interaction):
        uptime = int(time.time() - START_TIME)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60

        mem = psutil.Process().memory_info().rss / (1024 * 1024)
        channel = self.bot.get_channel(HEARTBEAT_CHANNEL_ID)
        channel_status = f"📍 <#{HEARTBEAT_CHANNEL_ID}>" if channel else "⚠️ Not Found"

        embed = discord.Embed(
            title="🌸 Rosethorn Status Panel",
            color=discord.Color.from_rgb(113, 20, 23),
            description=f"Rosethorn has been alive for **{hours}h {minutes}m**.\nMemory usage: **{mem:.1f}MB**\nHeartbeat Channel: {channel_status}"
        )
        embed.set_footer(text="Rosethorn Bot | Extension Sync Check")

        for ext in EXTENSIONS:
            if ext in self.bot.extensions:
                cmds = [c.name for c in self.bot.tree.get_commands() if c.module == ext]
                embed.add_field(
                    name=f"✅ {ext}",
                    value=f"{len(cmds)} slash command(s)",
                    inline=True
                )
            else:
                embed.add_field(
                    name=f"❌ {ext}",
                    value="Not loaded",
                    inline=True
                )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Rosestatus(bot))
    print("[Rosethorn] Rosestatus cog loaded.")

    guild = discord.Object(id=PRIMARY_GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
