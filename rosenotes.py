import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

STAFF_ROLE_ID = 1308905911489921124
JSON_PATH = "rosenotes.json"
PRIMARY_GUILD_ID = 1308904661578813540

def load_notes():
    if not os.path.exists(JSON_PATH):
        with open(JSON_PATH, "w") as f:
            json.dump({}, f)
    try:
        with open(JSON_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_notes(notes):
    with open(JSON_PATH, "w") as f:
        json.dump(notes, f, indent=4)

class Rosenotes(commands.GroupCog, name="rosenotes"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    def has_staff_role(self, interaction: discord.Interaction):
        return any(role.id == STAFF_ROLE_ID for role in interaction.user.roles)

    @app_commands.command(name="add")
    async def add_note(self, interaction: discord.Interaction, member: discord.Member, note: str, tags: str = ""):
        if not self.has_staff_role(interaction):
            return await interaction.response.send_message("You lack the scrollkeeper’s seal.", ephemeral=True)

        notes = load_notes()
        user_id = str(member.id)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = {
            "author": interaction.user.name,
            "timestamp": now,
            "note": note,
            "tags": tags.split(),
        }

        notes.setdefault(user_id, []).append(entry)
        save_notes(notes)
        await interaction.response.send_message(f"Note added to **{member.display_name}**'s scroll.", ephemeral=True)

    @app_commands.command(name="view")
    async def view_notes(self, interaction: discord.Interaction, member: discord.Member):
        if not self.has_staff_role(interaction):
            return await interaction.response.send_message("Access denied to Rosethorn’s archives.", ephemeral=True)

        notes = load_notes()
        user_id = str(member.id)
        entries = notes.get(user_id)

        if not entries:
            return await interaction.response.send_message("This soul bears no record.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        for i, entry in enumerate(entries):
            desc = f"**Note {i+1}:** {entry['note']}"
            if entry.get("edited_by"):
                desc += f"\n*Edited by {entry['edited_by']} on {entry['edited_at']}*"
            embed = discord.Embed(
                title=f"🪶 {member.display_name} — Lore Note {i+1}",
                description=desc,
                color=discord.Color.gold()
            )
            embed.set_footer(text=f"Written by {entry['author']} • {entry['timestamp']}")
            embed.add_field(name="Tags", value=" ".join(entry.get("tags", [])) or "None", inline=False)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="edit")
    async def edit_note(self, interaction: discord.Interaction, member: discord.Member, index: int, new_note: str, new_tags: str = ""):
        if not self.has_staff_role(interaction):
            return await interaction.response.send_message("You hold no quill of amendment.", ephemeral=True)

        notes = load_notes()
        user_id = str(member.id)
        entries = notes.get(user_id)

        if not entries or index >= len(entries):
            return await interaction.response.send_message("Note index is invalid.", ephemeral=True)

        entries[index]["note"] = new_note
        entries[index]["tags"] = new_tags.split()
        entries[index]["edited_by"] = interaction.user.name
        entries[index]["edited_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        save_notes(notes)
        await interaction.response.send_message(f"Note {index+1} for **{member.display_name}** has been updated.", ephemeral=True)

    @app_commands.command(name="clear")
    async def clear_notes(self, interaction: discord.Interaction, member: discord.Member):
        if not self.has_staff_role(interaction):
            return await interaction.response.send_message("This spell is not yours to cast.", ephemeral=True)

        notes = load_notes()
        user_id = str(member.id)

        if user_id not in notes or not notes[user_id]:
            return await interaction.response.send_message("There are no scrolls to burn.", ephemeral=True)

        notes[user_id] = []
        save_notes(notes)
        await interaction.response.send_message(f"All notes for **{member.display_name}** have been cleared.", ephemeral=True)

    @app_commands.command(name="search")
    async def search_notes(self, interaction: discord.Interaction, keyword: str = "", tag: str = "", author: str = ""):
        if not self.has_staff_role(interaction):
            return await interaction.response.send_message("You lack the archivist’s eye.", ephemeral=True)

        notes = load_notes()
        found = []

        for uid, entries in notes.items():
            for i, entry in enumerate(entries):
                if (
                    (keyword.lower() in entry["note"].lower()) and
                    (not tag or tag in entry.get("tags", [])) and
                    (not author or author.lower() == entry["author"].lower())
                ):
                    found.append((uid, i, entry))

        if not found:
            return await interaction.response.send_message("No entries match your query.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        for uid, i, entry in found:
            embed = discord.Embed(
                title=f"📜 User ID: {uid} — Match {i+1}",
                description=entry["note"],
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"By {entry['author']} • {entry['timestamp']}")
            embed.add_field(name="Tags", value=" ".join(entry.get("tags", [])) or "None", inline=False)
            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    cog = Rosenotes(bot)
    await bot.add_cog(cog)

    # 🔒 Instant Guild Sync
    GUILD = discord.Object(id=PRIMARY_GUILD_ID)
    bot.tree.copy_global_to(guild=GUILD)
    await bot.tree.sync(guild=GUILD)
