import discord
from discord import app_commands
from datetime import datetime, timedelta

@app_commands.command(name="realm-launch")
async def realm_launch(interaction: discord.Interaction):
    member = interaction.user

    if member.joined_at is None or (datetime.utcnow() - member.joined_at) < timedelta(weeks=2):
        await interaction.response.send_message(
            "⛔ You must be a member for at least 2 weeks to use this command.",
            ephemeral=True
        )
        return

    await interaction.response.send_message("🚀 Realm launch initialized!", ephemeral=False)
