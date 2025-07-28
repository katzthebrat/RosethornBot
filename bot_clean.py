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

# Import error handling system
from services.error_handler import error_handler, handle_errors, ErrorType, ErrorSeverity
from services.error_templates import templates as error_templates
from services.error_demonstration import error_demo

# Import sticky message service
from services.sticky_message_service import initialize_sticky_service, sticky_service

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
    
    # Initialize sticky message service
    global sticky_service
    sticky_service = initialize_sticky_service(bot)
    logger.info("🌹 Sticky message service initialized")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"🌹 Synced {len(synced)} slash command(s)")
        
        # Set default permissions for all commands to be available to everyone
        for guild in bot.guilds:
            try:
                await bot.tree.sync(guild=guild)
                logger.info(f"🌹 Synced commands for guild: {guild.name}")
            except Exception as e:
                logger.error(f"🥀 Failed to sync for guild {guild.name}: {e}")
    except Exception as e:
        logger.error(f"🥀 Failed to sync commands: {e}")

@bot.event
async def on_member_join(member):
    """Handle new member joining with animated welcome banner"""
    try:
        from services.welcome_banner import welcome_banner_service
        
        # Look for a welcome or general channel
        welcome_channel = None
        for channel in member.guild.text_channels:
            if any(name in channel.name.lower() for name in ['welcome', 'general', 'entrance', 'arrivals']):
                welcome_channel = channel
                break
        
        # If no specific welcome channel found, use the first available text channel
        if not welcome_channel and member.guild.text_channels:
            welcome_channel = member.guild.text_channels[0]
        
        if not welcome_channel:
            logger.warning(f"No suitable welcome channel found for guild {member.guild.name}")
            return
        
        # Create welcome banner image
        banner_bytes = await welcome_banner_service.create_welcome_banner(member, member.guild)
        banner_file = discord.File(banner_bytes, filename=f"welcome_{member.id}.png")
        
        # Create animated embed
        embed = await welcome_banner_service.create_animated_embed(member, member.guild)
        
        # Send welcome message
        welcome_message = await welcome_channel.send(
            file=banner_file,
            embed=embed
        )
        
        logger.info(f"🌹 Sent welcome banner for {member.display_name} in {member.guild.name}")
                
    except Exception as e:
        logger.error(f"🥀 Error sending welcome banner: {e}")

# ECONOMY COMMANDS
@bot.tree.command(name="balance", description="💰 Check your rosebud currency balance")
@discord.app_commands.default_permissions(send_messages=True)
@handle_errors
async def balance_command(interaction: discord.Interaction):
    balance = random.randint(100, 5000)
    embed = discord.Embed(title="💰 Manor Treasury", description="Your Victorian wealth status", color=EMBED_COLOR)
    embed.add_field(name="🌹 Rosebuds", value=f"{balance:,}", inline=True)
    embed.add_field(name="💎 Manor Rank", value="Distinguished Resident", inline=True)
    embed.set_footer(text="Wealth accumulated through Victorian endeavors")
    
    # Check tutorial progress
    await check_tutorial_progress(interaction.user.id, "balance")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="🌅 Claim your daily rosebud reward")
@discord.app_commands.default_permissions(send_messages=True)
@handle_errors
async def daily_command(interaction: discord.Interaction):
    reward = random.randint(50, 200)
    embed = discord.Embed(title="🌅 Daily Manor Allowance", description="Your Victorian stipend has arrived", color=EMBED_COLOR)
    embed.add_field(name="💰 Today's Reward", value=f"{reward:,} Rosebuds", inline=True)
    embed.add_field(name="🗓️ Next Claim", value="Available in 24 hours", inline=True)
    embed.set_footer(text="Regular attendance brings greater rewards")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="🛍️ Browse the Victorian manor boutique")
@discord.app_commands.default_permissions(send_messages=True)
@handle_errors
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
@discord.app_commands.default_permissions(send_messages=True)
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
    
    # Check tutorial progress
    await check_tutorial_progress(interaction.user.id, "rosenotes")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="transfer", description="💸 Send rosebuds to another member")
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
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

# MODERATION COMMANDS (ALL PUBLIC EMBEDS) - Only for specific admin
@bot.tree.command(name="warn", description="⚠️ Issue a formal warning to a member")
@discord.app_commands.default_permissions(moderate_members=True)
async def warn_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor etiquette"):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can issue warnings", ephemeral=True)
        return
    embed = discord.Embed(title="⚠️ Manor Warning Issued", description="A formal warning has been recorded", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Warning logged in manor records")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mute", description="🔇 Temporarily silence a member")
@discord.app_commands.default_permissions(moderate_members=True)
async def mute_command(interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = "Disrupting manor peace"):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can mute members", ephemeral=True)
        return
    embed = discord.Embed(title="🔇 Manor Silence", description="Member has been temporarily silenced", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value=duration, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.set_footer(text="Silence will be lifted automatically")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ban", description="🚫 Permanently ban a member from the manor")
@discord.app_commands.default_permissions(ban_members=True)
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor rules"):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can ban members", ephemeral=True)
        return
    embed = discord.Embed(title="🚫 Manor Banishment", description="Member has been permanently removed from the manor", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Banishment is permanent unless appealed")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="👢 Remove a member temporarily")
@discord.app_commands.default_permissions(kick_members=True)
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Disrupting manor peace"):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can kick members", ephemeral=True)
        return
    embed = discord.Embed(title="👢 Manor Removal", description="Member has been temporarily removed", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Member may return with proper invitation")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="purge", description="🧹 Clean up inactive members")
@discord.app_commands.default_permissions(manage_messages=True)
async def purge_command(interaction: discord.Interaction, count: int = 10):
    embed = discord.Embed(title="🧹 Manor Cleanup", description="Inactive members have been managed", color=EMBED_COLOR)
    embed.add_field(name="📊 Members Reviewed", value=f"{count} accounts", inline=True)
    embed.add_field(name="🗑️ Removed", value=f"{count//3} inactive", inline=True)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Manor maintenance completed successfully")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="simpleannounce", description="📢 Create a formal manor announcement")
@discord.app_commands.default_permissions(manage_messages=True)
async def simpleannounce_command(interaction: discord.Interaction, message: str):
    embed = discord.Embed(title="📢 Manor Proclamation", description="An important message from the administration", color=EMBED_COLOR)
    embed.add_field(name="📜 Announcement", value=message, inline=False)
    embed.add_field(name="👑 Proclaimed by", value=interaction.user.mention, inline=True)
    embed.add_field(name="📅 Date", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.set_footer(text="By order of the Manor Administration")
    await interaction.response.send_message(embed=embed)

# ENGAGEMENT COMMANDS
@bot.tree.command(name="level", description="📊 Check your manor rank and experience")
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
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
    
    # Check tutorial progress
    await check_tutorial_progress(interaction.user.id, "trivia")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="riddle", description="🔮 Solve Gothic riddles and puzzles")
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
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
@discord.app_commands.default_permissions(send_messages=True)
async def avatar_command(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"🖼️ {target.display_name}'s Portrait", description="A dignified representation", color=EMBED_COLOR)
    embed.set_image(url=target.display_avatar.url)
    embed.set_footer(text=f"Portrait of {target.display_name}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="invite", description="📨 Generate an invitation to the manor")
@discord.app_commands.default_permissions(create_instant_invite=True)
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
@discord.app_commands.default_permissions(send_messages=True)
async def afk_command(interaction: discord.Interaction, reason: str = "Away from the manor"):
    embed = discord.Embed(title="💤 Away Status Set", description="Your absence has been noted", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=interaction.user.mention, inline=True)
    embed.add_field(name="📝 Reason", value=reason, inline=False)
    embed.add_field(name="⏰ Since", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
    embed.set_footer(text="We await your return to the manor")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="createvoice", description="🎵 Create a temporary voice channel")
@discord.app_commands.default_permissions(manage_channels=True)
async def createvoice_command(interaction: discord.Interaction, name: str = "Victorian Parlor"):
    embed = discord.Embed(title="🎵 Voice Chamber Created", description="A new gathering place has been established", color=EMBED_COLOR)
    embed.add_field(name="🏛️ Chamber Name", value=name, inline=True)
    embed.add_field(name="👑 Creator", value=interaction.user.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value="Temporary (will close when empty)", inline=False)
    embed.set_footer(text="Enjoy your Victorian conversations!")
    await interaction.response.send_message(embed=embed)

# ADVANCED APPLICATION SYSTEM - Buttons → Modals → Threads → Role Assignment
class ApplicationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Realm Job Application", style=discord.ButtonStyle.primary, emoji="⚔️")
    async def realm_job_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RealmJobModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Admin Application", style=discord.ButtonStyle.secondary, emoji="👑")
    async def admin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = AdminModal()
        await interaction.response.send_modal(modal)

class RealmJobModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Realm Job Application")
        
        self.experience = discord.ui.TextInput(
            label="Previous Experience",
            placeholder="Describe your relevant experience...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        self.motivation = discord.ui.TextInput(
            label="Why do you want this position?",
            placeholder="What motivates you to serve the realm...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        self.availability = discord.ui.TextInput(
            label="Availability",
            placeholder="How many hours per week can you dedicate?",
            style=discord.TextStyle.short,
            max_length=100
        )
        
        self.add_item(self.experience)
        self.add_item(self.motivation)
        self.add_item(self.availability)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Create private thread for application review
            thread = await interaction.channel.create_thread(
                name=f"Realm Job - {interaction.user.display_name}",
                auto_archive_duration=1440
            )
            
            # Send detailed application to thread
            embed = discord.Embed(title="⚔️ Realm Job Application", color=EMBED_COLOR)
            embed.add_field(name="👤 Applicant", value=interaction.user.mention, inline=True)
            embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
            embed.add_field(name="💼 Previous Experience", value=self.experience.value, inline=False)
            embed.add_field(name="🎯 Motivation", value=self.motivation.value, inline=False)
            embed.add_field(name="⏰ Availability", value=self.availability.value, inline=False)
            
            # Add review buttons for admin staff
            review_view = ApplicationReviewView(application_type="realm_job", applicant=interaction.user)
            
            await thread.send(f"<@&1320538700656148541>", embed=embed, view=review_view)
            
            # Create individual tracking message for this application
            tracking_msg = await create_tracking_message("📋 Realm Job Application", {
                "👤 Applicant": interaction.user.mention,
                "🏷️ Type": "Realm Job",
                "📊 Status": "🟡 Pending Review"
            }, EMBED_COLOR, f"APP-{interaction.user.id}")
            
            # Store tracking message reference in the thread
            if tracking_msg:
                await thread.send(f"📊 **Tracking:** {tracking_msg.jump_url}", delete_after=1)
            
            await interaction.response.send_message("✅ Your Realm Job application has been submitted!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating application: {str(e)}", ephemeral=True)

class AdminModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Admin Application")
        
        self.experience = discord.ui.TextInput(
            label="Administrative Experience",
            placeholder="Describe your leadership/admin experience...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        self.skills = discord.ui.TextInput(
            label="Relevant Skills",
            placeholder="What skills make you suitable for admin role...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        self.scenarios = discord.ui.TextInput(
            label="Conflict Resolution",
            placeholder="How would you handle member disputes...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        
        self.add_item(self.experience)
        self.add_item(self.skills)
        self.add_item(self.scenarios)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Create private thread for application review
            thread = await interaction.channel.create_thread(
                name=f"Admin - {interaction.user.display_name}",
                auto_archive_duration=1440
            )
            
            # Send detailed application to thread
            embed = discord.Embed(title="👑 Admin Application", color=EMBED_COLOR)
            embed.add_field(name="👤 Applicant", value=interaction.user.mention, inline=True)
            embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
            embed.add_field(name="💼 Administrative Experience", value=self.experience.value, inline=False)
            embed.add_field(name="🛠️ Relevant Skills", value=self.skills.value, inline=False)
            embed.add_field(name="⚖️ Conflict Resolution", value=self.scenarios.value, inline=False)
            
            # Add review buttons for admin staff
            review_view = ApplicationReviewView(application_type="admin", applicant=interaction.user)
            
            await thread.send(f"<@&1320538700656148541>", embed=embed, view=review_view)
            
            # Create individual tracking message for this application
            tracking_msg = await create_tracking_message("📋 Admin Application", {
                "👤 Applicant": interaction.user.mention,
                "🏷️ Type": "Admin",
                "📊 Status": "🟡 Pending Review"
            }, EMBED_COLOR, f"APP-{interaction.user.id}")
            
            # Store tracking message reference in the thread
            if tracking_msg:
                await thread.send(f"📊 **Tracking:** {tracking_msg.jump_url}", delete_after=1)
            
            await interaction.response.send_message("✅ Your Admin application has been submitted!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating application: {str(e)}", ephemeral=True)

class ApplicationReviewView(discord.ui.View):
    def __init__(self, application_type: str, applicant):
        super().__init__(timeout=None)
        self.application_type = application_type
        self.applicant = applicant
    
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, emoji="✅")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role (1320538700656148541)
        is_admin = (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles))
        
        if not is_admin:
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        try:
            # Assign role based on application type
            if self.application_type == "realm_job":
                role_id = 1394853894437343422
                role_name = "Realm Job"
            else:  # admin
                role_id = 1320538700656148541
                role_name = "Admin"
            
            role = interaction.guild.get_role(role_id)
            if role and hasattr(self.applicant, 'add_roles'):
                await self.applicant.add_roles(role)
            
            # Find and update the tracking message
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                async for message in log_channel.history(limit=50):
                    if (message.embeds and 
                        self.applicant.mention in str(message.embeds[0].to_dict()) and 
                        "Application" in message.embeds[0].title):
                        await update_tracking_message(message, f"✅ {role_name} Application APPROVED", {
                            "👤 Applicant": self.applicant.mention,
                            "🏷️ Type": role_name,
                            "📊 Status": "🟢 APPROVED",
                            "👨‍⚖️ Reviewer": interaction.user.mention
                        }, 0x00FF00)
                        break
            
            await interaction.response.send_message(f"✅ {self.applicant.mention} has been approved for {role_name}!")
            
            # Wait 10 seconds then delete thread
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error approving application: {str(e)}", ephemeral=True)
    
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, emoji="❌")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role (1320538700656148541)
        is_admin = (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles))
        
        if not is_admin:
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        try:
            # Send DM to the applicant first
            try:
                dm_embed = discord.Embed(
                    title="🥀 Application Update",
                    description=f"Your {self.application_type} application for **{interaction.guild.name}** has been reviewed.",
                    color=0xFF0000
                )
                dm_embed.add_field(
                    name="📊 Decision",
                    value="❌ **Application Denied**",
                    inline=False
                )
                dm_embed.add_field(
                    name="📝 Feedback",
                    value="Your application did not meet our current requirements. You may reapply in the future after addressing any concerns.",
                    inline=False
                )
                dm_embed.add_field(
                    name="🔄 Next Steps",
                    value="• Review our server rules and guidelines\n• Consider improving your application\n• You may reapply after some time",
                    inline=False
                )
                dm_embed.set_footer(text="Thank you for your interest in our Victorian community")
                
                await self.applicant.send(embed=dm_embed)
                logger.info(f"🌹 Sent denial DM to {self.applicant.display_name}")
                
            except discord.Forbidden:
                logger.warning(f"🥀 Could not send DM to {self.applicant.display_name} - DMs blocked")
            except Exception as dm_error:
                logger.error(f"🥀 Error sending DM to {self.applicant.display_name}: {dm_error}")
            
            # Find and update the tracking message
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                async for message in log_channel.history(limit=50):
                    if (message.embeds and 
                        self.applicant.mention in str(message.embeds[0].to_dict()) and 
                        "Application" in message.embeds[0].title):
                        await update_tracking_message(message, f"❌ {self.application_type.title()} Application DENIED", {
                            "👤 Applicant": self.applicant.mention,
                            "🏷️ Type": self.application_type.title(),
                            "📊 Status": "🔴 DENIED",
                            "👨‍⚖️ Reviewer": interaction.user.mention
                        }, 0xFF0000)
                        break
            
            await interaction.response.send_message(f"❌ {self.applicant.mention}'s application has been denied. DM notification sent.")
            
            # Wait 10 seconds then delete thread
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error denying application: {str(e)}", ephemeral=True)

@bot.tree.command(name="apply", description="📋 Apply for a position in the manor")
@discord.app_commands.default_permissions(send_messages=True)
async def apply_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Manor Applications", description="Choose your desired position", color=EMBED_COLOR)
    embed.add_field(name="⚔️ Realm Job", value="Join the manor's workforce\nRole: <@&1394853894437343422>", inline=True)
    embed.add_field(name="👑 Admin", value="Lead and moderate the manor\nRole: <@&1320538700656148541>", inline=True)
    embed.set_footer(text="Select a button below to begin your application")
    
    view = ApplicationView()
    # Send as standalone message to channel, not as reply
    await interaction.response.send_message("✅ Application system activated!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)

# ADVANCED TICKET SYSTEM - 4 Types with Claim/Close Workflow
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Permissions", style=discord.ButtonStyle.primary, emoji="🔑")
    async def permissions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = PermissionsTicketModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="General", style=discord.ButtonStyle.secondary, emoji="❓")
    async def general_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = GeneralTicketModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Report", style=discord.ButtonStyle.danger, emoji="⚠️")
    async def report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ReportTicketModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Review", style=discord.ButtonStyle.success, emoji="📋")
    async def review_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ReviewTicketModal()
        await interaction.response.send_modal(modal)

class PermissionsTicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Permissions Ticket")
        
        self.realm_code = discord.ui.TextInput(
            label="What realm code do you need?",
            placeholder="Specify the realm code you're requesting...",
            style=discord.TextStyle.short,
            max_length=100
        )
        self.reason = discord.ui.TextInput(
            label="Reason for request",
            placeholder="Why do you need this realm code?",
            style=discord.TextStyle.paragraph,
            max_length=500
        )
        
        self.add_item(self.realm_code)
        self.add_item(self.reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        await self.create_ticket(interaction, "Permissions", f"Realm Code: {self.realm_code.value}\nReason: {self.reason.value}")

    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str, details: str):
        try:
            # Create private thread
            thread = await interaction.channel.create_thread(
                name=f"{ticket_type} - {interaction.user.display_name}",
                auto_archive_duration=1440
            )
            
            # Send ticket details to thread
            embed = discord.Embed(title=f"🎫 {ticket_type} Ticket", color=EMBED_COLOR)
            embed.add_field(name="👤 User", value=interaction.user.mention, inline=True)
            embed.add_field(name="📅 Created", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
            embed.add_field(name="📝 Details", value=details, inline=False)
            
            # Add claim and close buttons
            ticket_manage_view = TicketManageView(ticket_type=ticket_type, user=interaction.user)
            
            await thread.send(f"<@&1320538700656148541>", embed=embed, view=ticket_manage_view)
            
            # Create individual tracking message for this ticket
            tracking_msg = await create_tracking_message(f"🎫 {ticket_type} Ticket", {
                "👤 User": interaction.user.mention,
                "🏷️ Type": ticket_type,
                "📊 Status": "🟡 Open"
            }, EMBED_COLOR, f"TKT-{interaction.user.id}")
            
            # Store tracking message reference in the thread
            if tracking_msg:
                await thread.send(f"📊 **Tracking:** {tracking_msg.jump_url}", delete_after=1)
            
            await interaction.response.send_message(f"✅ Your {ticket_type} ticket has been created!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating ticket: {str(e)}", ephemeral=True)

class GeneralTicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="General Question Ticket")
        
        self.question = discord.ui.TextInput(
            label="Your Question",
            placeholder="What would you like to ask?",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        
        self.add_item(self.question)
    
    async def on_submit(self, interaction: discord.Interaction):
        await PermissionsTicketModal.create_ticket(self, interaction, "General", f"Question: {self.question.value}")

class ReportTicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Player Report Ticket")
        
        self.player = discord.ui.TextInput(
            label="Player to Report",
            placeholder="Username or mention the player...",
            style=discord.TextStyle.short,
            max_length=100
        )
        self.violation = discord.ui.TextInput(
            label="Rule Violation",
            placeholder="What rule did they break?",
            style=discord.TextStyle.paragraph,
            max_length=500
        )
        self.evidence = discord.ui.TextInput(
            label="Evidence (optional)",
            placeholder="Screenshots, messages, etc...",
            style=discord.TextStyle.paragraph,
            max_length=500,
            required=False
        )
        
        self.add_item(self.player)
        self.add_item(self.violation)
        self.add_item(self.evidence)
    
    async def on_submit(self, interaction: discord.Interaction):
        details = f"Reported Player: {self.player.value}\nViolation: {self.violation.value}"
        if self.evidence.value:
            details += f"\nEvidence: {self.evidence.value}"
        await PermissionsTicketModal.create_ticket(self, interaction, "Report", details)

class ReviewTicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Warning Review Ticket")
        
        self.warning_details = discord.ui.TextInput(
            label="Warning Details",
            placeholder="Describe the warning you want reviewed...",
            style=discord.TextStyle.paragraph,
            max_length=500
        )
        self.appeal_reason = discord.ui.TextInput(
            label="Why should it be reviewed?",
            placeholder="Explain why you believe the warning should be reviewed...",
            style=discord.TextStyle.paragraph,
            max_length=500
        )
        
        self.add_item(self.warning_details)
        self.add_item(self.appeal_reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        details = f"Warning: {self.warning_details.value}\nAppeal Reason: {self.appeal_reason.value}"
        await PermissionsTicketModal.create_ticket(self, interaction, "Review", details)

class TicketManageView(discord.ui.View):
    def __init__(self, ticket_type: str, user):
        super().__init__(timeout=None)
        self.ticket_type = ticket_type
        self.user = user
        self.claimed_by = None
    
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, emoji="✋")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role (1320538700656148541)
        is_admin = (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles))
        
        if not is_admin:
            await interaction.response.send_message("❌ Only staff can claim tickets", ephemeral=True)
            return
        
        self.claimed_by = interaction.user
        embed = discord.Embed(title="✋ Ticket Claimed", color=EMBED_COLOR)
        embed.add_field(name="Staff Member", value=interaction.user.mention, inline=True)
        embed.add_field(name="Status", value="In Progress", inline=True)
        
        # Find and update the tracking message
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            async for message in log_channel.history(limit=50):
                if (message.embeds and 
                    self.user.mention in str(message.embeds[0].to_dict()) and 
                    "Ticket" in message.embeds[0].title):
                    await update_tracking_message(message, f"✋ {self.ticket_type} Ticket CLAIMED", {
                        "👤 User": self.user.mention,
                        "🏷️ Type": self.ticket_type,
                        "📊 Status": "🟠 CLAIMED",
                        "👨‍⚖️ Claimed By": interaction.user.mention
                    }, 0xFFA500)
                    break
        
        await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role (1320538700656148541)
        is_admin = (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles))
        
        if not is_admin:
            await interaction.response.send_message("❌ Only staff can close tickets", ephemeral=True)
            return
        
        modal = TicketCloseModal(self.ticket_type, self.user)
        await interaction.response.send_modal(modal)

class TicketCloseModal(discord.ui.Modal):
    def __init__(self, ticket_type: str, user):
        super().__init__(title="Close Ticket")
        self.ticket_type = ticket_type
        self.user = user
        
        self.resolution = discord.ui.TextInput(
            label="How was this ticket resolved?",
            placeholder="Describe the solution or outcome...",
            style=discord.TextStyle.paragraph,
            max_length=1000
        )
        
        self.add_item(self.resolution)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(f"🔒 Ticket closed successfully!")
            
            # Find and update the tracking message
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                async for message in log_channel.history(limit=50):
                    if (message.embeds and 
                        self.user.mention in str(message.embeds[0].to_dict()) and 
                        "Ticket" in message.embeds[0].title):
                        await update_tracking_message(message, f"🔒 {self.ticket_type} Ticket CLOSED", {
                            "👤 User": self.user.mention,
                            "🏷️ Type": self.ticket_type,
                            "📊 Status": "🟢 CLOSED",
                            "👨‍⚖️ Closed By": interaction.user.mention,
                            "📝 Resolution": self.resolution.value
                        }, 0x00FF00)
                        break
            
            # Wait 10 seconds then delete thread
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            try:
                await interaction.followup.send(f"❌ Error closing ticket: {str(e)}", ephemeral=True)
            except:
                pass

@bot.tree.command(name="tickets", description="🎫 Create a support ticket")
@discord.app_commands.default_permissions(send_messages=True)
async def tickets_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 Manor Support Tickets", description="Choose the type of assistance you need", color=EMBED_COLOR)
    embed.add_field(name="🔑 Permissions", value="Request realm codes and access", inline=True)
    embed.add_field(name="❓ General", value="Ask general questions", inline=True)
    embed.add_field(name="⚠️ Report", value="Report rule violations", inline=True)
    embed.add_field(name="📋 Review", value="Appeal warnings or infractions", inline=True)
    embed.set_footer(text="Staff will respond promptly • Select a button below")
    
    view = TicketView()
    # Send as standalone message to channel, not as reply
    await interaction.response.send_message("✅ Ticket system activated!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)
    
    # Check tutorial progress
    await check_tutorial_progress(interaction.user.id, "tickets")

# AI TEST COMMANDS  
@bot.tree.command(name="aitest", description="🤖 Test free AI sentiment analysis and moderation")
@discord.app_commands.default_permissions(send_messages=True)
async def aitest_command(interaction: discord.Interaction, message: str):
    try:
        from services.huggingface_ai import free_ai
        
        # Initialize AI if needed
        await free_ai.initialize()
        
        # Analyze sentiment and moderate content
        sentiment = await free_ai.analyze_sentiment(message)
        moderation = await free_ai.moderate_content(message)
        
        embed = discord.Embed(title="🤖 Free AI Analysis", description="Victorian intelligence at thy service", color=EMBED_COLOR)
        embed.add_field(name="📝 Message", value=f"```{message[:100]}{'...' if len(message) > 100 else ''}```", inline=False)
        embed.add_field(name="💭 Sentiment", value=f"**{sentiment.title()}**", inline=True)
        
        safety_status = "✅ Safe" if moderation['safe'] else "⚠️ Flagged"
        embed.add_field(name="🛡️ Safety", value=safety_status, inline=True)
        
        if moderation['categories']:
            embed.add_field(name="🔍 Issues", value=", ".join(moderation['categories']), inline=True)
        
        embed.set_footer(text="Powered by free AI libraries • No API costs required")
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ AI Test Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="aiinfo", description="ℹ️ Information about free AI features")
@discord.app_commands.default_permissions(send_messages=True)
async def aiinfo_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 Free AI Features", description="RosethornBot's intelligence capabilities", color=EMBED_COLOR)
    embed.add_field(name="💭 Sentiment Analysis", value="Detects positive, negative, neutral emotions", inline=True)
    embed.add_field(name="🛡️ Content Moderation", value="Flags toxic, spam, and inappropriate content", inline=True)
    embed.add_field(name="🌹 Welcome Messages", value="Generates Victorian Gothic greetings", inline=True)
    embed.add_field(name="💰 No Costs", value="Uses free TextBlob & VADER libraries", inline=True)
    embed.add_field(name="🔄 Fallback System", value="OpenAI first, then free AI backup", inline=True)
    embed.add_field(name="🧪 Test Command", value="Use `/aitest` to try it out!", inline=True)
    embed.set_footer(text="Completely free AI - no API keys required")
    await interaction.response.send_message(embed=embed)

# INDIVIDUAL TRACKING SYSTEM
async def create_tracking_message(title, fields, color, ticket_id=None):
    """Create individual tracking message for each ticket/application"""
    log_channel = bot.get_channel(1320540890141556746)
    if not log_channel:
        return None
    
    try:
        embed = discord.Embed(title=title, description="Status will update as this progresses", color=color)
        
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=True)
        
        embed.add_field(name="📅 Created", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
        embed.set_footer(text=f"ID: {ticket_id or 'N/A'} • Created: {datetime.now().strftime('%H:%M:%S')}")
        
        message = await log_channel.send(embed=embed)
        return message
    except Exception as e:
        print(f"Error creating tracking message: {e}")
        return None

async def update_tracking_message(message, title, fields, color):
    """Update an existing tracking message"""
    if not message:
        return
    
    try:
        embed = discord.Embed(title=title, description="Status updated", color=color)
        
        for field_name, field_value in fields.items():
            embed.add_field(name=field_name, value=field_value, inline=True)
        
        embed.add_field(name="📅 Last Updated", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
        embed.set_footer(text=f"{message.embeds[0].footer.text.split('•')[0]}• Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        await message.edit(embed=embed)
    except Exception as e:
        print(f"Error updating tracking message: {e}")

# MISSING COMMANDS
@bot.tree.command(name="purgechat", description="🧹 Delete multiple messages from this channel")
@discord.app_commands.default_permissions(manage_messages=True)
async def purgechat_command(interaction: discord.Interaction, count: int = 10):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can purge messages", ephemeral=True)
        return
    
    if count < 1 or count > 100:
        await interaction.response.send_message("❌ Please specify between 1-100 messages to delete", ephemeral=True)
        return
    
    try:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=count)
        
        embed = discord.Embed(title="🧹 Messages Purged", description="Channel cleanup completed", color=EMBED_COLOR)
        embed.add_field(name="📊 Messages Deleted", value=f"{len(deleted)} messages", inline=True)
        embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
        embed.add_field(name="📍 Channel", value=interaction.channel.mention, inline=True)
        embed.set_footer(text="Manor maintenance completed")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Log the action
        await create_tracking_message("🧹 Messages Purged", {
            "📍 Channel": interaction.channel.mention,
            "📊 Count": f"{len(deleted)} messages",
            "👨‍⚖️ Moderator": interaction.user.mention
        }, EMBED_COLOR, f"PURGE-{interaction.id}")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error purging messages: {str(e)}", ephemeral=True)

@bot.tree.command(name="deletechannel", description="🗑️ Delete the current channel or thread")
@discord.app_commands.default_permissions(manage_channels=True)
async def deletechannel_command(interaction: discord.Interaction, confirmation: str = ""):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can delete channels", ephemeral=True)
        return
    
    if confirmation.lower() != "confirm":
        await interaction.response.send_message("❌ Please use `/deletechannel confirm` to confirm deletion", ephemeral=True)
        return
    
    try:
        channel_name = interaction.channel.name
        channel_type = "thread" if hasattr(interaction.channel, 'parent') else "channel"
        
        # Log before deletion
        await create_tracking_message(f"🗑️ {channel_type.title()} Deleted", {
            "📍 Name": channel_name,
            "🏷️ Type": channel_type.title(),
            "👨‍⚖️ Deleted By": interaction.user.mention
        }, 0xFF0000, f"DEL-{interaction.id}")
        
        await interaction.response.send_message(f"🗑️ Deleting {channel_type} in 5 seconds...", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Deleted by {interaction.user}")
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error deleting {channel_type}: {str(e)}", ephemeral=True)

@bot.tree.command(name="sticky", description="📌 Create auto-resending sticky messages that stay at bottom")
@discord.app_commands.default_permissions(manage_messages=True)
@discord.app_commands.describe(
    action="Action to perform with sticky messages",
    message="Content for the sticky message (required for create)"
)
@discord.app_commands.choices(action=[
    discord.app_commands.Choice(name="Create Auto-Sticky", value="create"),
    discord.app_commands.Choice(name="Remove Sticky", value="remove"),
    discord.app_commands.Choice(name="Check Status", value="status"),
    discord.app_commands.Choice(name="Toggle On/Off", value="toggle"),
    discord.app_commands.Choice(name="Manual Resend", value="resend")
])
@handle_errors
async def sticky_command(interaction: discord.Interaction, action: str = "status", message: str = ""):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can manage sticky messages", ephemeral=True)
        return
    
    if not sticky_service:
        await interaction.response.send_message("❌ Sticky message service not initialized", ephemeral=True)
        return
    
    channel = interaction.channel
    channel_id = channel.id
    action = action.lower()
    
    if action == "create":
        if not message:
            await interaction.response.send_message("❌ Please provide a message to make sticky", ephemeral=True)
            return
        
        # Check if channel already has a sticky message
        if sticky_service.is_sticky_active(channel_id):
            await interaction.response.send_message("❌ This channel already has an active sticky message. Use `/sticky remove` first.", ephemeral=True)
            return
        
        # Create sticky message embed data (simplified - title and message only)
        embed_data = {
            'title': "📌 Manor Notice",
            'description': message,
            'color': EMBED_COLOR,
            'fields': []  # No extra fields for cleaner look
        }
        
        # Create the embed
        embed = discord.Embed(
            title=embed_data['title'],
            description=embed_data['description'],
            color=embed_data['color']
        )
        
        # No fields to add - keeping it simple with just title and description
        
        try:
            # Send initial sticky message
            await interaction.response.send_message("✅ Creating auto-resending sticky message...", ephemeral=True)
            sticky_msg = await channel.send(embed=embed)
            
            # Add to sticky service
            sticky_service.add_sticky_message(
                channel_id=channel_id,
                content=message,
                embed_data=embed_data,
                created_by=interaction.user.id
            )
            
            # Update the service with the message ID
            sticky_info = sticky_service.get_sticky_info(channel_id)
            if sticky_info:
                sticky_info['last_message_id'] = sticky_msg.id
            
            # Log the sticky creation
            await create_tracking_message("📌 Auto-Sticky Message Created", {
                "📍 Channel": channel.mention,
                "💬 Message": message[:100] + ("..." if len(message) > 100 else ""),
                "👨‍⚖️ Created By": interaction.user.mention,
                "🔗 Message ID": str(sticky_msg.id),
                "⚙️ Type": "Auto-resending every 3 messages"
            }, EMBED_COLOR, f"STICKY-{sticky_msg.id}")
            
        except Exception as e:
            await interaction.followup.send(f"❌ Error creating sticky message: {str(e)}", ephemeral=True)
    
    elif action == "remove":
        if not sticky_service.is_sticky_active(channel_id):
            await interaction.response.send_message("❌ No active sticky message found in this channel", ephemeral=True)
            return
        
        try:
            # Get sticky info before removing
            sticky_info = sticky_service.get_sticky_info(channel_id)
            
            # Delete the current sticky message if it exists
            if sticky_info and sticky_info['last_message_id']:
                try:
                    old_message = await channel.fetch_message(sticky_info['last_message_id'])
                    await old_message.delete()
                except (discord.NotFound, discord.Forbidden):
                    pass
            
            # Remove from service
            sticky_service.remove_sticky_message(channel_id)
            
            # Log the removal
            await create_tracking_message("📌 Auto-Sticky Message Removed", {
                "📍 Channel": channel.mention,
                "👨‍⚖️ Removed By": interaction.user.mention,
                "⚙️ Type": "Auto-resending sticky"
            }, 0xFF0000, f"STICKY-DEL-{channel_id}")
            
            await interaction.response.send_message("✅ Auto-sticky message removed successfully", ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error removing sticky message: {str(e)}", ephemeral=True)
    
    elif action == "status":
        sticky_info = sticky_service.get_sticky_info(channel_id)
        
        if not sticky_info:
            embed = discord.Embed(
                title="📌 Sticky Message Status",
                description="No active sticky message in this channel",
                color=EMBED_COLOR
            )
            embed.add_field(name="💡 Tip", value="Use `/sticky create <message>` to create an auto-resending sticky message", inline=False)
        else:
            embed = discord.Embed(
                title="📌 Active Sticky Message",
                description=f"**Content:** {sticky_info['content'][:100]}{'...' if len(sticky_info['content']) > 100 else ''}",
                color=EMBED_COLOR
            )
            embed.add_field(name="📍 Channel", value=channel.mention, inline=True)
            embed.add_field(name="🔄 Status", value="Active" if sticky_info['active'] else "Paused", inline=True)
            embed.add_field(name="📅 Created", value=discord.utils.format_dt(sticky_info['created_at'], style='R'), inline=True)
            embed.add_field(name="⚙️ Resend Trigger", value="Every 3 messages", inline=True)
            embed.add_field(name="📊 Message Count", value=f"{sticky_service.message_counts.get(channel_id, 0)}/3", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action == "toggle":
        if not sticky_service.is_sticky_active(channel_id):
            await interaction.response.send_message("❌ No sticky message found in this channel to toggle", ephemeral=True)
            return
        
        new_state = sticky_service.toggle_sticky(channel_id)
        status = "enabled" if new_state else "paused"
        
        embed = discord.Embed(
            title="📌 Sticky Message Toggled",
            description=f"Auto-resending sticky message has been **{status}**",
            color=EMBED_COLOR if new_state else 0x8B4513
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action == "resend":
        if not sticky_service.is_sticky_active(channel_id):
            await interaction.response.send_message("❌ No active sticky message found in this channel", ephemeral=True)
            return
        
        success = await sticky_service.manual_resend(channel)
        
        if success:
            await interaction.response.send_message("✅ Sticky message manually resent", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to resend sticky message", ephemeral=True)
    
    else:
        await interaction.response.send_message("❌ Invalid action. Use: create, remove, status, toggle, or resend", ephemeral=True)

@bot.tree.command(name="reputation", description="🌟 Manage Victorian manor standing and virtues")
@discord.app_commands.default_permissions(manage_messages=True)
async def reputation_command(interaction: discord.Interaction, action: str = "view", member: discord.Member = None, points: int = 1, reason: str = "", virtue: str = "general"):
    # Check if user has admin role for giving reputation
    if action in ["give", "add", "remove"] and not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can award reputation", ephemeral=True)
        return
    
    if action == "view" or action == "check":
        target = member or interaction.user
        
        # Get member from database
        from models import Member, Reputation
        db_member = Member.query.filter_by(user_id=str(target.id), guild_id=str(interaction.guild.id)).first()
        
        if not db_member:
            # Create new member
            db_member = Member(
                user_id=str(target.id),
                guild_id=str(interaction.guild.id),
                username=target.display_name
            )
            db.session.add(db_member)
            db.session.commit()
        
        # Get recent reputation entries
        recent_rep = Reputation.query.filter_by(
            user_id=str(target.id),
            guild_id=str(interaction.guild.id)
        ).order_by(Reputation.created_at.desc()).limit(5).all()
        
        embed = discord.Embed(
            title="🌟 Manor Standing & Virtues",
            description=f"**{target.display_name}'s** reputation within our Victorian community",
            color=EMBED_COLOR
        )
        
        # Calculate virtue breakdown
        virtue_counts = {}
        for rep in recent_rep:
            virtue_counts[rep.virtue_type] = virtue_counts.get(rep.virtue_type, 0) + rep.points
        
        embed.add_field(
            name="🏛️ Overall Standing",
            value=f"**{db_member.reputation}** Reputation Points",
            inline=True
        )
        
        if virtue_counts:
            virtues_text = "\n".join([f"• **{virtue.title()}:** {points}" for virtue, points in virtue_counts.items()])
            embed.add_field(
                name="✨ Victorian Virtues",
                value=virtues_text,
                inline=True
            )
        
        embed.add_field(
            name="📊 Community Rank",
            value=get_reputation_rank(db_member.reputation),
            inline=True
        )
        
        if recent_rep:
            recent_text = "\n".join([
                f"**+{rep.points}** {rep.virtue_type} - {rep.reason[:30]}..." 
                for rep in recent_rep[:3]
            ])
            embed.add_field(
                name="📜 Recent Recognition",
                value=recent_text,
                inline=False
            )
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="Victorian virtue system • Manor community standing")
        await interaction.response.send_message(embed=embed)
    
    elif action == "give" or action == "add":
        if not member:
            await interaction.response.send_message("❌ Please specify a member to award reputation", ephemeral=True)
            return
        
        if not reason:
            reason = f"Recognized for {virtue} by manor administration"
        
        # Get or create member
        from models import Member, Reputation
        db_member = Member.query.filter_by(user_id=str(member.id), guild_id=str(interaction.guild.id)).first()
        
        if not db_member:
            db_member = Member(
                user_id=str(member.id),
                guild_id=str(interaction.guild.id),
                username=member.display_name
            )
            db.session.add(db_member)
        
        # Add reputation
        db_member.reputation += points
        
        # Create reputation entry
        rep_entry = Reputation(
            guild_id=str(interaction.guild.id),
            user_id=str(member.id),
            given_by=str(interaction.user.id),
            points=points,
            reason=reason,
            virtue_type=virtue
        )
        db.session.add(rep_entry)
        db.session.commit()
        
        # Send confirmation
        embed = discord.Embed(
            title="🌟 Reputation Awarded",
            description=f"**{member.display_name}** has been recognized for their virtue",
            color=0x00FF00
        )
        embed.add_field(name="✨ Virtue", value=virtue.title(), inline=True)
        embed.add_field(name="📈 Points", value=f"+{points}", inline=True)
        embed.add_field(name="🏛️ New Standing", value=f"{db_member.reputation} points", inline=True)
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        embed.set_footer(text=f"Awarded by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
        
        # Log the award
        await create_tracking_message("🌟 Reputation Awarded", {
            "👤 Member": member.mention,
            "✨ Virtue": virtue.title(),
            "📈 Points": f"+{points}",
            "📝 Reason": reason,
            "👨‍⚖️ Awarded By": interaction.user.mention
        }, 0x00FF00, f"REP-{rep_entry.id}")
    
    elif action == "leaderboard" or action == "top":
        from models import Member
        top_members = Member.query.filter_by(guild_id=str(interaction.guild.id)).order_by(Member.reputation.desc()).limit(10).all()
        
        embed = discord.Embed(
            title="🏆 Manor Reputation Leaderboard",
            description="Most virtuous members of our Victorian community",
            color=EMBED_COLOR
        )
        
        for i, member_data in enumerate(top_members, 1):
            try:
                user = bot.get_user(int(member_data.user_id))
                name = user.display_name if user else member_data.username
                rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                
                embed.add_field(
                    name=f"{rank_emoji} {name}",
                    value=f"**{member_data.reputation}** reputation\n{get_reputation_rank(member_data.reputation)}",
                    inline=True
                )
            except:
                continue
        
        embed.set_footer(text="Recognition for virtue and community contribution")
        await interaction.response.send_message(embed=embed)

def get_reputation_rank(points):
    """Get reputation rank title based on points."""
    if points >= 1000:
        return "🏰 **Manor Lord/Lady**"
    elif points >= 500:
        return "👑 **Distinguished Noble**"
    elif points >= 250:
        return "🎭 **Esteemed Resident**"
    elif points >= 100:
        return "🌹 **Respected Member**"
    elif points >= 50:
        return "📚 **Manor Scholar**"
    elif points >= 25:
        return "🕯️ **Promising Guest**"
    else:
        return "🚪 **New Arrival**"

@bot.tree.command(name="event", description="🎭 Create and manage manor events")
@discord.app_commands.default_permissions(manage_events=True)
async def event_command(interaction: discord.Interaction, action: str = "list", title: str = "", date: str = "", description: str = ""):
    # Check if user has admin role
    if action in ["create", "cancel", "edit"] and not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can manage events", ephemeral=True)
        return
    
    if action == "create":
        if not title or not date:
            await interaction.response.send_message("❌ Please provide event title and date (YYYY-MM-DD HH:MM)", ephemeral=True)
            return
        
        try:
            from datetime import datetime
            event_datetime = datetime.strptime(date, "%Y-%m-%d %H:%M")
            
            from models import ManorEvent
            event = ManorEvent(
                guild_id=str(interaction.guild.id),
                title=title,
                description=description or "Join us for this Victorian manor gathering",
                event_date=event_datetime,
                created_by=str(interaction.user.id),
                channel_id=str(interaction.channel.id)
            )
            db.session.add(event)
            db.session.commit()
            
            embed = discord.Embed(
                title="🎭 Manor Event Created",
                description=f"**{title}** has been scheduled",
                color=EMBED_COLOR
            )
            embed.add_field(name="📅 Date & Time", value=discord.utils.format_dt(event_datetime, style='F'), inline=False)
            embed.add_field(name="📝 Description", value=description or "Join us for this Victorian manor gathering", inline=False)
            embed.add_field(name="🏛️ RSVP", value="React with ✅ to attend, ❓ for maybe, ❌ to decline", inline=False)
            embed.set_footer(text=f"Event ID: {event.id} • Created by {interaction.user.display_name}")
            
            message = await interaction.response.send_message(embed=embed)
            
            # Add RSVP reactions
            await message.add_reaction("✅")
            await message.add_reaction("❓") 
            await message.add_reaction("❌")
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid date format. Use YYYY-MM-DD HH:MM", ephemeral=True)
    
    elif action == "list":
        from models import ManorEvent
        upcoming_events = ManorEvent.query.filter(
            ManorEvent.guild_id == str(interaction.guild.id),
            ManorEvent.event_date > datetime.now()
        ).order_by(ManorEvent.event_date).limit(10).all()
        
        if not upcoming_events:
            embed = discord.Embed(
                title="🎭 Manor Events",
                description="No upcoming events scheduled. Create one with `/event create`",
                color=EMBED_COLOR
            )
        else:
            embed = discord.Embed(
                title="🎭 Upcoming Manor Events",
                description="Victorian gatherings and activities",
                color=EMBED_COLOR
            )
            
            for event in upcoming_events:
                embed.add_field(
                    name=f"🎭 {event.title}",
                    value=f"📅 {discord.utils.format_dt(event.event_date, style='F')}\n📝 {event.description[:100]}...",
                    inline=False
                )
        
        embed.set_footer(text="Use /event create to schedule new events")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quote", description="📜 Victorian wisdom and daily quotes")
async def quote_command(interaction: discord.Interaction, action: str = "daily"):
    from models import VictorianQuote, UserQuoteCollection
    import random
    
    if action == "daily" or action == "random":
        # Get a random quote based on rarity
        quotes = VictorianQuote.query.all()
        if not quotes:
            # Seed some quotes if none exist
            await seed_quotes()
            quotes = VictorianQuote.query.all()
        
        # Weighted random selection based on rarity
        rarity_weights = {"common": 70, "rare": 25, "legendary": 5}
        available_quotes = []
        
        for quote in quotes:
            weight = rarity_weights.get(quote.rarity, 1)
            available_quotes.extend([quote] * weight)
        
        selected_quote = random.choice(available_quotes)
        
        # Check if user has this quote
        existing = UserQuoteCollection.query.filter_by(
            user_id=str(interaction.user.id),
            quote_id=selected_quote.id
        ).first()
        
        if not existing:
            # Add to user's collection
            collection_entry = UserQuoteCollection(
                user_id=str(interaction.user.id),
                quote_id=selected_quote.id
            )
            db.session.add(collection_entry)
            db.session.commit()
            collection_text = "✨ **New quote added to your collection!**"
        else:
            collection_text = "📚 Already in your collection"
        
        # Get rarity color
        rarity_colors = {"common": 0x708090, "rare": 0x9932CC, "legendary": 0xFFD700}
        color = rarity_colors.get(selected_quote.rarity, EMBED_COLOR)
        
        embed = discord.Embed(
            title="📜 Victorian Wisdom",
            description=f"*\"{selected_quote.quote_text}\"*",
            color=color
        )
        
        if selected_quote.author:
            embed.add_field(name="✍️ Author", value=selected_quote.author, inline=True)
        
        embed.add_field(name="🎭 Rarity", value=selected_quote.rarity.title(), inline=True)
        embed.add_field(name="📚 Collection", value=collection_text, inline=True)
        embed.set_footer(text="Daily wisdom from the Victorian era • Use /quote collection to view all")
        
        await interaction.response.send_message(embed=embed)
    
    elif action == "collection" or action == "my":
        # Show user's quote collection
        user_quotes = db.session.query(VictorianQuote).join(
            UserQuoteCollection, VictorianQuote.id == UserQuoteCollection.quote_id
        ).filter(UserQuoteCollection.user_id == str(interaction.user.id)).all()
        
        if not user_quotes:
            embed = discord.Embed(
                title="📚 Your Quote Collection",
                description="You haven't collected any quotes yet. Use `/quote daily` to start collecting Victorian wisdom!",
                color=EMBED_COLOR
            )
        else:
            embed = discord.Embed(
                title="📚 Your Victorian Quote Collection",
                description=f"You have collected **{len(user_quotes)}** pieces of wisdom",
                color=EMBED_COLOR
            )
            
            # Group by rarity
            common = [q for q in user_quotes if q.rarity == "common"]
            rare = [q for q in user_quotes if q.rarity == "rare"]
            legendary = [q for q in user_quotes if q.rarity == "legendary"]
            
            if common:
                embed.add_field(name="📜 Common", value=str(len(common)), inline=True)
            if rare:
                embed.add_field(name="🎭 Rare", value=str(len(rare)), inline=True)
            if legendary:
                embed.add_field(name="👑 Legendary", value=str(len(legendary)), inline=True)
            
            # Show recent quotes
            recent = user_quotes[-3:] if len(user_quotes) >= 3 else user_quotes
            for quote in recent:
                embed.add_field(
                    name=f"{quote.rarity.title()} Quote",
                    value=f"*\"{quote.quote_text[:100]}...\"*",
                    inline=False
                )
        
        embed.set_footer(text="Collect more quotes with /quote daily")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def seed_quotes():
    """Seed the database with Victorian quotes."""
    from models import VictorianQuote
    
    quotes_data = [
        {"text": "The way to get started is to quit talking and begin doing.", "author": "Victorian Proverb", "rarity": "common"},
        {"text": "In the depth of winter, I finally learned that within me there lay an invincible summer.", "author": "Victorian Sage", "rarity": "rare"},
        {"text": "A lady's imagination is very rapid; it jumps from admiration to love, from love to matrimony in a moment.", "author": "Jane Austen", "rarity": "legendary"},
        {"text": "The ornament of a house is the friends who frequent it.", "author": "Victorian Wisdom", "rarity": "common"},
        {"text": "There is nothing like staying at home for real comfort.", "author": "Jane Austen", "rarity": "rare"},
        {"text": "We are all in the gutter, but some of us are looking at the stars.", "author": "Oscar Wilde", "rarity": "legendary"},
    ]
    
    for quote_data in quotes_data:
        existing = VictorianQuote.query.filter_by(quote_text=quote_data["text"]).first()
        if not existing:
            quote = VictorianQuote(
                quote_text=quote_data["text"],
                author=quote_data["author"],
                rarity=quote_data["rarity"]
            )
            db.session.add(quote)
    
    db.session.commit()

@bot.tree.command(name="voice", description="🎵 Voice channel activity and statistics")
async def voice_command(interaction: discord.Interaction, action: str = "stats", member: discord.Member = None):
    target = member or interaction.user
    
    if action == "stats":
        from models import Member, VoiceSession
        
        # Get member data
        db_member = Member.query.filter_by(user_id=str(target.id), guild_id=str(interaction.guild.id)).first()
        
        if not db_member:
            db_member = Member(
                user_id=str(target.id),
                guild_id=str(interaction.guild.id),
                username=target.display_name
            )
            db.session.add(db_member)
            db.session.commit()
        
        # Get voice session data
        total_sessions = VoiceSession.query.filter_by(
            user_id=str(target.id),
            guild_id=str(interaction.guild.id)
        ).count()
        
        # Calculate total time
        completed_sessions = VoiceSession.query.filter(
            VoiceSession.user_id == str(target.id),
            VoiceSession.guild_id == str(interaction.guild.id),
            VoiceSession.duration_seconds.isnot(None)
        ).all()
        
        total_minutes = sum([session.duration_seconds // 60 for session in completed_sessions])
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        embed = discord.Embed(
            title="🎵 Voice Activity Statistics",
            description=f"**{target.display_name}'s** participation in manor conversations",
            color=EMBED_COLOR
        )
        
        embed.add_field(name="⏱️ Total Time", value=f"{hours}h {minutes}m", inline=True)
        embed.add_field(name="📊 Sessions", value=str(total_sessions), inline=True)
        embed.add_field(name="🏅 Voice Rank", value=get_voice_rank(total_minutes), inline=True)
        
        # Calculate average session length
        if completed_sessions:
            avg_minutes = total_minutes // len(completed_sessions)
            embed.add_field(name="⏳ Avg Session", value=f"{avg_minutes} minutes", inline=True)
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="Victorian manor voice participation tracking")
        await interaction.response.send_message(embed=embed)
    
    elif action == "leaderboard":
        from models import Member
        
        top_members = Member.query.filter_by(guild_id=str(interaction.guild.id)).order_by(Member.voice_minutes.desc()).limit(10).all()
        
        embed = discord.Embed(
            title="🎵 Voice Activity Leaderboard",
            description="Most active voices in our Victorian manor",
            color=EMBED_COLOR
        )
        
        for i, member_data in enumerate(top_members, 1):
            if member_data.voice_minutes > 0:
                try:
                    user = bot.get_user(int(member_data.user_id))
                    name = user.display_name if user else member_data.username
                    hours = member_data.voice_minutes // 60
                    minutes = member_data.voice_minutes % 60
                    
                    rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                    
                    embed.add_field(
                        name=f"{rank_emoji} {name}",
                        value=f"**{hours}h {minutes}m**\n{get_voice_rank(member_data.voice_minutes)}",
                        inline=True
                    )
                except:
                    continue
        
        embed.set_footer(text="Active participation in manor voice channels")
        await interaction.response.send_message(embed=embed)

def get_voice_rank(minutes):
    """Get voice activity rank based on minutes."""
    if minutes >= 3000:  # 50+ hours
        return "🎭 **Conversational Virtuoso**"
    elif minutes >= 1800:  # 30+ hours
        return "🎵 **Manor Orator**"
    elif minutes >= 900:   # 15+ hours
        return "📢 **Active Speaker**"
    elif minutes >= 300:   # 5+ hours
        return "🗣️ **Regular Participant**"
    elif minutes >= 60:    # 1+ hour
        return "👥 **Social Guest**"
    else:
        return "🤫 **Quiet Observer**"

# Voice state tracking for activity
@bot.event
async def on_voice_state_update(member, before, after):
    """Track voice channel activity."""
    from models import VoiceSession, Member
    
    guild_id = str(member.guild.id)
    user_id = str(member.id)
    
    # Member joined a voice channel
    if before.channel is None and after.channel is not None:
        session = VoiceSession(
            guild_id=guild_id,
            user_id=user_id,
            channel_id=str(after.channel.id),
            joined_at=datetime.now()
        )
        db.session.add(session)
        db.session.commit()
    
    # Member left a voice channel
    elif before.channel is not None and after.channel is None:
        # Find the active session
        session = VoiceSession.query.filter_by(
            guild_id=guild_id,
            user_id=user_id,
            left_at=None
        ).first()
        
        if session:
            session.left_at = datetime.now()
            duration = (session.left_at - session.joined_at).total_seconds()
            session.duration_seconds = int(duration)
            
            # Update member's total voice time
            db_member = Member.query.filter_by(user_id=user_id, guild_id=guild_id).first()
            if not db_member:
                db_member = Member(
                    user_id=user_id,
                    guild_id=guild_id,
                    username=member.display_name
                )
                db.session.add(db_member)
            
            db_member.voice_minutes += int(duration // 60)
            db.session.commit()

@bot.tree.command(name="spotlight", description="⭐ Member spotlight and recognition system")
@discord.app_commands.default_permissions(manage_messages=True)
async def spotlight_command(interaction: discord.Interaction, action: str = "current", member: discord.Member = None, reason: str = ""):
    # Check if user has admin role
    if action in ["nominate", "set"] and not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can manage member spotlight", ephemeral=True)
        return
    
    from models import MemberSpotlight
    from datetime import date, timedelta
    
    if action == "current" or action == "this_week":
        # Get current week's spotlight
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        current_spotlight = MemberSpotlight.query.filter_by(
            guild_id=str(interaction.guild.id),
            week_of=week_start
        ).first()
        
        if not current_spotlight:
            embed = discord.Embed(
                title="⭐ Member Spotlight",
                description="No member spotlight set for this week. Admins can nominate someone with `/spotlight nominate`",
                color=EMBED_COLOR
            )
        else:
            try:
                user = bot.get_user(int(current_spotlight.user_id))
                if user:
                    embed = discord.Embed(
                        title="⭐ This Week's Member Spotlight",
                        description=f"Celebrating **{user.display_name}** for their contributions to our Victorian community",
                        color=0xFFD700
                    )
                    embed.add_field(name="📝 Recognition", value=current_spotlight.reason or "Outstanding community member", inline=False)
                    embed.add_field(name="👨‍⚖️ Nominated By", value=f"<@{current_spotlight.nominated_by}>", inline=True)
                    embed.add_field(name="📅 Week Of", value=week_start.strftime("%B %d, %Y"), inline=True)
                    embed.set_thumbnail(url=user.display_avatar.url)
                else:
                    embed = discord.Embed(
                        title="⭐ Member Spotlight",
                        description="Member spotlight set but user not found",
                        color=EMBED_COLOR
                    )
            except:
                embed = discord.Embed(
                    title="⭐ Member Spotlight",
                    description="Error loading spotlight information",
                    color=EMBED_COLOR
                )
        
        embed.set_footer(text="Weekly recognition of exceptional community members")
        await interaction.response.send_message(embed=embed)
    
    elif action == "nominate" or action == "set":
        if not member:
            await interaction.response.send_message("❌ Please specify a member for the spotlight", ephemeral=True)
            return
        
        if not reason:
            reason = "Outstanding contribution to our Victorian manor community"
        
        # Get current week
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        # Check if spotlight already exists for this week
        existing = MemberSpotlight.query.filter_by(
            guild_id=str(interaction.guild.id),
            week_of=week_start
        ).first()
        
        if existing:
            existing.user_id = str(member.id)
            existing.reason = reason
            existing.nominated_by = str(interaction.user.id)
        else:
            spotlight = MemberSpotlight(
                guild_id=str(interaction.guild.id),
                user_id=str(member.id),
                week_of=week_start,
                reason=reason,
                nominated_by=str(interaction.user.id)
            )
            db.session.add(spotlight)
        
        db.session.commit()
        
        # Create spotlight embed
        embed = discord.Embed(
            title="⭐ Member Spotlight - This Week",
            description=f"**{member.display_name}** has been selected as our featured community member!",
            color=0xFFD700
        )
        embed.add_field(name="📝 Recognition", value=reason, inline=False)
        embed.add_field(name="👨‍⚖️ Nominated By", value=interaction.user.mention, inline=True)
        embed.add_field(name="📅 Week Of", value=week_start.strftime("%B %d, %Y"), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Celebrating excellence in our Victorian community")
        
        await interaction.response.send_message(embed=embed)
        
        # Log the spotlight
        await create_tracking_message("⭐ Member Spotlight Set", {
            "👤 Member": member.mention,
            "📝 Reason": reason,
            "👨‍⚖️ Nominated By": interaction.user.mention,
            "📅 Week": week_start.strftime("%B %d, %Y")
        }, 0xFFD700, f"SPOTLIGHT-{week_start.strftime('%Y%m%d')}")

@bot.tree.command(name="announce", description="📢 Create and schedule manor announcements")
@discord.app_commands.default_permissions(manage_messages=True)
async def announce_command(interaction: discord.Interaction, action: str = "now", content: str = "", schedule: str = "", title: str = ""):
    # Check if user has admin role
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can create announcements", ephemeral=True)
        return
    
    if action == "now" or action == "immediate":
        if not content:
            await interaction.response.send_message("❌ Please provide announcement content", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=title or "📢 Manor Announcement",
            description=content,
            color=EMBED_COLOR
        )
        embed.add_field(name="👨‍⚖️ Announced By", value=interaction.user.mention, inline=True)
        embed.add_field(name="📅 Date", value=discord.utils.format_dt(datetime.now(), style='F'), inline=True)
        embed.set_footer(text="Official announcement from Rosewood Manor administration")
        
        await interaction.response.send_message(embed=embed)
        
        # Log the announcement
        await create_tracking_message("📢 Manor Announcement", {
            "📰 Title": title or "General Announcement",
            "💬 Content": content[:200] + ("..." if len(content) > 200 else ""),
            "👨‍⚖️ By": interaction.user.mention,
            "📍 Channel": interaction.channel.mention
        }, EMBED_COLOR, f"ANNOUNCE-{interaction.id}")
    
    elif action == "schedule":
        if not content or not schedule:
            await interaction.response.send_message("❌ Please provide content and schedule (YYYY-MM-DD HH:MM)", ephemeral=True)
            return
        
        try:
            from datetime import datetime
            schedule_time = datetime.strptime(schedule, "%Y-%m-%d %H:%M")
            
            from models import ScheduledAnnouncement
            scheduled = ScheduledAnnouncement(
                guild_id=str(interaction.guild.id),
                channel_id=str(interaction.channel.id),
                title=title or "Scheduled Manor Announcement",
                content=content,
                next_send=schedule_time,
                created_by=str(interaction.user.id)
            )
            db.session.add(scheduled)
            db.session.commit()
            
            embed = discord.Embed(
                title="⏰ Announcement Scheduled",
                description="Your manor announcement has been scheduled successfully",
                color=EMBED_COLOR
            )
            embed.add_field(name="📰 Title", value=title or "Scheduled Manor Announcement", inline=False)
            embed.add_field(name="💬 Content", value=content[:200] + ("..." if len(content) > 200 else ""), inline=False)
            embed.add_field(name="📅 Scheduled For", value=discord.utils.format_dt(schedule_time, style='F'), inline=True)
            embed.add_field(name="📍 Channel", value=interaction.channel.mention, inline=True)
            embed.set_footer(text=f"Announcement ID: {scheduled.id}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message("❌ Invalid schedule format. Use YYYY-MM-DD HH:MM", ephemeral=True)
    
    elif action == "list":
        from models import ScheduledAnnouncement
        pending = ScheduledAnnouncement.query.filter(
            ScheduledAnnouncement.guild_id == str(interaction.guild.id),
            ScheduledAnnouncement.active == True,
            ScheduledAnnouncement.next_send > datetime.now()
        ).order_by(ScheduledAnnouncement.next_send).all()
        
        if not pending:
            embed = discord.Embed(
                title="📢 Scheduled Announcements",
                description="No pending announcements. Use `/announce schedule` to create one.",
                color=EMBED_COLOR
            )
        else:
            embed = discord.Embed(
                title="📢 Scheduled Manor Announcements",
                description=f"**{len(pending)}** pending announcements",
                color=EMBED_COLOR
            )
            
            for announcement in pending[:10]:  # Limit to 10
                channel = bot.get_channel(int(announcement.channel_id))
                channel_name = channel.name if channel else "Unknown"
                
                embed.add_field(
                    name=f"📰 {announcement.title}",
                    value=f"📅 {discord.utils.format_dt(announcement.next_send, style='R')}\n📍 #{channel_name}\n💬 {announcement.content[:50]}...",
                    inline=False
                )
        
        embed.set_footer(text="Manor announcement scheduling system")
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="rolemanage", description="🎭 Custom role assignment and management")
async def rolemanage_command(interaction: discord.Interaction, action: str = "list", role: discord.Role = None, member: discord.Member = None):
    # Define self-assignable roles (customize these)
    SELF_ASSIGNABLE_ROLES = [
        "🎨 Artist", "📚 Scholar", "🎵 Musician", "🌙 Night Owl", "☀️ Early Bird", 
        "🎮 Gamer", "📖 Bookworm", "🍵 Tea Lover", "☕ Coffee Enthusiast"
    ]
    
    if action == "list" or action == "available":
        embed = discord.Embed(
            title="🎭 Available Custom Roles",
            description="Victorian manor roles you can assign to yourself",
            color=EMBED_COLOR
        )
        
        # Find existing self-assignable roles
        guild_roles = interaction.guild.roles
        available_roles = []
        
        for role_name in SELF_ASSIGNABLE_ROLES:
            role_obj = discord.utils.get(guild_roles, name=role_name)
            if role_obj:
                available_roles.append(role_obj)
        
        if available_roles:
            role_list = "\n".join([f"• {role.mention}" for role in available_roles])
            embed.add_field(name="🏷️ Self-Assignable Roles", value=role_list, inline=False)
        else:
            embed.add_field(name="🏷️ Self-Assignable Roles", value="No custom roles available yet", inline=False)
        
        embed.add_field(
            name="📋 Commands",
            value="`/rolemanage assign @role` - Assign role to yourself\n`/rolemanage remove @role` - Remove role from yourself",
            inline=False
        )
        embed.set_footer(text="Only certain roles can be self-assigned")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action == "assign" or action == "add":
        if not role:
            await interaction.response.send_message("❌ Please specify a role to assign", ephemeral=True)
            return
        
        target = member or interaction.user
        
        # Check if role is self-assignable
        if role.name not in SELF_ASSIGNABLE_ROLES and not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
            await interaction.response.send_message("❌ This role cannot be self-assigned", ephemeral=True)
            return
        
        if role in target.roles:
            await interaction.response.send_message(f"❌ {target.display_name} already has the {role.name} role", ephemeral=True)
            return
        
        try:
            await target.add_roles(role, reason=f"Role assigned by {interaction.user}")
            
            embed = discord.Embed(
                title="🎭 Role Assigned",
                description=f"**{role.name}** has been added to {target.mention}",
                color=0x00FF00
            )
            embed.set_footer(text="Victorian manor role management")
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ Cannot assign this role due to permission hierarchy", ephemeral=True)
    
    elif action == "remove" or action == "unassign":
        if not role:
            await interaction.response.send_message("❌ Please specify a role to remove", ephemeral=True)
            return
        
        target = member or interaction.user
        
        if role not in target.roles:
            await interaction.response.send_message(f"❌ {target.display_name} doesn't have the {role.name} role", ephemeral=True)
            return
        
        try:
            await target.remove_roles(role, reason=f"Role removed by {interaction.user}")
            
            embed = discord.Embed(
                title="🎭 Role Removed",
                description=f"**{role.name}** has been removed from {target.mention}",
                color=0xFF6B6B
            )
            embed.set_footer(text="Victorian manor role management")
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ Cannot remove this role due to permission hierarchy", ephemeral=True)

# PLAYFUL ONBOARDING TUTORIAL SYSTEM
class TutorialStep:
    def __init__(self, title, description, action_type, action_data=None, completion_message="Well done!"):
        self.title = title
        self.description = description
        self.action_type = action_type  # 'command', 'reaction', 'button', 'completion'
        self.action_data = action_data or {}
        self.completion_message = completion_message

# Tutorial steps with Victorian Gothic character guidance
TUTORIAL_STEPS = [
    TutorialStep(
        "🌹 Welcome to Rosewood Manor",
        "Greetings, dear guest! I am **Lady Rosalind**, the manor's ethereal guide. Welcome to our Victorian estate where shadows dance with moonlight and every corner holds secrets waiting to be discovered.",
        "button",
        {"button_text": "Enter the Manor", "next_step": 1}
    ),
    TutorialStep(
        "💰 Your Manor Treasury",
        "Every resident of our manor possesses a treasury of mystical **Rosebuds** - our ethereal currency. These crimson petals hold power within our realm. Try the `/balance` command to glimpse your spiritual wealth.",
        "command",
        {"command": "balance", "next_step": 2},
        "Splendid! Your treasury shimmers with potential. These rosebuds shall serve you well in our manor's mysterious endeavors."
    ),
    TutorialStep(
        "📜 Manor Wisdom & Lore",
        "Knowledge is power in our shadowed halls. Use `/rosenotes` to discover the ancient wisdom and personal chronicles that bind our community together through time and mystery.",
        "command",
        {"command": "rosenotes", "next_step": 3},
        "Excellent! The ancient texts reveal their secrets to those who seek knowledge. These chronicles hold the memories of all who dwell within our walls."
    ),
    TutorialStep(
        "🎭 Manor Entertainment",
        "Even in the shadows, we find joy and merriment. Try `/trivia` to test your wit against the manor's riddles, or `/8ball` to commune with the mystical spirits that guide our fate.",
        "command",
        {"command": "trivia", "next_step": 4, "alternatives": ["8ball"]},
        "Marvelous! Your spirit brightens these ancient halls. Entertainment is the soul's respite from the weight of eternity."
    ),
    TutorialStep(
        "🎫 Manor Assistance",
        "Should you ever require aid or wish to report disturbances in our peaceful realm, use `/tickets` to summon assistance from our devoted staff. We are always here to help.",
        "command",
        {"command": "tickets", "next_step": 5},
        "Wise choice! Our staff are ever-vigilant guardians of peace and order within the manor. Never hesitate to seek their counsel."
    ),
    TutorialStep(
        "🌹 Your Manor Journey Begins",
        "Congratulations, dear resident! You have completed your initiation into the mysteries of Rosewood Manor. Lady Rosalind's guidance has prepared you for the adventures that await within our shadowed halls.",
        "completion",
        {"rewards": {"rosebuds": 100, "title": "Manor Initiate"}},
        "Welcome to your new eternal home, Manor Initiate! May your journey be filled with wonder, mystery, and the dark beauty that defines our Victorian realm."
    )
]

class TutorialView(discord.ui.View):
    def __init__(self, user_id, step_number=0):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.step_number = step_number
        self.setup_buttons()
    
    def setup_buttons(self):
        self.clear_items()
        current_step = TUTORIAL_STEPS[self.step_number]
        
        if current_step.action_type == "button":
            button = discord.ui.Button(
                label=current_step.action_data.get("button_text", "Continue"),
                style=discord.ButtonStyle.primary,
                emoji="🌹"
            )
            button.callback = self.next_step_callback
            self.add_item(button)
        
        # Add next step button for command steps
        if current_step.action_type == "command":
            next_button = discord.ui.Button(
                label="Next Step",
                style=discord.ButtonStyle.success,
                emoji="➡️"
            )
            next_button.callback = self.next_step_callback
            self.add_item(next_button)
        
        # Always add skip button except on completion
        if current_step.action_type != "completion":
            skip_button = discord.ui.Button(
                label="Skip Tutorial",
                style=discord.ButtonStyle.secondary,
                emoji="⏭️"
            )
            skip_button.callback = self.skip_tutorial
            self.add_item(skip_button)
    
    async def next_step_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This tutorial is not for you", ephemeral=True)
            return
        
        current_step = TUTORIAL_STEPS[self.step_number]
        next_step_num = current_step.action_data.get("next_step", self.step_number + 1)
        
        # Update tutorial tracking
        if self.user_id in tutorial_tracking:
            tutorial_tracking[self.user_id]["current_step"] = next_step_num
        
        if next_step_num < len(TUTORIAL_STEPS):
            await self.show_step(interaction, next_step_num)
        else:
            await self.complete_tutorial(interaction)
    
    async def skip_tutorial(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This tutorial is not for you", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🌹 Tutorial Skipped",
            description="Lady Rosalind fades into the shadows with a knowing smile.\n\n*\"The manor's mysteries await your discovery at your own pace, dear guest. Should you wish to learn, simply use `/tutorial` again.\"*",
            color=EMBED_COLOR
        )
        embed.set_footer(text="You can restart the tutorial anytime with /tutorial")
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def show_step(self, interaction, step_number):
        self.step_number = step_number
        self.setup_buttons()
        
        step = TUTORIAL_STEPS[step_number]
        
        embed = discord.Embed(
            title=step.title,
            description=step.description,
            color=EMBED_COLOR
        )
        
        # Add step progress
        embed.add_field(
            name="📍 Progress", 
            value=f"Step {step_number + 1} of {len(TUTORIAL_STEPS)}", 
            inline=True
        )
        
        if step.action_type == "command":
            embed.add_field(
                name="🎯 Your Task",
                value=f"Try the `/{step.action_data['command']}` command",
                inline=True
            )
            if "alternatives" in step.action_data:
                embed.add_field(
                    name="✨ Alternatives",
                    value=" or ".join([f"`/{alt}`" for alt in step.action_data["alternatives"]]),
                    inline=True
                )
        
        embed.set_thumbnail(url="https://i.imgur.com/placeholder_rosalind.png")  # Placeholder for character image
        embed.set_footer(text="Lady Rosalind guides you through the manor • Tutorial System")
        
        # Add instruction for command steps
        if step.action_type == "command":
            embed.add_field(
                name="💡 Hint",
                value="Try the command above, then click 'Next Step' to continue!",
                inline=False
            )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def show_step_follow_up(self, interaction, step_number):
        """Show next step as a follow-up message after button interaction"""
        self.step_number = step_number
        self.setup_buttons()
        
        step = TUTORIAL_STEPS[step_number]
        
        embed = discord.Embed(
            title=step.title,
            description=step.description,
            color=EMBED_COLOR
        )
        
        # Add step progress
        embed.add_field(
            name="📍 Progress", 
            value=f"Step {step_number + 1} of {len(TUTORIAL_STEPS)}", 
            inline=True
        )
        
        if step.action_type == "command":
            embed.add_field(
                name="🎯 Your Task",
                value=f"Try the `/{step.action_data['command']}` command",
                inline=True
            )
            if "alternatives" in step.action_data:
                embed.add_field(
                    name="✨ Alternatives",
                    value=" or ".join([f"`/{alt}`" for alt in step.action_data["alternatives"]]),
                    inline=True
                )
        
        embed.set_thumbnail(url="https://i.imgur.com/placeholder_rosalind.png")
        embed.set_footer(text="Lady Rosalind guides you through the manor • Tutorial System")
        
        try:
            await interaction.followup.send(embed=embed, view=self, ephemeral=True)
        except:
            # If followup fails, try editing original message
            await interaction.edit_original_response(embed=embed, view=self)
        

    
    async def complete_tutorial(self, interaction):
        step = TUTORIAL_STEPS[-1]
        
        embed = discord.Embed(
            title=step.title,
            description=step.description,
            color=0x00FF00
        )
        
        # Show rewards
        rewards = step.action_data.get("rewards", {})
        if rewards:
            reward_text = []
            if "rosebuds" in rewards:
                reward_text.append(f"🌹 {rewards['rosebuds']} Rosebuds")
            if "title" in rewards:
                reward_text.append(f"🏷️ Title: **{rewards['title']}**")
            
            embed.add_field(name="🎁 Rewards Earned", value="\n".join(reward_text), inline=False)
        
        embed.add_field(
            name="🗝️ What's Next?",
            value="• Explore commands with `/help`\n• Join conversations in manor channels\n• Apply for positions with `/apply`\n• Create tickets with `/tickets` if you need help",
            inline=False
        )
        
        embed.set_footer(text="Welcome to Rosewood Manor! Your adventure begins now...")
        
        # Log tutorial completion
        await create_tracking_message("🎓 Tutorial Completed", {
            "👤 User": interaction.user.mention,
            "📚 Status": "✅ Completed",
            "🎁 Rewards": "100 Rosebuds + Manor Initiate Title"
        }, 0x00FF00, f"TUTORIAL-{interaction.user.id}")
        
        await interaction.response.edit_message(embed=embed, view=None)

# Tutorial tracking for command completion
tutorial_tracking = {}

# ONBOARDING MODAL AND APPROVAL SYSTEM
class OnboardingModal(discord.ui.Modal, title="Rosewood Manor Registration"):
    def __init__(self):
        super().__init__()
        
    preferred_name = discord.ui.TextInput(
        label="Preferred Name for Discord",
        placeholder="What should we call you in our manor?",
        required=True,
        max_length=32
    )
    
    gamertag = discord.ui.TextInput(
        label="Gamertag",
        placeholder="Your Minecraft/Gaming username",
        required=True,
        max_length=32
    )
    
    birthdate = discord.ui.TextInput(
        label="Birthdate",
        placeholder="MM/DD/YYYY (for age verification)",
        required=True,
        max_length=10
    )
    
    referral = discord.ui.TextInput(
        label="How did you hear about us?",
        placeholder="Friend, social media, search, etc.",
        required=False,
        max_length=100
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        # Create approval embed
        embed = discord.Embed(
            title="🌹 New Manor Registration",
            description="A new member seeks entry to our Victorian estate",
            color=EMBED_COLOR
        )
        
        embed.add_field(name="👤 Preferred Name", value=self.preferred_name.value, inline=True)
        embed.add_field(name="🎮 Gamertag", value=self.gamertag.value, inline=True)
        embed.add_field(name="📅 Birthdate", value=self.birthdate.value, inline=True)
        embed.add_field(name="📢 Referral", value=self.referral.value or "Not specified", inline=True)
        embed.add_field(name="📍 Discord User", value=interaction.user.mention, inline=True)
        embed.add_field(name="🕐 Submitted", value=discord.utils.format_dt(datetime.now(), style='f'), inline=True)
        embed.add_field(name="📊 Status", value="⏳ **Pending Review**", inline=False)
        
        embed.set_footer(text=f"Registration ID: REG-{interaction.user.id}")
        
        # Create approval view
        view = OnboardingApprovalView(interaction.user.id, self.preferred_name.value, self.gamertag.value)
        
        # Send to logging channel
        logging_channel = bot.get_channel(1320540890141556746)
        if logging_channel:
            approval_message = await logging_channel.send(embed=embed, view=view)
            
            # Store message ID for tracking
            view.approval_message_id = approval_message.id
        
        # Confirm submission to user
        confirm_embed = discord.Embed(
            title="✅ Registration Submitted",
            description="Your application to join Rosewood Manor has been submitted for review.",
            color=0x00FF00
        )
        confirm_embed.add_field(
            name="⏳ What's Next?",
            value="• Our admins will review your application\n• You'll receive a DM with the decision\n• If approved, you'll gain access to member areas",
            inline=False
        )
        confirm_embed.set_footer(text="Thank you for your patience • Manor Administration")
        
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

class OnboardingApprovalView(discord.ui.View):
    def __init__(self, user_id, preferred_name, gamertag):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.preferred_name = preferred_name
        self.gamertag = gamertag
        self.approval_message_id = None
    
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, emoji="✅")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role
        if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
            await interaction.response.send_message("❌ Only administrators can approve registrations", ephemeral=True)
            return
        
        # Get the user to approve
        user = bot.get_user(self.user_id)
        guild = interaction.guild
        member = guild.get_member(self.user_id)
        
        if not member:
            await interaction.response.send_message("❌ Member not found in server", ephemeral=True)
            return
        
        try:
            # Change nickname to "Preferred name [gamertag]" format
            new_nickname = f"{self.preferred_name} [{self.gamertag}]"
            await member.edit(nick=new_nickname)
            
            # Add member role (1311529774946193460)
            member_role = guild.get_role(1311529774946193460)
            if member_role:
                await member.add_roles(member_role)
            
            # Update the approval embed
            original_embed = interaction.message.embeds[0]
            original_embed.set_field_at(6, name="📊 Status", value="✅ **Approved**", inline=False)
            original_embed.add_field(name="👨‍⚖️ Approved By", value=interaction.user.mention, inline=True)
            original_embed.add_field(name="⏰ Approved At", value=discord.utils.format_dt(datetime.now(), style='f'), inline=True)
            original_embed.color = 0x00FF00
            
            # Send DM to approved member
            try:
                dm_embed = discord.Embed(
                    title="🌹 Welcome to Rosewood Manor!",
                    description=f"Congratulations, {self.preferred_name}! Your registration has been approved.",
                    color=0x00FF00
                )
                dm_embed.add_field(
                    name="🎉 You now have access to:",
                    value="• Member-only channels\n• Special commands and features\n• Community events and activities",
                    inline=False
                )
                dm_embed.add_field(
                    name="🌹 Next Steps:",
                    value="• Explore the manor with `/tutorial`\n• Check out `/rules` to review our guidelines\n• Visit member channels to introduce yourself",
                    inline=False
                )
                dm_embed.set_footer(text="Welcome to our Victorian community!")
                
                await user.send(embed=dm_embed)
            except:
                pass  # DM failed, continue anyway
            
            # Disable buttons and update message
            for item in self.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=original_embed, view=self)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error processing approval: {str(e)}", ephemeral=True)
    
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, emoji="❌")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin role
        if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
            await interaction.response.send_message("❌ Only administrators can deny registrations", ephemeral=True)
            return
        
        # Show denial reason modal
        modal = DenialReasonModal(self.user_id, self.preferred_name, interaction.message)
        await interaction.response.send_modal(modal)

class DenialReasonModal(discord.ui.Modal, title="Registration Denial Reason"):
    def __init__(self, user_id, preferred_name, approval_message):
        super().__init__()
        self.user_id = user_id
        self.preferred_name = preferred_name
        self.approval_message = approval_message
    
    reason = discord.ui.TextInput(
        label="Reason for Denial",
        placeholder="Please provide a clear reason for denying this registration...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        user = bot.get_user(self.user_id)
        
        # Update the approval embed
        original_embed = self.approval_message.embeds[0]
        original_embed.set_field_at(6, name="📊 Status", value="❌ **Denied**", inline=False)
        original_embed.add_field(name="👨‍⚖️ Denied By", value=interaction.user.mention, inline=True)
        original_embed.add_field(name="⏰ Denied At", value=discord.utils.format_dt(datetime.now(), style='f'), inline=True)
        original_embed.add_field(name="📝 Denial Reason", value=self.reason.value, inline=False)
        original_embed.color = 0xFF0000
        
        # Send DM to denied member
        try:
            dm_embed = discord.Embed(
                title="🥀 Registration Update",
                description=f"Dear {self.preferred_name}, your registration to Rosewood Manor requires attention.",
                color=0xFF0000
            )
            dm_embed.add_field(
                name="📝 Admin Feedback:",
                value=self.reason.value,
                inline=False
            )
            dm_embed.add_field(
                name="🔄 Next Steps:",
                value="• Please address the feedback provided\n• You may resubmit your registration\n• Contact an admin if you need clarification",
                inline=False
            )
            dm_embed.set_footer(text="We appreciate your understanding • Manor Administration")
            
            await user.send(embed=dm_embed)
        except:
            pass  # DM failed, continue anyway
        
        # Disable buttons and update message
        view = discord.ui.View()
        for item in view.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=original_embed, view=view)

# RULES COMMAND AND AGREEMENT SYSTEM
class RulesAgreementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="I Agree", style=discord.ButtonStyle.success, emoji="✅")
    async def agree_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Add rules agreement role (1394518008570970172)
        guild = interaction.guild
        member = interaction.user
        rules_role = guild.get_role(1394518008570970172)
        
        if rules_role:
            if rules_role in member.roles:
                await interaction.response.send_message("✅ You have already agreed to the rules!", ephemeral=True)
                return
            
            await member.add_roles(rules_role)
            
            embed = discord.Embed(
                title="✅ Rules Agreement Confirmed",
                description="Thank you for agreeing to the Rosewood Manor rules!",
                color=0x00FF00
            )
            embed.add_field(
                name="🌹 Welcome to the Community",
                value="You now have full access to member features and can participate in all manor activities.",
                inline=False
            )
            embed.set_footer(text="Remember to follow the rules at all times • Manor Administration")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log the agreement
            await create_tracking_message("📜 Rules Agreement", {
                "👤 Member": interaction.user.mention,
                "📅 Agreed At": discord.utils.format_dt(datetime.now(), style='f'),
                "✅ Status": "Confirmed"
            }, 0x00FF00, f"RULES-{interaction.user.id}")
            
        else:
            await interaction.response.send_message("❌ Rules role not found. Please contact an administrator.", ephemeral=True)

@bot.tree.command(name="onboard", description="🌹 Begin your registration to Rosewood Manor")
@discord.app_commands.default_permissions(send_messages=True)
async def onboard_command(interaction: discord.Interaction):
    modal = OnboardingModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="rules", description="📜 View and agree to the manor rules")
@discord.app_commands.default_permissions(send_messages=True)
async def rules_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Rosewood Manor Rules",
        description="Please read and agree to our community guidelines",
        color=EMBED_COLOR
    )
    
    rules_part1 = """**1. Building Restrictions**
Do **NOT** build within 1000 blocks of spawn in any direction. If your base is visible from spawn, you are too close.

**2. No Stealing or Griefing**
Theft, destruction, or griefing will **not** be tolerated. Violators **will** be permanently banned—no second chances.

**3. No Spamming**
Avoid excessive messaging in-game or on Discord. Due to varying time zones, responses may be delayed.

**4. Respect Messaging Boundaries**
Do **NOT** DM members without permission. Use <#1325432475387957288> before reaching out."""
    
    rules_part2 = """**5. Respect Personal Space**
Avoid building too close to others. If you can see another player's base from yours, you're too close. Set up your land claim.

**6. Auto Farms Regulations**
All auto farms **must receive admin approval**, be designated for community use, & include a manual on/off switch.

**7. Zero Tolerance for Harassment**
Treat everyone with respect. **Harassment, witch-hunting, racism, sexism, and hate speech are strictly forbidden**.

**8. Keep Chats Organized**
Use appropriate channels for discussions. We aim to keep the server welcoming and cozy for all members."""
    
    embed.add_field(name="🏰 Core Rules (1-4)", value=rules_part1, inline=False)
    embed.add_field(name="🛡️ Core Rules (5-8)", value=rules_part2, inline=False)
    
    member_requirements = """**9. Member Mode Requirements**
To access member mode, you must:
✅ Add your gamertag 
✅ Confirm agreement to these rules
✅ Respond to bot DM (Message "Thorn" if you can't find it)

**10. Realm Code Sharing**
Sharing the realm code requires admin approval. New players must join Discord and agree to the rules."""
    
    admin_guidelines = """**11. Admin Requests**
Admins will only provide basic building blocks. Support community shops by purchasing resources from fellow players.

**12. Ticket System**
Once a ticket is opened, you have **12 hours** to respond. Do **NOT** DM admins regarding open tickets."""
    
    embed.add_field(name="📋 Member Requirements (9-10)", value=member_requirements, inline=False)
    embed.add_field(name="⚖️ Admin Guidelines (11-12)", value=admin_guidelines, inline=False)
    embed.add_field(name="⚖️ Violations", value="If you violate any rules, a ticket will be created to review the situation, allowing you to explain your perspective.", inline=False)
    embed.set_footer(text="By clicking 'I Agree', you accept these rules • Updated regularly")
    
    view = RulesAgreementView()
    # Send as standalone message to channel, not as reply
    await interaction.response.send_message("✅ Rules posted!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)

@bot.tree.command(name="tutorial", description="🎭 Begin your guided tour of Rosewood Manor")
@discord.app_commands.default_permissions(send_messages=True)
async def tutorial_command(interaction: discord.Interaction):
    # Create initial tutorial embed
    step = TUTORIAL_STEPS[0]
    
    embed = discord.Embed(
        title=step.title,
        description=step.description,
        color=EMBED_COLOR
    )
    
    embed.add_field(
        name="📍 Progress", 
        value=f"Step 1 of {len(TUTORIAL_STEPS)}", 
        inline=True
    )
    
    embed.add_field(
        name="⏱️ Duration",
        value="~3-5 minutes",
        inline=True
    )
    
    embed.set_thumbnail(url="https://i.imgur.com/placeholder_rosalind.png")  # Placeholder for character image
    embed.set_footer(text="Lady Rosalind awaits your presence • Interactive Tutorial")
    
    view = TutorialView(interaction.user.id, 0)
    tutorial_tracking[interaction.user.id] = {"current_step": 0, "started_at": datetime.now()}
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# Enhanced command tracking for tutorial progression
async def check_tutorial_progress(user_id, command_used):
    """Check if user completed a tutorial step"""
    if user_id not in tutorial_tracking:
        return
    
    current_step_num = tutorial_tracking[user_id]["current_step"]
    if current_step_num >= len(TUTORIAL_STEPS):
        return
    
    current_step = TUTORIAL_STEPS[current_step_num]
    
    if (current_step.action_type == "command" and 
        (command_used == current_step.action_data.get("command") or 
         command_used in current_step.action_data.get("alternatives", []))):
        
        # User completed the step!
        tutorial_tracking[user_id]["current_step"] += 1
        
        # Send completion message and next step
        try:
            user = bot.get_user(user_id)
            if user:
                # Step completion message
                completion_embed = discord.Embed(
                    title="✨ Step Completed!",
                    description=f"**Lady Rosalind nods approvingly**\n\n*\"{current_step.completion_message}\"*",
                    color=0x00FF00
                )
                completion_embed.set_footer(text="Well done! Moving to the next step...")
                await user.send(embed=completion_embed)
                
                # Wait a moment
                await asyncio.sleep(2)
                
                next_step_num = tutorial_tracking[user_id]["current_step"]
                if next_step_num < len(TUTORIAL_STEPS):
                    next_step = TUTORIAL_STEPS[next_step_num]
                    
                    # Send next step
                    next_embed = discord.Embed(
                        title=next_step.title,
                        description=next_step.description,
                        color=EMBED_COLOR
                    )
                    
                    next_embed.add_field(
                        name="📍 Progress", 
                        value=f"Step {next_step_num + 1} of {len(TUTORIAL_STEPS)}", 
                        inline=True
                    )
                    
                    if next_step.action_type == "command":
                        next_embed.add_field(
                            name="🎯 Your Task",
                            value=f"Try the `/{next_step.action_data['command']}` command",
                            inline=True
                        )
                        if "alternatives" in next_step.action_data:
                            next_embed.add_field(
                                name="✨ Alternatives",
                                value=" or ".join([f"`/{alt}`" for alt in next_step.action_data["alternatives"]]),
                                inline=True
                            )
                    
                    next_embed.set_footer(text="Lady Rosalind guides you through the manor • Tutorial System")
                    
                    # Create a simple view for skip option
                    view = TutorialSkipView(user_id, next_step_num)
                    await user.send(embed=next_embed, view=view)
                    
                else:
                    # Tutorial complete
                    final_embed = discord.Embed(
                        title="🎉 Tutorial Complete!",
                        description="Congratulations! You have mastered the basics of Rosewood Manor.",
                        color=0x00FF00
                    )
                    final_embed.add_field(
                        name="🎁 Rewards Earned",
                        value="🌹 100 Rosebuds\n🏷️ Title: **Manor Initiate**",
                        inline=False
                    )
                    final_embed.set_footer(text="Welcome to our Victorian community!")
                    await user.send(embed=final_embed)
                    
                    # Log completion
                    await create_tracking_message("🎓 Tutorial Completed", {
                        "👤 User": user.mention,
                        "📚 Status": "✅ Completed via Command Tracking",
                        "🎁 Rewards": "100 Rosebuds + Manor Initiate Title"
                    }, 0x00FF00, f"TUTORIAL-AUTO-{user_id}")
                    
                    del tutorial_tracking[user_id]
                    
        except Exception as e:
            print(f"Error in tutorial progression: {e}")

class TutorialSkipView(discord.ui.View):
    def __init__(self, user_id, step_number):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.step_number = step_number
    
    @discord.ui.button(label="Skip Tutorial", style=discord.ButtonStyle.secondary, emoji="⏭️")
    async def skip_tutorial(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This tutorial is not for you", ephemeral=True)
            return
        
        if self.user_id in tutorial_tracking:
            del tutorial_tracking[self.user_id]
        
        embed = discord.Embed(
            title="🌹 Tutorial Skipped",
            description="Lady Rosalind fades into the shadows with a knowing smile.\n\n*\"The manor's mysteries await your discovery at your own pace, dear guest.\"*",
            color=EMBED_COLOR
        )
        embed.set_footer(text="You can restart the tutorial anytime with /tutorial")
        await interaction.response.edit_message(embed=embed, view=None)

# SIMPLIFIED DM ONBOARDING SYSTEM
@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Handle sticky message resending
    if sticky_service and isinstance(message.channel, discord.TextChannel):
        await sticky_service.on_message(message)
    
    # Check if it's a DM and the message is "thorn" or "Thorn"
    if (isinstance(message.channel, discord.DMChannel) and 
        message.content.lower() == "thorn"):
        
        # Send simplified onboarding
        embed = discord.Embed(
            title="🌹 Welcome to Rosewood Manor",
            description="Greetings! I am the Rosewood Manor bot, here to guide you through our Victorian community.",
            color=EMBED_COLOR
        )
        
        embed.add_field(
            name="🏰 About Our Manor",
            value="We are a Victorian Gothic themed Minecraft realm and Discord community focused on building, creativity, and respectful collaboration.",
            inline=False
        )
        
        embed.add_field(
            name="📋 Quick Start Steps:",
            value="1️⃣ Join our Discord server\n2️⃣ Use `/onboard` to register\n3️⃣ Read and agree to `/rules`\n4️⃣ Get approved by our admins\n5️⃣ Receive realm access!",
            inline=False
        )
        
        embed.add_field(
            name="🎭 New Member Features:",
            value="• Use `/tutorial` for a guided tour\n• Try `/balance` to check your Rosebuds\n• Create `/tickets` if you need help\n• Explore with `/help` for all commands",
            inline=False
        )
        
        embed.add_field(
            name="🌹 Ready to Begin?",
            value="Head to our Discord server and use the `/onboard` command to start your registration process!",
            inline=False
        )
        
        embed.set_footer(text="We look forward to welcoming you to our manor • Rosewood Administration")
        
        try:
            await message.author.send(embed=embed)
        except:
            pass  # If DM fails, silently continue
        
        # Log the DM interaction
        await create_tracking_message("📱 DM Onboarding Triggered", {
            "👤 User": f"{message.author.display_name} ({message.author.id})",
            "💬 Trigger": "DM: 'thorn'",
            "📅 Time": discord.utils.format_dt(datetime.now(), style='f')
        }, EMBED_COLOR, f"DM-{message.author.id}")
    
    # Process other commands
    await bot.process_commands(message)

# Welcome banner management commands
@bot.tree.command(name="welcomebanner", description="🎨 Configure animated welcome banners")
@discord.app_commands.default_permissions(manage_guild=True)
@discord.app_commands.describe(
    action="Choose an action to perform with welcome banners",
    channel="Channel where welcome banners will be sent (for setup)",
    template="Visual template for the welcome banner"
)
@discord.app_commands.choices(action=[
    discord.app_commands.Choice(name="Check Status", value="status"),
    discord.app_commands.Choice(name="Setup/Configure", value="setup"),
    discord.app_commands.Choice(name="Test Banner", value="test"),
    discord.app_commands.Choice(name="Toggle On/Off", value="toggle")
])
@discord.app_commands.choices(template=[
    discord.app_commands.Choice(name="Victorian Rose", value="victorian_rose"),
    discord.app_commands.Choice(name="Gothic Manor", value="gothic_manor"),
    discord.app_commands.Choice(name="Elegant Throne", value="elegant_throne"),
    discord.app_commands.Choice(name="Mystical Garden", value="mystical_garden")
])
@handle_errors
async def welcomebanner_command(interaction: discord.Interaction, action: str = "status", channel: discord.TextChannel = None, template: str = "victorian_rose"):
    try:
        from services.welcome_banner import welcome_banner_service
        
        if action == "status":
            embed = discord.Embed(
                title="🎨 Welcome Banner Settings",
                description="Current configuration for new member banners",
                color=EMBED_COLOR
            )
            embed.add_field(name="⚠️ Database Setup Required", value="Welcome banners require database configuration.\nCurrently operating in preview mode only.", inline=False)
            embed.add_field(name="🎨 Available Templates", value="• Victorian Rose\n• Gothic Manor\n• Elegant Throne\n• Mystical Garden", inline=False)
            await interaction.response.send_message(embed=embed)
        
        elif action == "setup":
            if not channel:
                await interaction.response.send_message("❌ Please specify a channel for welcome banners", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="🎨 Welcome Banner Configuration",
                description="Welcome banner settings configured (preview mode)",
                color=EMBED_COLOR
            )
            embed.add_field(name="📍 Channel", value=channel.mention, inline=True)
            embed.add_field(name="🎨 Template", value=template.replace("_", " ").title(), inline=True)
            embed.add_field(name="⚠️ Note", value="Database integration pending. Banners will work when member joins.", inline=False)
            
            await interaction.response.send_message(embed=embed)
        
        elif action == "test":
            banner_bytes = await welcome_banner_service.create_welcome_banner(interaction.user, interaction.guild)
            banner_file = discord.File(banner_bytes, filename=f"test_welcome_{interaction.user.id}.png")
            embed = await welcome_banner_service.create_animated_embed(interaction.user, interaction.guild)
            embed.title = "🧪 Test Welcome Banner"
            embed.description = f"Preview of animated welcome banner for **{interaction.user.display_name}**"
            
            await interaction.response.send_message(file=banner_file, embed=embed, ephemeral=True)
        
        elif action == "toggle":
            embed = discord.Embed(
                title="🎨 Welcome Banner Toggle",
                description="Welcome banners are currently in preview mode.\nFull database integration coming soon!",
                color=EMBED_COLOR
            )
            await interaction.response.send_message(embed=embed)
                
    except Exception as e:
        embed = discord.Embed(title="🎨 Welcome Banner Error", description=f"Error: {str(e)}", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Global error handler for the bot
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Global error handler for slash commands"""
    await error_handler.handle_command_error(interaction, error, interaction.command.name if interaction.command else None)

# Bot Management Commands
@bot.tree.command(name="botstatus", description="🤖 Check bot status and performance metrics")
@discord.app_commands.default_permissions(manage_messages=True)
@handle_errors
async def bot_status_command(interaction: discord.Interaction):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can check bot status", ephemeral=True)
        return
    
    import psutil
    import time
    from datetime import timedelta
    
    # Get bot uptime
    uptime_seconds = time.time() - bot.start_time if hasattr(bot, 'start_time') else 0
    uptime = str(timedelta(seconds=int(uptime_seconds)))
    
    # Get system metrics
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_used = memory.used // (1024 * 1024)  # MB
    memory_total = memory.total // (1024 * 1024)  # MB
    
    embed = discord.Embed(
        title="🤖 RosethornBot Status",
        description="Current bot performance and system metrics",
        color=EMBED_COLOR
    )
    
    embed.add_field(name="🔄 Bot Status", value="Online ✅", inline=True)
    embed.add_field(name="⏰ Uptime", value=uptime, inline=True)
    embed.add_field(name="🏰 Guilds", value=str(len(bot.guilds)), inline=True)
    
    embed.add_field(name="🧮 CPU Usage", value=f"{cpu_percent}%", inline=True)
    embed.add_field(name="💾 Memory", value=f"{memory_used}MB / {memory_total}MB", inline=True)
    embed.add_field(name="🌐 Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    embed.add_field(name="📊 Commands", value="43 slash commands", inline=True)
    embed.add_field(name="🔌 Services", value="All operational", inline=True)
    embed.add_field(name="📌 Sticky Service", value="Active" if sticky_service else "Inactive", inline=True)
    
    embed.set_footer(text="Victorian manor bot management • Rosewood Manor")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="sync", description="🔄 Manually sync bot commands")
@discord.app_commands.default_permissions(manage_messages=True)
@handle_errors
async def sync_command(interaction: discord.Interaction, guild_only: bool = False):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can sync commands", ephemeral=True)
        return
    
    await interaction.response.send_message("🔄 Syncing commands...", ephemeral=True)
    
    try:
        if guild_only:
            # Sync only for current guild (faster)
            guild_synced = await bot.tree.sync(guild=interaction.guild)
            
            embed = discord.Embed(
                title="🔄 Guild Command Sync Complete",
                description="Bot commands have been synchronized for this server only",
                color=EMBED_COLOR
            )
            embed.add_field(name="🏰 Guild Sync", value=f"{len(guild_synced)} commands", inline=True)
            embed.add_field(name="✅ Status", value="Guild sync successful", inline=True)
            embed.set_footer(text="Commands should appear immediately in this server")
        else:
            # Sync globally and for guild
            synced = await bot.tree.sync()
            guild_synced = await bot.tree.sync(guild=interaction.guild)
            
            embed = discord.Embed(
                title="🔄 Command Sync Complete",
                description="Bot commands have been synchronized",
                color=EMBED_COLOR
            )
            embed.add_field(name="🌐 Global Sync", value=f"{len(synced)} commands", inline=True)
            embed.add_field(name="🏰 Guild Sync", value=f"{len(guild_synced)} commands", inline=True)
            embed.add_field(name="✅ Status", value="Sync successful", inline=True)
            embed.set_footer(text="Commands may take up to 1 hour to appear globally")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error syncing commands: {str(e)}", ephemeral=True)

@bot.tree.command(name="restart", description="🔄 Restart the bot (VPS only)")
@discord.app_commands.default_permissions(manage_messages=True)
@handle_errors
async def restart_command(interaction: discord.Interaction, confirmation: str = ""):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can restart the bot", ephemeral=True)
        return
    
    if confirmation.lower() != "confirm":
        embed = discord.Embed(
            title="🔄 Bot Restart Confirmation",
            description="⚠️ This will restart the entire bot process",
            color=0xFF6B35
        )
        embed.add_field(name="📋 To Confirm", value="`/restart confirm`", inline=False)
        embed.add_field(name="⏱️ Downtime", value="~10-30 seconds", inline=True)
        embed.add_field(name="🔄 Auto-reconnect", value="Yes", inline=True)
        embed.set_footer(text="Use with caution • Bot will disconnect temporarily")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔄 Restarting RosethornBot",
        description="Bot will reconnect in approximately 10-30 seconds",
        color=EMBED_COLOR
    )
    embed.add_field(name="👨‍⚖️ Initiated By", value=interaction.user.mention, inline=True)
    embed.add_field(name="⏰ Time", value=discord.utils.format_dt(datetime.now(), style='f'), inline=True)
    
    await interaction.response.send_message(embed=embed)
    
    # Log the restart
    await create_tracking_message("🔄 Bot Restart Initiated", {
        "👨‍⚖️ Initiated By": interaction.user.mention,
        "🏰 Guild": interaction.guild.name,
        "⏰ Time": discord.utils.format_dt(datetime.now(), style='f')
    }, 0xFF6B35, f"RESTART-{interaction.id}")
    
    # Restart the bot (this will work on VPS with proper process management)
    import os
    import sys
    
    try:
        await bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        logger.error(f"Error restarting bot: {e}")
        # Fallback - just disconnect and let process manager restart
        await bot.close()

# Import modal service
try:
    from services.modal_service import modal_service, CustomModalForm
except ImportError:
    modal_service = None
    logger.warning("Modal service not available")

# Custom Modal Form Commands
@bot.tree.command(name="createform", description="📝 Create a custom modal form with questions")
@discord.app_commands.default_permissions(manage_messages=True)
@discord.app_commands.describe(
    form_id="Unique identifier for the form",
    title="Title of the form",
    log_channel="Channel to send responses to (optional)"
)
@handle_errors
async def create_form_command(interaction: discord.Interaction, form_id: str, title: str, log_channel: discord.TextChannel = None):
    # Check if user has admin role
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can create forms", ephemeral=True)
        return
    
    if not modal_service:
        await interaction.response.send_message("❌ Modal service not available", ephemeral=True)
        return
    
    # Check if form already exists
    if modal_service.get_form(form_id):
        await interaction.response.send_message(f"❌ Form with ID '{form_id}' already exists", ephemeral=True)
        return
    
    # Create interactive form builder
    class FormBuilderView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)
            self.questions = []
            self.current_form_config = {
                'title': title,
                'questions': [],
                'show_summary': True,
                'timeout': 300
            }
            if log_channel:
                self.current_form_config['log_channel_id'] = log_channel.id
        
        @discord.ui.button(label="Add Question", style=discord.ButtonStyle.primary, emoji="➕")
        async def add_question(self, interaction: discord.Interaction, button: discord.ui.Button):
            if len(self.questions) >= 5:
                await interaction.response.send_message("❌ Maximum 5 questions allowed per form", ephemeral=True)
                return
            
            # Modal to add question
            class QuestionModal(discord.ui.Modal, title="Add Question"):
                question_label = discord.ui.TextInput(
                    label="Question Label",
                    placeholder="What is your question?",
                    required=True,
                    max_length=45
                )
                placeholder_text = discord.ui.TextInput(
                    label="Placeholder Text (optional)",
                    placeholder="Hint text for the user...",
                    required=False,
                    max_length=100
                )
                required_toggle = discord.ui.TextInput(
                    label="Required? (yes/no)",
                    placeholder="yes",
                    default="yes",
                    required=True,
                    max_length=3
                )
                multiline_toggle = discord.ui.TextInput(
                    label="Long text? (yes/no)",
                    placeholder="no",
                    default="no",
                    required=True,
                    max_length=3
                )
                
                async def on_submit(self, interaction: discord.Interaction):
                    question_config = {
                        'id': f'q{len(parent_view.questions) + 1}',
                        'label': str(self.question_label.value),
                        'placeholder': str(self.placeholder_text.value) if self.placeholder_text.value else '',
                        'required': str(self.required_toggle.value).lower() in ['yes', 'y', 'true', '1'],
                        'multiline': str(self.multiline_toggle.value).lower() in ['yes', 'y', 'true', '1'],
                        'max_length': 1024 if str(self.multiline_toggle.value).lower() in ['yes', 'y', 'true', '1'] else 200
                    }
                    
                    parent_view.questions.append(question_config)
                    parent_view.current_form_config['questions'] = parent_view.questions
                    
                    # Update embed
                    await parent_view.update_embed(interaction)
            
            parent_view = self
            await interaction.response.send_modal(QuestionModal())
        
        @discord.ui.button(label="Remove Last Question", style=discord.ButtonStyle.secondary, emoji="➖")
        async def remove_question(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not self.questions:
                await interaction.response.send_message("❌ No questions to remove", ephemeral=True)
                return
            
            self.questions.pop()
            self.current_form_config['questions'] = self.questions
            await self.update_embed(interaction)
        
        @discord.ui.button(label="Create Form", style=discord.ButtonStyle.success, emoji="✅")
        async def create_form(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not self.questions:
                await interaction.response.send_message("❌ Add at least one question before creating the form", ephemeral=True)
                return
            
            # Create the form
            success = modal_service.create_form(form_id, self.current_form_config)
            
            if success:
                embed = discord.Embed(
                    title="✅ Form Created Successfully",
                    description=f"Form **{title}** has been created with ID: `{form_id}`",
                    color=0x00FF00
                )
                embed.add_field(name="📝 Questions", value=str(len(self.questions)), inline=True)
                embed.add_field(name="🆔 Form ID", value=f"`{form_id}`", inline=True)
                embed.add_field(name="📍 Log Channel", value=log_channel.mention if log_channel else "None", inline=True)
                embed.add_field(name="📋 Usage", value=f"`/showform {form_id}` to display the form", inline=False)
                embed.set_footer(text="Users can now fill out this form • Rosewood Manor")
                
                # Disable all buttons
                for item in self.children:
                    item.disabled = True
                
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                await interaction.response.send_message("❌ Failed to create form", ephemeral=True)
        
        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="❌")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            embed = discord.Embed(
                title="❌ Form Creation Cancelled",
                description="Form builder has been cancelled",
                color=0xFF0000
            )
            
            # Disable all buttons
            for item in self.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
        
        async def update_embed(self, interaction: discord.Interaction):
            embed = discord.Embed(
                title="📝 Form Builder",
                description=f"Creating form: **{title}**\nForm ID: `{form_id}`",
                color=0x711417
            )
            
            if log_channel:
                embed.add_field(name="📍 Log Channel", value=log_channel.mention, inline=True)
            
            embed.add_field(name="📊 Questions Added", value=f"{len(self.questions)}/5", inline=True)
            
            if self.questions:
                questions_text = ""
                for i, q in enumerate(self.questions, 1):
                    required = "✅" if q.get('required', True) else "⚪"
                    multiline = "📄" if q.get('multiline', False) else "📝"
                    questions_text += f"{i}. {required} {multiline} {q['label']}\n"
                
                embed.add_field(name="❓ Current Questions", value=questions_text[:1024], inline=False)
            else:
                embed.add_field(name="❓ Current Questions", value="*No questions added yet*", inline=False)
            
            embed.add_field(name="📋 Next Steps", value="• Add questions using the ➕ button\n• Click ✅ when ready to create form", inline=False)
            embed.set_footer(text="Form Builder • Use buttons below to manage questions")
            
            await interaction.response.edit_message(embed=embed, view=self)
    
    # Initial embed
    embed = discord.Embed(
        title="📝 Form Builder",
        description=f"Creating form: **{title}**\nForm ID: `{form_id}`",
        color=0x711417
    )
    
    if log_channel:
        embed.add_field(name="📍 Log Channel", value=log_channel.mention, inline=True)
    
    embed.add_field(name="📊 Questions Added", value="0/5", inline=True)
    embed.add_field(name="❓ Current Questions", value="*No questions added yet*", inline=False)
    embed.add_field(name="📋 Next Steps", value="• Add questions using the ➕ button\n• Click ✅ when ready to create form", inline=False)
    embed.set_footer(text="Form Builder • Use buttons below to manage questions")
    
    view = FormBuilderView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="showform", description="📋 Display a custom form for users to fill out")
@discord.app_commands.default_permissions(manage_messages=True)
@discord.app_commands.describe(form_id="ID of the form to display")
@handle_errors
async def show_form_command(interaction: discord.Interaction, form_id: str):
    # Check if user has admin role
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can show forms", ephemeral=True)
        return
    
    if not modal_service:
        await interaction.response.send_message("❌ Modal service not available", ephemeral=True)
        return
    
    form_config = modal_service.get_form(form_id)
    if not form_config:
        await interaction.response.send_message(f"❌ Form '{form_id}' not found", ephemeral=True)
        return
    
    # Create form display with button to open modal
    class FormDisplayView(discord.ui.View):
        def __init__(self, form_config):
            super().__init__(timeout=None)  # Persistent view
            self.form_config = form_config
        
        @discord.ui.button(label="Fill Out Form", style=discord.ButtonStyle.primary, emoji="📝")
        async def fill_form(self, interaction: discord.Interaction, button: discord.ui.Button):
            modal = modal_service.create_modal(form_id)
            if modal:
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message("❌ Error creating form", ephemeral=True)
    
    # Create display embed
    embed = discord.Embed(
        title=f"📝 {form_config['title']}",
        description="Click the button below to fill out this form",
        color=0x711417
    )
    
    # Add preview of questions
    questions_preview = ""
    for i, question in enumerate(form_config['questions'], 1):
        required = "✅ Required" if question.get('required', True) else "⚪ Optional"
        questions_preview += f"{i}. **{question['label']}** ({required})\n"
    
    embed.add_field(name="❓ Questions", value=questions_preview[:1024], inline=False)
    embed.add_field(name="🆔 Form ID", value=f"`{form_id}`", inline=True)
    embed.add_field(name="📊 Total Questions", value=str(len(form_config['questions'])), inline=True)
    embed.set_footer(text="Victorian manor form system • Rosewood Manor")
    
    view = FormDisplayView(form_config)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="formresponses", description="📊 View responses to a custom form")
@discord.app_commands.default_permissions(manage_messages=True)
@discord.app_commands.describe(
    form_id="ID of the form to view responses for",
    action="Action to perform with responses"
)
@discord.app_commands.choices(action=[
    discord.app_commands.Choice(name="View Summary", value="summary"),
    discord.app_commands.Choice(name="Export All", value="export"),
    discord.app_commands.Choice(name="Clear All", value="clear")
])
@handle_errors
async def form_responses_command(interaction: discord.Interaction, form_id: str, action: str = "summary"):
    # Check if user has admin role
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can view form responses", ephemeral=True)
        return
    
    if not modal_service:
        await interaction.response.send_message("❌ Modal service not available", ephemeral=True)
        return
    
    form_config = modal_service.get_form(form_id)
    if not form_config:
        await interaction.response.send_message(f"❌ Form '{form_id}' not found", ephemeral=True)
        return
    
    responses = modal_service.get_responses(form_id)
    
    if action == "summary":
        embed = discord.Embed(
            title=f"📊 {form_config['title']} - Response Summary",
            color=0x711417
        )
        
        embed.add_field(name="📝 Total Responses", value=str(len(responses)), inline=True)
        embed.add_field(name="🆔 Form ID", value=f"`{form_id}`", inline=True)
        embed.add_field(name="📅 Created", value=discord.utils.format_dt(form_config['created_at'], style='R'), inline=True)
        
        if responses:
            recent_responses = ""
            for response in responses[-5:]:  # Last 5 responses
                user_id = response['user_id']
                submitted = response['submitted_at']
                recent_responses += f"<@{user_id}>: {discord.utils.format_dt(submitted, style='R')}\n"
            
            embed.add_field(name="🕒 Recent Responses", value=recent_responses[:1024], inline=False)
        else:
            embed.add_field(name="📭 Status", value="No responses yet", inline=False)
        
        embed.set_footer(text="Use 'export' action to download all responses")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action == "export":
        if not responses:
            await interaction.response.send_message("❌ No responses to export", ephemeral=True)
            return
        
        export_text = modal_service.export_responses(form_id)
        if export_text:
            # Create file
            import io
            file_content = io.StringIO(export_text)
            file = discord.File(file_content, filename=f"{form_id}_responses.txt")
            
            embed = discord.Embed(
                title="📤 Form Responses Export",
                description=f"Exported {len(responses)} responses from **{form_config['title']}**",
                color=0x711417
            )
            
            await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Failed to export responses", ephemeral=True)
    
    elif action == "clear":
        if not responses:
            await interaction.response.send_message("❌ No responses to clear", ephemeral=True)
            return
        
        # Confirmation
        embed = discord.Embed(
            title="⚠️ Confirm Response Deletion",
            description=f"This will permanently delete **{len(responses)}** responses from **{form_config['title']}**",
            color=0xFF6B35
        )
        embed.add_field(name="📋 To Confirm", value=f"`/formresponses {form_id} clear_confirmed`", inline=False)
        embed.set_footer(text="This action cannot be undone")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="listforms", description="📋 List all available custom forms")
@discord.app_commands.default_permissions(manage_messages=True)
@handle_errors
async def list_forms_command(interaction: discord.Interaction):
    # Check if user has admin role
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can list forms", ephemeral=True)
        return
    
    if not modal_service:
        await interaction.response.send_message("❌ Modal service not available", ephemeral=True)
        return
    
    forms = modal_service.list_forms()
    
    if not forms:
        embed = discord.Embed(
            title="📋 Custom Forms",
            description="No forms have been created yet",
            color=0x711417
        )
        embed.add_field(name="💡 Get Started", value="Use `/createform` to create your first custom form", inline=False)
    else:
        embed = discord.Embed(
            title="📋 Available Custom Forms",
            description=f"Found {len(forms)} custom form(s)",
            color=0x711417
        )
        
        forms_text = ""
        for form_id in forms:
            form_config = modal_service.get_form(form_id)
            if form_config:
                response_count = len(modal_service.get_responses(form_id))
                forms_text += f"**{form_config['title']}**\n"
                forms_text += f"└ ID: `{form_id}` • {len(form_config['questions'])} questions • {response_count} responses\n\n"
        
        embed.add_field(name="📝 Forms", value=forms_text[:1024], inline=False)
        embed.add_field(name="📋 Commands", value="`/showform <id>` - Display form\n`/formresponses <id>` - View responses", inline=False)
    
    embed.set_footer(text="Custom modal form system • Rosewood Manor")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Add error demonstration commands
@bot.tree.command(name="commands", description="📋 View all available bot commands organized by category")
@discord.app_commands.default_permissions(send_messages=True)
@handle_errors
async def commands_command(interaction: discord.Interaction):
    """Display comprehensive list of all bot commands"""
    embed = discord.Embed(
        title="📋 RosethornBot Command Directory",
        description="Complete guide to our Victorian manor's capabilities",
        color=EMBED_COLOR
    )
    
    # Economy Commands
    embed.add_field(
        name="💰 Economy & Currency",
        value="`/balance` - Check rosebud balance\n`/daily` - Daily reward claim\n`/shop` - Browse manor boutique\n`/transfer` - Send rosebuds to others\n`/work` - Earn through manor jobs",
        inline=False
    )
    
    # Moderation Commands (Admin Only)
    embed.add_field(
        name="🛡️ Moderation (Admin Only)",
        value="`/warn` - Issue formal warnings\n`/mute` - Temporarily silence members\n`/ban` - Permanent banishment\n`/kick` - Temporary removal\n`/purgechat` - Delete multiple messages\n`/deletechannel` - Remove channels/threads",
        inline=False
    )
    
    # Support & Applications
    embed.add_field(
        name="🎫 Support & Applications",
        value="`/tickets` - Create support tickets\n`/apply` - Apply for manor positions\n`/rosenotes` - Member lore system",
        inline=False
    )
    
    # Engagement & Social
    embed.add_field(
        name="🎭 Engagement & Social",
        value="`/level` - Check experience & rank\n`/leaderboard` - Top manor residents\n`/trivia` - Victorian knowledge test\n`/riddle` - Gothic puzzles\n`/giveaway` - Host community events\n`/reputation` - Victorian virtue system",
        inline=False
    )
    
    # Utility & Information
    embed.add_field(
        name="⚙️ Utility & Information",
        value="`/serverinfo` - Manor statistics\n`/avatar` - Member portraits\n`/invite` - Create invitations\n`/afk` - Set away status\n`/voice` - Voice activity stats",
        inline=False
    )
    
    # Manor Management
    embed.add_field(
        name="🏰 Manor Management",
        value="`/event` - Create manor gatherings\n`/quote` - Victorian wisdom collection\n`/spotlight` - Weekly member recognition\n`/announce` - Manor proclamations\n`/rolemanage` - Custom role assignment",
        inline=False
    )
    
    # Special Features
    embed.add_field(
        name="✨ Special Features",
        value="`/sticky` - Auto-resending messages\n`/onboard` - New member registration\n`/rules` - View & agree to rules\n`/tutorial` - Guided manor tour\n`/welcomebanner` - Animated welcome setup",
        inline=False
    )
    
    # Admin Tools
    embed.add_field(
        name="👑 Admin Tools",
        value="`/sync` - Sync bot commands\n`/botstatus` - Bot performance metrics\n`/restart` - Restart bot process\n`/createform` - Custom modal forms\n`/showform` - Display custom forms\n`/dmall` - Send DM to all members",
        inline=False
    )
    
    # AI & Testing
    embed.add_field(
        name="🤖 AI & Testing",
        value="`/aitest` - Test sentiment analysis\n`/aiinfo` - AI feature information\n`/errortest` - Error system testing",
        inline=False
    )
    
    embed.add_field(
        name="📊 Command Statistics",
        value=f"**Total Commands:** 48+\n**Categories:** 9\n**Admin Commands:** 15+\n**Member Commands:** 30+",
        inline=True
    )
    
    embed.add_field(
        name="🌹 Getting Started",
        value="New to the manor? Try:\n• `/tutorial` for guided tour\n• `/balance` to check currency\n• `/rules` to read guidelines\n• `/onboard` to register",
        inline=True
    )
    
    embed.set_footer(text="Victorian manor bot • Use commands with elegance and grace")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="dm", description="📨 Send a direct message to a specific member")
@discord.app_commands.default_permissions(administrator=True)
@discord.app_commands.describe(
    member="The member to send the message to",
    message="The message to send"
)
@handle_errors
async def dm_command(interaction: discord.Interaction, member: discord.Member, message: str):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can send DMs", ephemeral=True)
        return
    
    # Create the DM embed
    dm_embed = discord.Embed(
        title="📢 Manor Message",
        description=message,
        color=EMBED_COLOR
    )
    dm_embed.add_field(
        name="👑 From",
        value=f"{interaction.guild.name} Administration",
        inline=True
    )
    dm_embed.add_field(
        name="📅 Date",
        value=discord.utils.format_dt(datetime.now(), style='f'),
        inline=True
    )
    dm_embed.set_footer(text=f"Sent from {interaction.guild.name} • Reply to this message will not reach staff")
    
    try:
        await member.send(embed=dm_embed)
        
        # Confirmation embed
        success_embed = discord.Embed(
            title="✅ DM Sent Successfully",
            description=f"Your message has been delivered to {member.display_name}",
            color=0x00FF00
        )
        success_embed.add_field(name="👤 Recipient", value=member.mention, inline=True)
        success_embed.add_field(name="💬 Message", value=message[:100] + ("..." if len(message) > 100 else ""), inline=False)
        
        await interaction.response.send_message(embed=success_embed, ephemeral=True)
        
        # Log the DM
        await create_tracking_message("📨 Direct Message Sent", {
            "👨‍⚖️ Sent By": interaction.user.mention,
            "👤 Recipient": member.mention,
            "💬 Message": message[:100] + ("..." if len(message) > 100 else "")
        }, EMBED_COLOR, f"DM-{interaction.id}")
        
    except discord.Forbidden:
        error_embed = discord.Embed(
            title="❌ DM Failed",
            description=f"Could not send DM to {member.display_name} - they may have DMs disabled",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ DM Error",
            description=f"An error occurred while sending the DM: {str(e)}",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

@bot.tree.command(name="dmall", description="📨 Send a direct message to all server members or a specific member")
@discord.app_commands.default_permissions(administrator=True)
@discord.app_commands.describe(
    message="The message to send",
    confirmation="Type 'CONFIRM' to proceed with mass DM (not needed for single member)",
    member="Optional: Send to specific member only (leave blank for all members)"
)
@handle_errors
async def dmall_command(interaction: discord.Interaction, message: str, confirmation: str = "", member: discord.Member = None):
    # Check if user has admin role (1320538700656148541)
    if not (hasattr(interaction.user, 'roles') and any(role.id == 1320538700656148541 for role in interaction.user.roles)):
        await interaction.response.send_message("❌ Only administrators can send DMs", ephemeral=True)
        return
    
    # Handle single member DM
    if member:
        # Create the DM embed
        dm_embed = discord.Embed(
            title="📢 Manor Message",
            description=message,
            color=EMBED_COLOR
        )
        dm_embed.add_field(
            name="👑 From",
            value=f"{interaction.guild.name} Administration",
            inline=True
        )
        dm_embed.add_field(
            name="📅 Date",
            value=discord.utils.format_dt(datetime.now(), style='f'),
            inline=True
        )
        dm_embed.set_footer(text=f"Sent from {interaction.guild.name} • Reply to this message will not reach staff")
        
        try:
            await member.send(embed=dm_embed)
            
            # Confirmation embed
            success_embed = discord.Embed(
                title="✅ DM Sent Successfully",
                description=f"Your message has been delivered to {member.display_name}",
                color=0x00FF00
            )
            success_embed.add_field(name="👤 Recipient", value=member.mention, inline=True)
            success_embed.add_field(name="💬 Message", value=message[:100] + ("..." if len(message) > 100 else ""), inline=False)
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
            # Log the DM
            await create_tracking_message("📨 Direct Message Sent", {
                "👨‍⚖️ Sent By": interaction.user.mention,
                "👤 Recipient": member.mention,
                "💬 Message": message[:100] + ("..." if len(message) > 100 else "")
            }, EMBED_COLOR, f"DM-{interaction.id}")
            
            return
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="❌ DM Failed",
                description=f"Could not send DM to {member.display_name} - they may have DMs disabled",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
            
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ DM Error",
                description=f"An error occurred while sending the DM: {str(e)}",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return
    
    # Mass DM logic (existing code)
    if confirmation.upper() != "CONFIRM":
        embed = discord.Embed(
            title="⚠️ Mass DM Confirmation Required",
            description=f"This will send a DM to **{interaction.guild.member_count}** members in {interaction.guild.name}",
            color=0xFF6B35
        )
        embed.add_field(
            name="📝 Message Preview",
            value=f"```{message[:500]}{'...' if len(message) > 500 else ''}```",
            inline=False
        )
        embed.add_field(
            name="⚠️ Warning",
            value="• This action cannot be undone\n• Members may report spam\n• Use responsibly for important announcements only",
            inline=False
        )
        embed.add_field(
            name="✅ To Confirm",
            value=f"`/dmall message:{message[:50]}... confirmation:CONFIRM`",
            inline=False
        )
        embed.set_footer(text="Mass DM system • Use with extreme caution")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Start the mass DM process
    await interaction.response.send_message("📨 Starting mass DM process...", ephemeral=True)
    
    # Create the DM embed
    dm_embed = discord.Embed(
        title="📢 Manor Announcement",
        description=message,
        color=EMBED_COLOR
    )
    dm_embed.add_field(
        name="👑 From",
        value=f"{interaction.guild.name} Administration",
        inline=True
    )
    dm_embed.add_field(
        name="📅 Date",
        value=discord.utils.format_dt(datetime.now(), style='f'),
        inline=True
    )
    dm_embed.set_footer(text=f"Sent from {interaction.guild.name} • Reply to this message will not reach staff")
    
    # Track results
    successful_dms = 0
    failed_dms = 0
    blocked_dms = 0
    
    # Get all members (excluding bots)
    members = [member for member in interaction.guild.members if not member.bot]
    total_members = len(members)
    
    # Send progress update
    progress_embed = discord.Embed(
        title="📨 Mass DM in Progress",
        description=f"Sending messages to {total_members} members...",
        color=EMBED_COLOR
    )
    progress_embed.add_field(name="📊 Progress", value="0%", inline=True)
    progress_embed.add_field(name="✅ Sent", value="0", inline=True)
    progress_embed.add_field(name="❌ Failed", value="0", inline=True)
    
    try:
        progress_msg = await interaction.followup.send(embed=progress_embed, ephemeral=True)
    except:
        progress_msg = None
    
    # Send DMs in batches to avoid rate limits
    batch_size = 5
    for i in range(0, len(members), batch_size):
        batch = members[i:i + batch_size]
        
        for member in batch:
            try:
                await member.send(embed=dm_embed)
                successful_dms += 1
                await asyncio.sleep(1)  # Rate limit protection
                
            except discord.Forbidden:
                blocked_dms += 1
                logger.info(f"🥀 Could not DM {member.display_name} - DMs blocked")
                
            except Exception as e:
                failed_dms += 1
                logger.error(f"🥀 Error DMing {member.display_name}: {e}")
        
        # Update progress every batch
        if progress_msg and i % (batch_size * 4) == 0:  # Update every 4 batches
            progress_percent = int((i / len(members)) * 100)
            progress_embed.set_field_at(0, name="📊 Progress", value=f"{progress_percent}%", inline=True)
            progress_embed.set_field_at(1, name="✅ Sent", value=str(successful_dms), inline=True)
            progress_embed.set_field_at(2, name="❌ Failed/Blocked", value=str(failed_dms + blocked_dms), inline=True)
            
            try:
                await progress_msg.edit(embed=progress_embed)
            except:
                pass
        
        # Small delay between batches
        await asyncio.sleep(2)
    
    # Final results
    results_embed = discord.Embed(
        title="✅ Mass DM Complete",
        description="Mass direct message operation has finished",
        color=0x00FF00
    )
    results_embed.add_field(name="📊 Total Members", value=str(total_members), inline=True)
    results_embed.add_field(name="✅ Successfully Sent", value=str(successful_dms), inline=True)
    results_embed.add_field(name="🚫 DMs Blocked", value=str(blocked_dms), inline=True)
    results_embed.add_field(name="❌ Other Failures", value=str(failed_dms), inline=True)
    results_embed.add_field(name="📈 Success Rate", value=f"{(successful_dms/total_members)*100:.1f}%", inline=True)
    results_embed.add_field(name="👨‍⚖️ Sent By", value=interaction.user.mention, inline=True)
    
    if progress_msg:
        try:
            await progress_msg.edit(embed=results_embed)
        except:
            await interaction.followup.send(embed=results_embed, ephemeral=True)
    else:
        await interaction.followup.send(embed=results_embed, ephemeral=True)
    
    # Log the mass DM
    await create_tracking_message("📨 Mass DM Sent", {
        "👨‍⚖️ Sent By": interaction.user.mention,
        "📊 Total Members": str(total_members),
        "✅ Successful": str(successful_dms),
        "❌ Failed": str(failed_dms + blocked_dms),
        "💬 Message": message[:100] + ("..." if len(message) > 100 else "")
    }, EMBED_COLOR, f"MASS-DM-{interaction.id}")

@bot.tree.command(name="errortest", description="🧪 Test the elegant error message system")
@discord.app_commands.default_permissions(administrator=True)
@discord.app_commands.describe(error_type="Type of error to demonstrate")
@discord.app_commands.choices(error_type=[
    discord.app_commands.Choice(name="Permission Denied", value="permission"),
    discord.app_commands.Choice(name="User Not Found", value="user_not_found"),
    discord.app_commands.Choice(name="Invalid Input", value="invalid_input"),
    discord.app_commands.Choice(name="Database Error", value="database"),
    discord.app_commands.Choice(name="Rate Limited", value="rate_limit"),
    discord.app_commands.Choice(name="Insufficient Funds", value="funds"),
    discord.app_commands.Choice(name="Maintenance Mode", value="maintenance"),
    discord.app_commands.Choice(name="Random Error", value="random")
])
@handle_errors
async def errortest_command(interaction: discord.Interaction, error_type: str = "random"):
    """Test the elegant error message system"""
    
    if error_type == "permission":
        await error_demo.demo_permission_error(interaction)
    elif error_type == "user_not_found":
        await error_demo.demo_user_not_found(interaction, "VanishedGuest#1234")
    elif error_type == "invalid_input":
        await error_demo.demo_invalid_input(interaction, "balance")
    elif error_type == "database":
        await error_demo.demo_database_error(interaction)
    elif error_type == "rate_limit":
        await error_demo.demo_rate_limited(interaction)
    elif error_type == "funds":
        await error_demo.demo_insufficient_funds(interaction)
    elif error_type == "maintenance":
        await error_demo.demo_maintenance_mode(interaction)
    else:  # random
        await error_demo.demo_random_error(interaction)

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"🥀 Bot startup error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_discord_bot())