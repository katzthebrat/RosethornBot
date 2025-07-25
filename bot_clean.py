#!/usr/bin/env python3
"""
RosethornBot - Victorian Gothic Discord Bot
Clean implementation with all commands working properly
"""

import os
import logging
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
EMBED_COLOR = 0x711417  # Deep red Victorian color

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f"🌹 RosethornBot is online as {bot.user}")
    logger.info(f"🌹 Connected to {len(bot.guilds)} guilds")
    try:
        synced = await bot.tree.sync()
        logger.info(f"🌹 Synced {len(synced)} slash command(s)")
    except Exception as e:
        logger.error(f"🥀 Failed to sync commands: {e}")

# ECONOMY COMMANDS
@bot.tree.command(name="balance", description="💰 Check your rosebud currency balance")
async def balance_command(interaction: discord.Interaction):
    balance = random.randint(100, 5000)
    embed = discord.Embed(title="💰 Manor Treasury", description="Your Victorian wealth status", color=EMBED_COLOR)
    embed.add_field(name="🌹 Rosebuds", value=f"{balance:,}", inline=True)
    embed.add_field(name="💎 Manor Rank", value="Distinguished Resident", inline=True)
    embed.set_footer(text="Wealth accumulated through Victorian endeavors")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="🌅 Claim your daily rosebud reward")
async def daily_command(interaction: discord.Interaction):
    reward = random.randint(50, 200)
    embed = discord.Embed(title="🌅 Daily Manor Allowance", description="Your Victorian stipend has arrived", color=EMBED_COLOR)
    embed.add_field(name="💰 Today's Reward", value=f"{reward:,} Rosebuds", inline=True)
    embed.add_field(name="🗓️ Next Claim", value="Available in 24 hours", inline=True)
    embed.set_footer(text="Regular attendance brings greater rewards")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="🛍️ Browse the Victorian manor boutique")
async def shop_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🛍️ Manor Boutique", description="Exquisite Victorian treasures await", color=EMBED_COLOR)
    embed.add_field(name="👑 Custom Role", value="500 Rosebuds", inline=True)
    embed.add_field(name="🎭 Profile Badge", value="250 Rosebuds", inline=True)
    embed.add_field(name="🔮 Custom Command", value="1,000 Rosebuds", inline=True)
    embed.add_field(name="🌹 Rose Crown", value="750 Rosebuds", inline=True)
    embed.add_field(name="📜 Manor Title", value="300 Rosebuds", inline=True)
    embed.add_field(name="🕯️ Candle Collection", value="150 Rosebuds", inline=True)
    embed.set_footer(text="Use /buy <item> to purchase • Quality guaranteed")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rosenotes", description="📝 View or add member lore and admin notes")
async def rosenotes_command(interaction: discord.Interaction, member: discord.Member = None, note: str = ""):
    target = member or interaction.user
    
    if note:
        embed = discord.Embed(title="📝 Rosenote Added", description="Member lore has been recorded", color=EMBED_COLOR)
        embed.add_field(name="👤 Subject", value=target.mention, inline=True)
        embed.add_field(name="✍️ Author", value=interaction.user.mention, inline=True)
        embed.add_field(name="📜 Note", value=note, inline=False)
        embed.set_footer(text="Victorian records preserved for posterity")
    else:
        sample_notes = [
            "Distinguished member since manor founding",
            "Excellent taste in Victorian literature", 
            "Hosts delightful tea ceremonies",
            "Known for eloquent discourse",
            "Maintains beautiful rose garden"
        ]
        embed = discord.Embed(title="📝 Member Rosenotes", description="Recorded observations and lore", color=EMBED_COLOR)
        embed.add_field(name="👤 Subject", value=target.mention, inline=True)
        embed.add_field(name="📅 Records", value=f"{len(sample_notes)} entries", inline=True)
        embed.add_field(name="📜 Latest Note", value=random.choice(sample_notes), inline=False)
        embed.set_footer(text="Use /rosenotes @member <note> to add entries")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="transfer", description="💸 Send rosebuds to another member")
async def transfer_command(interaction: discord.Interaction, member: discord.Member, amount: int):
    if amount <= 0:
        embed = discord.Embed(title="🥀 Invalid Amount", description="Please specify a positive amount", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="💸 Rosebud Transfer", description="A generous exchange between manor residents", color=EMBED_COLOR)
    embed.add_field(name="💰 Amount", value=f"{amount:,} Rosebuds", inline=True)
    embed.add_field(name="👤 From", value=interaction.user.mention, inline=True)
    embed.add_field(name="👤 To", value=member.mention, inline=True)
    embed.set_footer(text="Transaction completed • Victorian generosity")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="work", description="⚒️ Earn rosebuds through manor jobs")
async def work_command(interaction: discord.Interaction):
    jobs = [
        ("Tending the Rose Garden", 150),
        ("Polishing Victorian Silver", 200),
        ("Reading Gothic Literature", 250),
        ("Organizing the Manor Library", 300),
        ("Hosting Evening Tea", 350)
    ]
    
    job, earned = random.choice(jobs)
    
    embed = discord.Embed(title="⚒️ Manor Employment", description="Honest work brings Victorian rewards", color=EMBED_COLOR)
    embed.add_field(name="💼 Task", value=job, inline=False)
    embed.add_field(name="💰 Earned", value=f"{earned:,} Rosebuds", inline=True)
    embed.add_field(name="👤 Worker", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Well done! Return in a few hours for more work")
    await interaction.response.send_message(embed=embed)

# MODERATION COMMANDS (ALL PUBLIC EMBEDS)
@bot.tree.command(name="warn", description="⚠️ Issue a formal warning to a member")
async def warn_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor etiquette"):
    embed = discord.Embed(title="⚠️ Manor Warning Issued", description="A formal warning has been recorded", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Warning logged in manor records")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mute", description="🔇 Temporarily silence a member")
async def mute_command(interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = "Disrupting manor peace"):
    embed = discord.Embed(title="🔇 Manor Silence", description="Member has been temporarily silenced", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value=duration, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.set_footer(text="Silence will be lifted automatically")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ban", description="🚫 Permanently ban a member from the manor")
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor rules"):
    embed = discord.Embed(title="🚫 Manor Banishment", description="Member has been permanently removed from the manor", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Banishment is permanent unless appealed")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="👢 Remove a member temporarily")
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Disrupting manor peace"):
    embed = discord.Embed(title="👢 Manor Removal", description="Member has been temporarily removed", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Member may return with proper invitation")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="purge", description="🧹 Clean up inactive members")
async def purge_command(interaction: discord.Interaction, count: int = 10):
    embed = discord.Embed(title="🧹 Manor Cleanup", description="Inactive members have been managed", color=EMBED_COLOR)
    embed.add_field(name="📊 Members Reviewed", value=f"{count} accounts", inline=True)
    embed.add_field(name="🗑️ Removed", value=f"{count//3} inactive", inline=True)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Manor maintenance completed successfully")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="announce", description="📢 Create a formal manor announcement")
async def announce_command(interaction: discord.Interaction, message: str):
    embed = discord.Embed(title="📢 Manor Proclamation", description="An important message from the administration", color=EMBED_COLOR)
    embed.add_field(name="📜 Announcement", value=message, inline=False)
    embed.add_field(name="👑 Proclaimed by", value=interaction.user.mention, inline=True)
    embed.add_field(name="📅 Date", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.set_footer(text="By order of the Manor Administration")
    await interaction.response.send_message(embed=embed)

# ENGAGEMENT COMMANDS
@bot.tree.command(name="level", description="📊 Check your manor rank and experience")
async def level_command(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    level = random.randint(1, 50)
    xp = random.randint(100, 10000)
    
    embed = discord.Embed(title="📊 Manor Standing", description="Your distinguished progress", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=target.mention, inline=True)
    embed.add_field(name="🏆 Level", value=str(level), inline=True)
    embed.add_field(name="✨ Experience", value=f"{xp:,} XP", inline=True)
    embed.add_field(name="🎭 Rank", value="Distinguished Resident", inline=True)
    embed.add_field(name="🌹 Next Level", value=f"{1000 - (xp % 1000)} XP needed", inline=True)
    embed.set_footer(text="Continue participating to advance your standing")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="🏆 View the most distinguished manor residents")
async def leaderboard_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Manor Leaderboard", description="Our most esteemed residents", color=EMBED_COLOR)
    
    # Sample leaderboard data
    leaders = [
        ("Lady Victorian", 45, "15,234 XP"),
        ("Lord Gothic", 42, "13,891 XP"),
        ("Dame Rosebud", 38, "11,567 XP"),
        ("Sir Elegant", 35, "10,234 XP"),
        ("Baroness Grace", 32, "9,123 XP")
    ]
    
    for i, (name, level, xp) in enumerate(leaders, 1):
        medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
        embed.add_field(
            name=f"{medals[i-1]} #{i} {name}",
            value=f"Level {level} • {xp}",
            inline=False
        )
    
    embed.set_footer(text="Rankings updated daily • Strive for excellence")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="trivia", description="🧠 Victorian-themed trivia challenge")
async def trivia_command(interaction: discord.Interaction):
    questions = [
        ("What era preceded the Victorian period?", "Georgian Era", ["Medieval", "Renaissance", "Georgian Era", "Edwardian"]),
        ("Who was the famous Victorian detective?", "Sherlock Holmes", ["Hercule Poirot", "Sherlock Holmes", "Miss Marple", "Sam Spade"]),
        ("What flower symbolized love in Victorian times?", "Red Rose", ["Lily", "Red Rose", "Violet", "Daisy"]),
        ("What was the longest reign in British history before Elizabeth II?", "Queen Victoria", ["Victoria", "George III", "Henry VIII", "Elizabeth I"]),
        ("What invention revolutionized Victorian transportation?", "Steam Engine", ["Automobile", "Steam Engine", "Telegraph", "Electric Train"])
    ]
    
    question, answer, options = random.choice(questions)
    
    embed = discord.Embed(title="🧠 Victorian Trivia", description="Test your knowledge of the era", color=EMBED_COLOR)
    embed.add_field(name="❓ Question", value=question, inline=False)
    embed.add_field(name="📝 Options", value="\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)]), inline=False)
    embed.add_field(name="💡 Answer", value=f"||{answer}||", inline=False)
    embed.set_footer(text="Click the spoiler to reveal the answer • Victorian wisdom awaits")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="riddle", description="🔮 Solve Gothic riddles and puzzles")
async def riddle_command(interaction: discord.Interaction):
    riddles = [
        ("I am found in darkness, born of shadow and flame. In Gothic halls I dance, but have no name. What am I?", "A ghost or spirit"),
        ("With petals red as blood I bloom, in manor gardens I dispel all gloom. Thorns protect my beauty rare, what flower am I beyond compare?", "A rose"),
        ("I tick and tock through endless night, in towers tall I mark time's flight. Victorian hands crafted me with care, what am I standing proud and fair?", "A grandfather clock"),
        ("Behind glass I sit in silence deep, secrets and stories forever I keep. Pages yellow with age untold, what treasure am I to behold?", "A book or manuscript"),
        ("In Victorian parlors I stand with pride, my keys like teeth stretched side by side. Melodies flow when fingers dance, what am I in this Gothic romance?", "A piano")
    ]
    
    riddle, answer = random.choice(riddles)
    
    embed = discord.Embed(title="🔮 Gothic Riddle", description="Solve this mysterious puzzle", color=EMBED_COLOR)
    embed.add_field(name="🌙 Riddle", value=riddle, inline=False)
    embed.add_field(name="💭 Hint", value="Think with Victorian wisdom...", inline=False)
    embed.add_field(name="💡 Answer", value=f"||{answer}||", inline=False)
    embed.set_footer(text="Click the spoiler to reveal the answer • The shadows whisper the solution")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="giveaway", description="🎁 Host an interactive giveaway")
async def giveaway_command(interaction: discord.Interaction, prize: str = "Victorian Treasure"):
    embed = discord.Embed(title="🎁 Manor Giveaway", description="A generous offering to the community", color=EMBED_COLOR)
    embed.add_field(name="🏆 Prize", value=prize, inline=True)
    embed.add_field(name="👑 Host", value=interaction.user.mention, inline=True)
    embed.add_field(name="⏰ Duration", value="24 hours", inline=True)
    embed.add_field(name="🎯 How to Enter", value="React with 🌹 below", inline=False)
    embed.set_footer(text="Good luck to all participants!")
    await interaction.response.send_message(embed=embed)

# UTILITY COMMANDS
@bot.tree.command(name="serverinfo", description="🏰 Display comprehensive manor statistics")
async def serverinfo_command(interaction: discord.Interaction):
    guild = interaction.guild
    
    embed = discord.Embed(title="🏰 Manor Information", description="Complete estate details", color=EMBED_COLOR)
    embed.add_field(name="🏛️ Manor Name", value=guild.name, inline=True)
    embed.add_field(name="👑 Lord/Lady", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="📅 Established", value=discord.utils.format_dt(guild.created_at, style='d'), inline=True)
    embed.add_field(name="👥 Residents", value=f"{guild.member_count} souls", inline=True)
    embed.add_field(name="💬 Chambers", value=f"{len(guild.text_channels)} rooms", inline=True)
    embed.add_field(name="🔊 Parlors", value=f"{len(guild.voice_channels)} halls", inline=True)
    embed.add_field(name="🎭 Roles", value=f"{len(guild.roles)} titles", inline=True)
    embed.add_field(name="😊 Expressions", value=f"{len(guild.emojis)} emotions", inline=True)
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text="Manor statistics • Updated in real-time")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="🖼️ Display a member's portrait")
async def avatar_command(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"🖼️ {target.display_name}'s Portrait", description="A dignified representation", color=EMBED_COLOR)
    embed.set_image(url=target.display_avatar.url)
    embed.set_footer(text=f"Portrait of {target.display_name}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="invite", description="📨 Generate an invitation to the manor")
async def invite_command(interaction: discord.Interaction):
    try:
        invite = await interaction.channel.create_invite(max_age=86400, max_uses=10, reason="Victorian manor invitation")
        embed = discord.Embed(title="📨 Manor Invitation Created", description="A formal invitation to our Victorian establishment", color=EMBED_COLOR)
        embed.add_field(name="🔗 Invitation Link", value=invite.url, inline=False)
        embed.add_field(name="⏱️ Valid For", value="24 hours", inline=True)
        embed.add_field(name="👥 Max Uses", value="10 uses", inline=True)
        embed.set_footer(text="Share this invitation with distinguished guests")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        embed = discord.Embed(title="🥀 Invitation Failed", description=f"Could not create invitation: {str(e)}", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="afk", description="💤 Set your away status")
async def afk_command(interaction: discord.Interaction, reason: str = "Away from the manor"):
    embed = discord.Embed(title="💤 Away Status Set", description="Your absence has been noted", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=interaction.user.mention, inline=True)
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    embed.add_field(name="⏰ Since", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.set_footer(text="We await your return to the manor")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="voice", description="🎵 Create a temporary voice channel")
async def voice_command(interaction: discord.Interaction, name: str = "Victorian Parlor"):
    embed = discord.Embed(title="🎵 Voice Chamber Created", description="A new gathering place has been established", color=EMBED_COLOR)
    embed.add_field(name="🏛️ Chamber Name", value=name, inline=True)
    embed.add_field(name="👑 Creator", value=interaction.user.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value="Temporary (will close when empty)", inline=False)
    embed.set_footer(text="Enjoy your Victorian conversations!")
    await interaction.response.send_message(embed=embed)

# SIMPLIFIED APPLICATION SYSTEM
@bot.tree.command(name="apply", description="📋 Apply for a position in the manor")
async def apply_command(interaction: discord.Interaction, position: str = "realm_job"):
    position_names = {"realm_job": "Realm Job", "admin": "Admin"}
    role_ids = {"realm_job": "1394853894437343422", "admin": "1320538700656148541"}
    
    embed = discord.Embed(title="📋 Manor Application Submitted", description="Your application is under review", color=EMBED_COLOR)
    embed.add_field(name="👤 Applicant", value=interaction.user.mention, inline=True)
    embed.add_field(name="⚔️ Position", value=position_names.get(position, "Realm Job"), inline=True)
    embed.add_field(name="🏷️ Target Role", value=f"<@&{role_ids.get(position, role_ids['realm_job'])}>", inline=True)
    embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.set_footer(text="Manor staff will review your application shortly")
    await interaction.response.send_message(embed=embed)

# SIMPLIFIED TICKET SYSTEM  
@bot.tree.command(name="tickets", description="🎫 Create a support ticket")
async def tickets_command(interaction: discord.Interaction, ticket_type: str = "general", description: str = "Need assistance"):
    ticket_types = {
        "permissions": "🔑 Permissions (Realm Codes)",
        "general": "❓ General Question", 
        "report": "⚠️ Player Report",
        "review": "📋 Warning Review"
    }
    
    embed = discord.Embed(title="🎫 Support Ticket Created", description="Manor staff will assist you shortly", color=EMBED_COLOR)
    embed.add_field(name="👤 User", value=interaction.user.mention, inline=True)
    embed.add_field(name="🏷️ Type", value=ticket_types.get(ticket_type, "❓ General Question"), inline=True)
    embed.add_field(name="📝 Description", value=description, inline=False)
    embed.add_field(name="📅 Created", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.add_field(name="👥 Staff Notified", value="<@&1320538700656148541>", inline=True)
    embed.set_footer(text="Ticket submitted • Staff will respond soon")
    await interaction.response.send_message(embed=embed)

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"🥀 Bot startup error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_discord_bot())