import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
import asyncio

INFRACTIONS_FILE = "infractions.json"
MUTE_ROLE_NAME = "Muted"
GUILD_ID = 1308904661578813540  # 👈 Your server

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def log_infraction(self, user_id, moderator, reason):
        data = {}
        if os.path.exists(INFRACTIONS_FILE):
            with open(INFRACTIONS_FILE, "r") as f:
                data = json.load(f)

        data.setdefault(str(user_id), []).append({
            "moderator": moderator,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })

        with open(INFRACTIONS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    @app_commands.command(name="warn", description="Issue a warning to a member")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        self.log_infraction(member.id, interaction.user.name, reason)
        await interaction.response.send_message(f"⚠️ `{member.display_name}` warned.\nReason: {reason}", ephemeral=True)

    @app_commands.command(name="infractions", description="View a member’s warning history")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(kick_members=True)
    async def infractions(self, interaction: discord.Interaction, member: discord.Member):
        if not os.path.exists(INFRACTIONS_FILE):
            await interaction.response.send_message("📜 No infractions found.", ephemeral=True)
            return

        with open(INFRACTIONS_FILE, "r") as f:
            data = json.load(f)

        entries = data.get(str(member.id), [])
        if not entries:
            await interaction.response.send_message(f"`{member.display_name}` has no infractions.", ephemeral=True)
            return

        embed = discord.Embed(title=f"📜 Infractions for {member.display_name}", color=discord.Color.orange())
        for i, entry in enumerate(entries, 1):
            embed.add_field(
                name=f"Warning {i}",
                value=f"**By:** {entry['moderator']}\n**Reason:** {entry['reason']}\n**Date:** {entry['timestamp']}",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"🥾 `{member.display_name}` was kicked.\nReason: {reason}", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 `{member.display_name}` was banned.\nReason: {reason}", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a previously banned user")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"♻️ `{user.name}` has been unbanned.", ephemeral=True)

    @app_commands.command(name="purge", description="Delete recent messages")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True)

    @app_commands.command(name="mute", description="Mute a member (adds Muted role)")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration_minutes: int = None):
        role = discord.utils.get(interaction.guild.roles, name=MUTE_ROLE_NAME)
        if not role:
            role = await interaction.guild.create_role(name=MUTE_ROLE_NAME)
            for channel in interaction.guild.channels:
                await channel.set_permissions(role, send_messages=False, speak=False)

        await member.add_roles(role)
        await interaction.response.send_message(f"🔇 `{member.display_name}` has been muted.", ephemeral=True)

        if duration_minutes:
            await asyncio.sleep(duration_minutes * 60)
            await member.remove_roles(role)
            await interaction.followup.send(f"🔈 `{member.display_name}` unmuted after {duration_minutes}m.", ephemeral=True)

    @app_commands.command(name="unmute", description="Remove mute role from a member")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        role = discord.utils.get(interaction.guild.roles, name=MUTE_ROLE_NAME)
        if role and role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"🔈 `{member.display_name}` has been unmuted.", ephemeral=True)
        else:
            await interaction.response.send_message(f"ℹ️ `{member.display_name}` is not muted.", ephemeral=True)

    @app_commands.command(name="userinfo", description="Get info about a member")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(
            title=f"🧾 Info for {member.display_name}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Joined", value=f"<t:{int(member.joined_at.timestamp())}:F>", inline=False)
        embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles if r.name != "@everyone"]) or "None", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="remindrules", description="DM a member with the server rules")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def remindrules(self, interaction: discord.Interaction, member: discord.Member):
        try:
            await member.send("📜 Please remember to follow the server rules. Let me know if you need help.")
            await interaction.response.send_message(f"📨 Reminded `{member.display_name}` in DMs.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ Couldn’t DM `{member.display_name}`.", ephemeral=True)

async def setup_moderation(bot):
    await bot.add_cog(Moderation(bot))
    print("[Rosethorn] Moderation cog loaded.")
