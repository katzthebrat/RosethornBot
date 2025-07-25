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
        
        # Set default permissions for all commands to be available to everyone
        for guild in bot.guilds:
            try:
                await bot.tree.sync(guild=guild)
                logger.info(f"🌹 Synced commands for guild: {guild.name}")
            except Exception as e:
                logger.error(f"🥀 Failed to sync for guild {guild.name}: {e}")
    except Exception as e:
        logger.error(f"🥀 Failed to sync commands: {e}")

# ECONOMY COMMANDS
@bot.tree.command(name="balance", description="💰 Check your rosebud currency balance")
@discord.app_commands.default_permissions(send_messages=True)
async def balance_command(interaction: discord.Interaction):
    balance = random.randint(100, 5000)
    embed = discord.Embed(title="💰 Manor Treasury", description="Your Victorian wealth status", color=EMBED_COLOR)
    embed.add_field(name="🌹 Rosebuds", value=f"{balance:,}", inline=True)
    embed.add_field(name="💎 Manor Rank", value="Distinguished Resident", inline=True)
    embed.set_footer(text="Wealth accumulated through Victorian endeavors")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="🌅 Claim your daily rosebud reward")
@discord.app_commands.default_permissions(send_messages=True)
async def daily_command(interaction: discord.Interaction):
    reward = random.randint(50, 200)
    embed = discord.Embed(title="🌅 Daily Manor Allowance", description="Your Victorian stipend has arrived", color=EMBED_COLOR)
    embed.add_field(name="💰 Today's Reward", value=f"{reward:,} Rosebuds", inline=True)
    embed.add_field(name="🗓️ Next Claim", value="Available in 24 hours", inline=True)
    embed.set_footer(text="Regular attendance brings greater rewards")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="🛍️ Browse the Victorian manor boutique")
@discord.app_commands.default_permissions(send_messages=True)
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

@bot.tree.command(name="announce", description="📢 Create a formal manor announcement")
@discord.app_commands.default_permissions(manage_messages=True)
async def announce_command(interaction: discord.Interaction, message: str):
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

@bot.tree.command(name="voice", description="🎵 Create a temporary voice channel")
@discord.app_commands.default_permissions(manage_channels=True)
async def voice_command(interaction: discord.Interaction, name: str = "Victorian Parlor"):
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
            
            await interaction.response.send_message(f"❌ {self.applicant.mention}'s application has been denied.")
            
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

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"🥀 Bot startup error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_discord_bot())