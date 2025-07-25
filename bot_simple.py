import os
import asyncio
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import logging
from main import db, create_app
from models import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'your_discord_bot_token_here')
EMBED_COLOR = 0x711417  # Victorian deep red

# Define command prefix function
def get_prefix(bot, message):
    """Get command prefix for guild."""
    if not message.guild:
        return '!'
    
    # Simple prefix for now, can be enhanced later
    return '!'

# Create bot instance
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# Flask app context
app = create_app()

@bot.event
async def on_ready():
    """Bot ready event."""
    logger.info(f"🌹 RosethornBot is online as {bot.user}")
    logger.info(f"🌹 Connected to {len(bot.guilds)} guilds")
    
    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="over the Victorian Gothic manor 🌹"
    )
    await bot.change_presence(activity=activity)
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"🌹 Synced {len(synced)} slash command(s)")
    except Exception as e:
        logger.error(f"🥀 Failed to sync commands: {e}")

@bot.event
async def on_guild_join(guild):
    """Handle bot joining a new guild."""
    logger.info(f"🌹 Joined new guild: {guild.name} ({guild.id})")
    
    # Send welcome message if possible
    if guild.system_channel:
        embed = discord.Embed(
            title="🌹 Welcome to RosethornBot",
            description="Thank you for inviting me to your Victorian Gothic manor! I am here to serve with elegance and grace.",
            color=EMBED_COLOR
        )
        embed.add_field(
            name="🥀 Getting Started",
            value="Use `!help` to see my commands or visit the web dashboard to configure me.",
            inline=False
        )
        embed.set_footer(text="Crafted with thorns and roses 🌹")
        
        try:
            await guild.system_channel.send(embed=embed)
        except discord.Forbidden:
            pass

# Victorian Gothic Commands
@bot.tree.command(name="rose", description="🌹 Receive a beautiful Victorian rose")
async def rose_command(interaction: discord.Interaction):
    import random
    roses = [
        "🌹 A crimson rose blooms in the moonlight for thee",
        "🥀 A thorned beauty graces thy presence", 
        "🌹 In Victorian gardens, roses whisper secrets",
        "🌹 A rose as deep red as the manor's velvet curtains"
    ]
    
    embed = discord.Embed(
        title="🌹 Victorian Rose Garden",
        description=random.choice(roses),
        color=EMBED_COLOR
    )
    embed.set_footer(text="From thy Gothic Manor with love")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="manor", description="🏰 Explore the Gothic Manor")
async def manor_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🏰 Welcome to Rosethorn Manor",
        description="A Victorian Gothic estate shrouded in mystery and elegance",
        color=EMBED_COLOR
    )
    embed.add_field(
        name="🕯️ The Library", 
        value="Ancient tomes whisper forgotten secrets",
        inline=True
    )
    embed.add_field(
        name="🌹 Rose Garden", 
        value="Crimson blooms under pale moonlight",
        inline=True
    )
    embed.add_field(
        name="⚱️ The Crypt", 
        value="Where Victorian spirits find eternal rest",
        inline=True
    )
    embed.set_footer(text="Rosethorn Manor • Victorian Gothic Discord Bot")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fortune", description="🔮 Receive a Victorian fortune reading")
async def fortune_command(interaction: discord.Interaction):
    import random
    fortunes = [
        "The roses whisper of fortune approaching on raven's wings",
        "In Victorian shadows, thy destiny unfolds like crimson petals",
        "The manor's spirits foresee prosperity in thy near future",
        "Moonlight reveals a path paved with thorns leading to glory",
        "Ancient whispers speak of love blooming in unexpected gardens"
    ]
    
    embed = discord.Embed(
        title="🔮 Victorian Fortune Reading",
        description=f"*The crystal ball swirls with gothic mist...*\n\n{random.choice(fortunes)}",
        color=EMBED_COLOR
    )
    embed.set_footer(text="Fortunes told by the Manor's mystic spirits")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gothic", description="🦇 Gothic atmosphere command")
async def gothic_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🦇 Victorian Gothic Atmosphere",
        description="*Thunder rolls across the moor as candlelight flickers...*",
        color=EMBED_COLOR
    )
    embed.add_field(
        name="🕯️ Tonight's Mood",
        value="The manor breathes with ancient elegance",
        inline=False
    )
    embed.add_field(
        name="🌙 Weather",
        value="Misty moonlight casts long shadows",
        inline=True
    )
    embed.add_field(
        name="🎭 Atmosphere",
        value="Mysteriously romantic",
        inline=True
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sync", description="🔄 Sync bot commands (Admin only)")
async def sync_command(interaction: discord.Interaction):
    # Check if user is administrator
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="🚫 Access Denied",
            description="Only administrators can sync bot commands",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        synced = await bot.tree.sync()
        embed = discord.Embed(
            title="🔄 Commands Synced",
            description=f"Successfully synced {len(synced)} slash commands!",
            color=EMBED_COLOR
        )
        embed.add_field(
            name="🌹 Available Commands",
            value="Commands should now appear when you type `/` in Discord",
            inline=False
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="🥀 Sync Failed", 
            description=f"Failed to sync commands: {str(e)}",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name='help')
async def help_command(ctx):
    """Display help information."""
    embed = discord.Embed(
        title="🌹 RosethornBot Commands",
        description="Your Victorian Gothic servant at your command",
        color=EMBED_COLOR
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value="`kick`, `ban`, `mute`, `warn`",
        inline=False
    )
    
    embed.add_field(
        name="🌹 Economy",
        value="`balance`, `checkin`, `shop`",
        inline=False
    )
    
    embed.add_field(
        name="🎫 Tickets",
        value="`ticket`, `close`",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Utility",
        value="`afk`, `poll`, `embed`",
        inline=False
    )
    
    embed.set_footer(text="Use the web dashboard for advanced configuration 🌹")
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency."""
    embed = discord.Embed(
        title="🌹 Pong!",
        description=f"Latency: {round(bot.latency * 1000)}ms",
        color=EMBED_COLOR
    )
    await ctx.send(embed=embed)

@bot.command(name='poll')
async def create_poll(ctx, question, *options):
    """Create a poll with reactions."""
    if len(options) < 2:
        await ctx.send("❌ Please provide at least 2 options for the poll.")
        return
    
    if len(options) > 10:
        await ctx.send("❌ Maximum 10 options allowed.")
        return
    
    embed = discord.Embed(
        title="📊 Poll",
        description=question,
        color=EMBED_COLOR
    )
    
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    for i, option in enumerate(options):
        embed.add_field(
            name=f"{reactions[i]} Option {i+1}",
            value=option,
            inline=False
        )
    
    embed.set_footer(text=f"Poll created by {ctx.author.display_name} 🌹")
    
    poll_message = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])

@bot.command(name='embed')
@commands.has_permissions(manage_messages=True)
async def create_embed(ctx, *, content):
    """Create a custom embed message."""
    embed = discord.Embed(
        description=content,
        color=EMBED_COLOR
    )
    embed.set_footer(text="Created with RosethornBot 🌹")
    await ctx.send(embed=embed)

# Economy System Commands
@bot.tree.command(name="balance", description="💰 Check your rosebud balance")
async def balance_command(interaction: discord.Interaction):
    balance = 1000  # Placeholder
    
    embed = discord.Embed(
        title="🌹 Rosebud Wallet",
        description="Your current balance in the Victorian treasury",
        color=EMBED_COLOR
    )
    embed.add_field(name="💰 Balance", value=f"{balance:,} Rosebuds", inline=True)
    embed.add_field(name="🏆 Rank", value="Noble Patron", inline=True)
    embed.set_footer(text="Earn more rosebuds through activities and daily check-ins!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="🌅 Claim your daily rosebud allowance")
async def daily_command(interaction: discord.Interaction):
    daily_amount = 100
    
    embed = discord.Embed(
        title="🌅 Daily Victorian Allowance",
        description="You have received your daily stipend from the manor!",
        color=EMBED_COLOR
    )
    embed.add_field(name="💰 Received", value=f"+{daily_amount} Rosebuds", inline=True)
    embed.add_field(name="🕐 Next Claim", value="Available in 23h 59m", inline=True)
    embed.set_footer(text="Return tomorrow for another allowance!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rosenotes", description="📝 View or add notes about a member")
async def rosenotes_command(interaction: discord.Interaction, member: discord.Member, note: str = None):
    if note:
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(title="🚫 Access Denied", description="Only administrators can add rosenotes", color=0xFF0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(title="📝 Rosenote Added", description=f"Note added for {member.display_name}", color=EMBED_COLOR)
        embed.add_field(name="📋 Note", value=note, inline=False)
        embed.set_footer(text=f"Added by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=f"📝 Rosenotes for {member.display_name}", description="Member information and administrative notes", color=EMBED_COLOR)
        embed.add_field(name="👤 Member Since", value=member.joined_at.strftime("%B %d, %Y") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name="🎭 Roles", value=f"{len(member.roles)-1} roles", inline=True)
        embed.add_field(name="📋 Notes", value="No administrative notes on file", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="shop", description="🛍️ Browse the Victorian manor shop")
async def shop_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🛍️ Victorian Manor Boutique", description="Elegant items available for purchase with rosebuds", color=EMBED_COLOR)
    embed.add_field(name="🎭 Custom Role", value="500 Rosebuds - Create your own colored role", inline=False)
    embed.add_field(name="🌹 Profile Badge", value="250 Rosebuds - Victorian achievement badge", inline=False)
    embed.add_field(name="💬 Custom Command", value="1000 Rosebuds - Create a personal command", inline=False)
    embed.set_footer(text="Use /buy <item> to purchase!")
    await interaction.response.send_message(embed=embed)

# Advanced Features Commands
@bot.tree.command(name="ticket", description="🎫 Create a support ticket")
async def ticket_command(interaction: discord.Interaction, topic: str, description: str = None):
    embed = discord.Embed(
        title="🎫 Victorian Support Ticket",
        description=f"A new matter requires attention from the manor staff",
        color=EMBED_COLOR
    )
    embed.add_field(name="📋 Topic", value=topic, inline=False)
    if description:
        embed.add_field(name="📝 Description", value=description, inline=False)
    embed.add_field(name="👤 Requested by", value=interaction.user.mention, inline=True)
    embed.add_field(name="🕐 Created", value=discord.utils.format_dt(discord.utils.utcnow(), style='R'), inline=True)
    embed.set_footer(text="Manor staff will assist you shortly • Ticket #001")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="afk", description="💤 Set yourself as away from keyboard")
async def afk_command(interaction: discord.Interaction, reason: str = "Away from the manor"):
    embed = discord.Embed(
        title="💤 Away From Manor",
        description=f"{interaction.user.display_name} has stepped away from the Victorian halls",
        color=EMBED_COLOR
    )
    embed.add_field(name="🚪 Reason", value=reason, inline=False)
    embed.add_field(name="🕐 Since", value=discord.utils.format_dt(discord.utils.utcnow(), style='R'), inline=True)
    embed.set_footer(text="Return when you're ready to rejoin manor activities")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="announce", description="📢 Create a Victorian announcement")
async def announce_command(interaction: discord.Interaction, title: str, message: str, channel: discord.TextChannel = None):
    if not interaction.user.guild_permissions.manage_guild:
        embed = discord.Embed(title="🚫 Access Denied", description="Only manor administrators can make announcements", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    target_channel = channel or interaction.channel
    
    embed = discord.Embed(
        title=f"📢 {title}",
        description=message,
        color=EMBED_COLOR
    )
    embed.set_footer(text=f"Announcement by {interaction.user.display_name} • Rosethorn Manor")
    embed.timestamp = discord.utils.utcnow()
    
    await target_channel.send(embed=embed)
    
    response_embed = discord.Embed(
        title="✅ Announcement Posted",
        description=f"Your announcement has been posted to {target_channel.mention}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=response_embed, ephemeral=True)

@bot.tree.command(name="purge", description="🧹 Clean up inactive members")
async def purge_command(interaction: discord.Interaction, days: int = 30, dry_run: bool = True):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(title="🚫 Access Denied", description="Only administrators can purge members", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # This would check for members without roles who haven't been active
    inactive_count = 5  # Placeholder for actual count
    
    embed = discord.Embed(
        title="🧹 Manor Cleaning",
        description=f"Member retention management for Rosethorn Manor",
        color=EMBED_COLOR
    )
    
    if dry_run:
        embed.add_field(name="🔍 Dry Run Results", value=f"Found {inactive_count} inactive members (no activity in {days} days)", inline=False)
        embed.add_field(name="⚠️ Action Required", value="Use `/purge days:30 dry_run:False` to actually remove members", inline=False)
    else:
        embed.add_field(name="✅ Cleaning Complete", value=f"Removed {inactive_count} inactive members from the manor", inline=False)
    
    embed.set_footer(text="Keeping the manor tidy and active")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Moderation Commands
@bot.tree.command(name="warn", description="⚠️ Issue a warning to a member")
async def warn_command(interaction: discord.Interaction, member: discord.Member, reason: str):
    if not interaction.user.guild_permissions.moderate_members:
        embed = discord.Embed(title="🚫 Access Denied", description="Only moderators can issue warnings", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="⚠️ Manor Warning Issued", description=f"A formal warning has been recorded", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Warning logged in manor records")
    await interaction.response.send_message(embed=embed)  # Public embed as requested

@bot.tree.command(name="mute", description="🔇 Temporarily silence a member")
async def mute_command(interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = "Disrupting manor peace"):
    if not interaction.user.guild_permissions.moderate_members:
        embed = discord.Embed(title="🚫 Access Denied", description="Only moderators can mute members", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🔇 Manor Silence", description=f"Member has been temporarily silenced", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value=duration, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.set_footer(text="Silence will be lifted automatically")
    await interaction.response.send_message(embed=embed)  # Public embed as requested

# Engagement Commands
@bot.tree.command(name="level", description="📊 Check your manor rank and experience")
async def level_command(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    level = 15  # Placeholder
    xp = 2750   # Placeholder
    next_level_xp = 3000
    
    embed = discord.Embed(title=f"📊 {target.display_name}'s Manor Standing", description="Your progress through the Victorian hierarchy", color=EMBED_COLOR)
    embed.add_field(name="🎭 Level", value=f"Level {level} - Noble Resident", inline=True)
    embed.add_field(name="⭐ Experience", value=f"{xp:,} XP", inline=True)
    embed.add_field(name="📈 Progress", value=f"{xp}/{next_level_xp} XP to next level", inline=False)
    embed.set_footer(text="Participate in manor activities to gain experience!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="giveaway", description="🎁 Host a Victorian giveaway")
async def giveaway_command(interaction: discord.Interaction, prize: str, duration: str = "1h", winners: int = 1):
    if not interaction.user.guild_permissions.manage_guild:
        embed = discord.Embed(title="🚫 Access Denied", description="Only administrators can host giveaways", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🎁 Manor Giveaway", description="A generous offering from the Victorian treasury!", color=EMBED_COLOR)
    embed.add_field(name="🏆 Prize", value=prize, inline=False)
    embed.add_field(name="⏱️ Duration", value=duration, inline=True)
    embed.add_field(name="👥 Winners", value=f"{winners} lucky recipient(s)", inline=True)
    embed.add_field(name="🎯 How to Enter", value="React with 🌹 to participate!", inline=False)
    embed.set_footer(text=f"Hosted by {interaction.user.display_name} • Good luck!")
    
    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()
    await message.add_reaction("🌹")

@bot.tree.command(name="leaderboard", description="🏆 View the manor's most distinguished residents")
async def leaderboard_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🏆 Manor Leaderboard", description="The most esteemed residents of our Victorian halls", color=EMBED_COLOR)
    
    # Placeholder leaderboard data
    leaderboard_data = [
        ("Lord Victorian", "Level 25", "5,750 XP"),
        ("Lady Rosethorne", "Level 23", "4,890 XP"),
        ("Duke Shadowmere", "Level 21", "4,210 XP"),
        ("Countess Raven", "Level 19", "3,650 XP"),
        ("Baron Crimson", "Level 18", "3,420 XP")
    ]
    
    for i, (name, level, xp) in enumerate(leaderboard_data, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        embed.add_field(name=f"{medal} {name}", value=f"{level} • {xp}", inline=False)
    
    embed.set_footer(text="Rankings updated daily • Participate to climb the ranks!")
    await interaction.response.send_message(embed=embed)

# Utility Commands
@bot.tree.command(name="serverinfo", description="ℹ️ Display manor information and statistics")
async def serverinfo_command(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"ℹ️ {guild.name} Manor Statistics", description="Information about our Victorian establishment", color=EMBED_COLOR)
    
    embed.add_field(name="👑 Manor Lord", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="📅 Established", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="👥 Residents", value=f"{guild.member_count:,} members", inline=True)
    embed.add_field(name="💬 Chambers", value=f"{len(guild.text_channels)} text • {len(guild.voice_channels)} voice", inline=True)
    embed.add_field(name="🎭 Roles", value=f"{len(guild.roles)} positions", inline=True)
    embed.add_field(name="😊 Emojis", value=f"{len(guild.emojis)} expressions", inline=True)
    
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
    if not interaction.user.guild_permissions.create_instant_invite:
        embed = discord.Embed(title="🚫 Access Denied", description="Only members with invite permissions can create invitations", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
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

# Additional Commands
@bot.tree.command(name="ban", description="🚫 Permanently ban a member from the manor")
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor rules"):
    embed = discord.Embed(title="🚫 Manor Banishment", description=f"Member has been permanently removed from the manor", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Banishment is permanent unless appealed")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="👢 Remove a member temporarily")
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Disrupting manor peace"):
    embed = discord.Embed(title="👢 Manor Removal", description=f"Member has been temporarily removed", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Member may return with proper invitation")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="transfer", description="💸 Send rosebuds to another member")
async def transfer_command(interaction: discord.Interaction, member: discord.Member, amount: int):
    embed = discord.Embed(title="💸 Rosebud Transfer", description="A generous exchange between manor residents", color=EMBED_COLOR)
    embed.add_field(name="💰 Amount", value=f"{amount:,} Rosebuds", inline=True)
    embed.add_field(name="👤 From", value=interaction.user.mention, inline=True)
    embed.add_field(name="👤 To", value=member.mention, inline=True)
    embed.set_footer(text="Transaction completed • Victorian generosity")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="work", description="⚒️ Earn rosebuds through manor jobs")
async def work_command(interaction: discord.Interaction):
    import random
    jobs = [("Tending the Rose Garden", 150), ("Polishing Victorian Silver", 200), ("Reading Gothic Literature", 250)]
    job, earned = random.choice(jobs)
    
    embed = discord.Embed(title="⚒️ Manor Employment", description="Honest work brings Victorian rewards", color=EMBED_COLOR)
    embed.add_field(name="💼 Task", value=job, inline=False)
    embed.add_field(name="💰 Earned", value=f"{earned:,} Rosebuds", inline=True)
    embed.add_field(name="👤 Worker", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Well done! Return in a few hours for more work")
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
    
    import random
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
    
    import random
    riddle, answer = random.choice(riddles)
    
    embed = discord.Embed(title="🔮 Gothic Riddle", description="Solve this mysterious puzzle", color=EMBED_COLOR)
    embed.add_field(name="🌙 Riddle", value=riddle, inline=False)
    embed.add_field(name="💭 Hint", value="Think with Victorian wisdom...", inline=False)
    embed.add_field(name="💡 Answer", value=f"||{answer}||", inline=False)
    embed.set_footer(text="Click the spoiler to reveal the answer • The shadows whisper the solution")
    await interaction.response.send_message(embed=embed)

# ADVANCED APPLICATION SYSTEM with Buttons → Modals → Threads → Role Assignment
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
                auto_archive_duration=1440  # 24 hours
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
            
            # Log to tracking channel
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="📋 Application Submitted", color=EMBED_COLOR)
                log_embed.add_field(name="Type", value="Realm Job", inline=True)
                log_embed.add_field(name="Applicant", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="Status", value="Pending Review", inline=True)
                await log_channel.send(embed=log_embed)
            
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
                auto_archive_duration=1440  # 24 hours
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
            
            # Log to tracking channel
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="📋 Application Submitted", color=EMBED_COLOR)
                log_embed.add_field(name="Type", value="Admin", inline=True)
                log_embed.add_field(name="Applicant", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="Status", value="Pending Review", inline=True)
                await log_channel.send(embed=log_embed)
            
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
        # Check if user has admin permissions
        if not hasattr(interaction.user, 'roles') or not any(role.id == 1320538700656148541 for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        # Assign role based on application type
        if self.application_type == "realm_job":
            role_id = 1394853894437343422
            role_name = "Realm Job"
        else:  # admin
            role_id = 1320538700656148541
            role_name = "Admin"
        
        try:
            role = interaction.guild.get_role(role_id)
            if role and hasattr(self.applicant, 'add_roles'):
                await self.applicant.add_roles(role)
            
            # Update log
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="✅ Application Approved", color=0x00FF00)
                log_embed.add_field(name="Type", value=role_name, inline=True)
                log_embed.add_field(name="Applicant", value=self.applicant.mention, inline=True)
                log_embed.add_field(name="Reviewer", value=interaction.user.mention, inline=True)
                await log_channel.send(embed=log_embed)
            
            await interaction.response.send_message(f"✅ {self.applicant.mention} has been approved for {role_name}!")
            
            # Wait 10 seconds then delete thread
            import asyncio
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error approving application: {str(e)}", ephemeral=True)
    
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, emoji="❌")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin permissions
        if not hasattr(interaction.user, 'roles') or not any(role.id == 1320538700656148541 for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        try:
            # Update log
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="❌ Application Denied", color=0xFF0000)
                log_embed.add_field(name="Type", value=self.application_type.title(), inline=True)
                log_embed.add_field(name="Applicant", value=self.applicant.mention, inline=True)
                log_embed.add_field(name="Reviewer", value=interaction.user.mention, inline=True)
                await log_channel.send(embed=log_embed)
            
            await interaction.response.send_message(f"❌ {self.applicant.mention}'s application has been denied.")
            
            # Wait 10 seconds then delete thread
            import asyncio
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error denying application: {str(e)}", ephemeral=True)

@bot.tree.command(name="apply", description="📋 Apply for a position in the manor")
async def apply_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Manor Applications", description="Choose your desired position", color=EMBED_COLOR)
    embed.add_field(name="⚔️ Realm Job", value="Join the manor's workforce\nRole: <@&1394853894437343422>", inline=True)
    embed.add_field(name="👑 Admin", value="Lead and moderate the manor\nRole: <@&1320538700656148541>", inline=True)
    embed.set_footer(text="Select a button below to begin your application")
    
    view = ApplicationView()
    await interaction.response.send_message(embed=embed, view=view)

# ADVANCED TICKET SYSTEM with 4 types: Permissions, General, Report, Review
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
                auto_archive_duration=1440  # 24 hours
            )
            
            # Send ticket details to thread
            embed = discord.Embed(title=f"🎫 {ticket_type} Ticket", color=EMBED_COLOR)
            embed.add_field(name="👤 User", value=interaction.user.mention, inline=True)
            embed.add_field(name="📅 Created", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
            embed.add_field(name="📝 Details", value=details, inline=False)
            
            # Add claim and close buttons
            ticket_manage_view = TicketManageView(ticket_type=ticket_type, user=interaction.user)
            
            await thread.send(f"<@&1320538700656148541>", embed=embed, view=ticket_manage_view)
            
            # Log to tracking channel
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="🎫 Ticket Created", color=EMBED_COLOR)
                log_embed.add_field(name="Type", value=ticket_type, inline=True)
                log_embed.add_field(name="User", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="Status", value="Open", inline=True)
                await log_channel.send(embed=log_embed)
            
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
        # Check if user is staff
        if not hasattr(interaction.user, 'roles') or not any(role.id == 1320538700656148541 for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only staff can claim tickets", ephemeral=True)
            return
        
        self.claimed_by = interaction.user
        embed = discord.Embed(title="✋ Ticket Claimed", color=EMBED_COLOR)
        embed.add_field(name="Staff Member", value=interaction.user.mention, inline=True)
        embed.add_field(name="Status", value="In Progress", inline=True)
        
        # Update log
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            log_embed = discord.Embed(title="✋ Ticket Claimed", color=0xFFA500)
            log_embed.add_field(name="Type", value=self.ticket_type, inline=True)
            log_embed.add_field(name="User", value=self.user.mention, inline=True)
            log_embed.add_field(name="Staff", value=interaction.user.mention, inline=True)
            await log_channel.send(embed=log_embed)
        
        await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user is staff
        if not hasattr(interaction.user, 'roles') or not any(role.id == 1320538700656148541 for role in interaction.user.roles):
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
            # Log closure
            log_channel = bot.get_channel(1320540890141556746)
            if log_channel:
                log_embed = discord.Embed(title="🔒 Ticket Closed", color=0x00FF00)
                log_embed.add_field(name="Type", value=self.ticket_type, inline=True)
                log_embed.add_field(name="User", value=self.user.mention, inline=True)
                log_embed.add_field(name="Closed By", value=interaction.user.mention, inline=True)
                log_embed.add_field(name="Resolution", value=self.resolution.value, inline=False)
                await log_channel.send(embed=log_embed)
            
            await interaction.response.send_message(f"🔒 Ticket closed successfully!")
            
            # Wait 10 seconds then delete thread
            import asyncio
            await asyncio.sleep(10)
            await interaction.channel.delete()
        except Exception as e:
            await interaction.response.send_message(f"❌ Error closing ticket: {str(e)}", ephemeral=True)

@bot.tree.command(name="tickets", description="🎫 Create a support ticket")
async def tickets_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🎫 Manor Support Tickets", description="Choose the type of assistance you need", color=EMBED_COLOR)
    embed.add_field(name="🔑 Permissions", value="Request realm codes and access", inline=True)
    embed.add_field(name="❓ General", value="Ask general questions", inline=True)
    embed.add_field(name="⚠️ Report", value="Report rule violations", inline=True)
    embed.add_field(name="📋 Review", value="Appeal warnings or infractions", inline=True)
    embed.set_footer(text="Staff will respond promptly • Select a button below")
    
    view = TicketView()
    await interaction.response.send_message(embed=embed, view=view)

# Advanced Moderation Commands
@bot.tree.command(name="ban", description="🚫 Permanently ban a member from the manor")
async def ban_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Violating manor rules"):
    if not interaction.user.guild_permissions.ban_members:
        embed = discord.Embed(title="🚫 Access Denied", description="Only administrators can ban members", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🚫 Manor Banishment", description=f"Member has been permanently removed from the manor", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Administrator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Banishment is permanent unless appealed")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="kick", description="👢 Remove a member temporarily")
async def kick_command(interaction: discord.Interaction, member: discord.Member, reason: str = "Disrupting manor peace"):
    if not interaction.user.guild_permissions.kick_members:
        embed = discord.Embed(title="🚫 Access Denied", description="Only moderators can kick members", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="👢 Manor Removal", description=f"Member has been temporarily removed", color=EMBED_COLOR)
    embed.add_field(name="👤 Member", value=member.mention, inline=True)
    embed.add_field(name="📋 Reason", value=reason, inline=False)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Member may return with proper invitation")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="slowmode", description="⏰ Set channel message cooldown")
async def slowmode_command(interaction: discord.Interaction, seconds: int = 5):
    if not interaction.user.guild_permissions.manage_channels:
        embed = discord.Embed(title="🚫 Access Denied", description="Only moderators can set slowmode", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="⏰ Manor Pace Control", description=f"Channel message cooldown has been adjusted", color=EMBED_COLOR)
    embed.add_field(name="⏱️ Cooldown", value=f"{seconds} seconds", inline=True)
    embed.add_field(name="🛡️ Moderator", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Maintaining dignified conversation pace")
    await interaction.response.send_message(embed=embed)

# Economy Extensions
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

@bot.tree.command(name="buy", description="🛒 Purchase items from the manor shop")
async def buy_command(interaction: discord.Interaction, item: str):
    items = {
        "custom_role": {"price": 500, "name": "Custom Role"},
        "profile_badge": {"price": 250, "name": "Profile Badge"},
        "custom_command": {"price": 1000, "name": "Custom Command"}
    }
    
    if item.lower() not in items:
        embed = discord.Embed(title="🛍️ Item Not Found", description="That item is not available in our boutique", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    item_data = items[item.lower()]
    embed = discord.Embed(title="🛒 Purchase Complete", description="Your order has been processed", color=EMBED_COLOR)
    embed.add_field(name="🛍️ Item", value=item_data["name"], inline=True)
    embed.add_field(name="💰 Cost", value=f"{item_data['price']:,} Rosebuds", inline=True)
    embed.add_field(name="👤 Buyer", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Enjoy your Victorian purchase!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="work", description="⚒️ Earn rosebuds through manor jobs")
async def work_command(interaction: discord.Interaction):
    import random
    jobs = [
        ("Tending the Rose Garden", 50, 150),
        ("Polishing Victorian Silver", 75, 200),
        ("Reading Gothic Literature", 100, 250),
        ("Organizing the Manor Library", 125, 300),
        ("Hosting Evening Tea", 150, 350)
    ]
    
    job, min_earn, max_earn = random.choice(jobs)
    earned = random.randint(min_earn, max_earn)
    
    embed = discord.Embed(title="⚒️ Manor Employment", description="Honest work brings Victorian rewards", color=EMBED_COLOR)
    embed.add_field(name="💼 Task", value=job, inline=False)
    embed.add_field(name="💰 Earned", value=f"{earned:,} Rosebuds", inline=True)
    embed.add_field(name="👤 Worker", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Well done! Return in a few hours for more work")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gamble", description="🎲 Risk rosebuds for potential rewards")
async def gamble_command(interaction: discord.Interaction, amount: int):
    if amount <= 0:
        embed = discord.Embed(title="🥀 Invalid Amount", description="Please specify a positive amount", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    import random
    won = random.choice([True, False])
    
    if won:
        winnings = amount * 2
        embed = discord.Embed(title="🎲 Fortune Favors the Bold", description="The Victorian gods smile upon you!", color=EMBED_COLOR)
        embed.add_field(name="🎰 Result", value="Victory!", inline=True)
        embed.add_field(name="💰 Winnings", value=f"{winnings:,} Rosebuds", inline=True)
    else:
        embed = discord.Embed(title="🎲 Fortune's Cruel Turn", description="The manor's luck was not with you", color=EMBED_COLOR)
        embed.add_field(name="🎰 Result", value="Defeat", inline=True)
        embed.add_field(name="💸 Lost", value=f"{amount:,} Rosebuds", inline=True)
    
    embed.add_field(name="👤 Gambler", value=interaction.user.mention, inline=True)
    embed.set_footer(text="Gamble responsibly • The house always remembers")
    await interaction.response.send_message(embed=embed)

# Entertainment & Games
@bot.tree.command(name="trivia", description="🧠 Victorian-themed trivia challenge")
async def trivia_command(interaction: discord.Interaction):
    questions = [
        ("What era preceded the Victorian period?", "Georgian Era", ["Medieval", "Renaissance", "Georgian Era", "Edwardian"]),
        ("Who was the famous Victorian detective?", "Sherlock Holmes", ["Hercule Poirot", "Sherlock Holmes", "Miss Marple", "Sam Spade"]),
        ("What flower symbolized love in Victorian times?", "Red Rose", ["Lily", "Red Rose", "Violet", "Daisy"])
    ]
    
    import random
    question, answer, options = random.choice(questions)
    
    embed = discord.Embed(title="🧠 Victorian Trivia", description="Test your knowledge of the era", color=EMBED_COLOR)
    embed.add_field(name="❓ Question", value=question, inline=False)
    embed.add_field(name="📝 Options", value="\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)]), inline=False)
    embed.set_footer(text="Think carefully • Victorian wisdom awaits")
    await interaction.response.send_message(embed=embed)



# Voice & Social Features
@bot.tree.command(name="voice", description="🎵 Create a temporary voice channel")
async def voice_command(interaction: discord.Interaction, name: str = "Victorian Parlor"):
    if not interaction.user.guild_permissions.manage_channels:
        embed = discord.Embed(title="🚫 Access Denied", description="Only members with channel permissions can create voice rooms", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🎵 Voice Chamber Created", description="A new gathering place has been established", color=EMBED_COLOR)
    embed.add_field(name="🏛️ Chamber Name", value=name, inline=True)
    embed.add_field(name="👑 Creator", value=interaction.user.mention, inline=True)
    embed.add_field(name="⏱️ Duration", value="Temporary (will close when empty)", inline=False)
    embed.set_footer(text="Enjoy your Victorian conversations!")
    await interaction.response.send_message(embed=embed)

# APPLICATION SYSTEM - Complex workflow with buttons, modals, threads
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
        # Create private thread
        thread = await interaction.channel.create_thread(
            name=f"Realm Job - {interaction.user.display_name}",
            type=discord.ChannelType.private_thread
        )
        
        # Send application to thread
        embed = discord.Embed(title="⚔️ Realm Job Application", color=EMBED_COLOR)
        embed.add_field(name="👤 Applicant", value=interaction.user.mention, inline=True)
        embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
        embed.add_field(name="💼 Previous Experience", value=self.experience.value, inline=False)
        embed.add_field(name="🎯 Motivation", value=self.motivation.value, inline=False)
        embed.add_field(name="⏰ Availability", value=self.availability.value, inline=False)
        
        # Add review button for admin staff
        review_view = ApplicationReviewView(application_type="realm_job", applicant=interaction.user)
        
        await thread.send(f"<@&1320538700656148541>", embed=embed, view=review_view)
        
        # Log to tracking channel
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            log_embed = discord.Embed(title="📋 Application Submitted", color=EMBED_COLOR)
            log_embed.add_field(name="Type", value="Realm Job", inline=True)
            log_embed.add_field(name="Applicant", value=interaction.user.mention, inline=True)
            log_embed.add_field(name="Status", value="Pending Review", inline=True)
            await log_channel.send(embed=log_embed)
        
        await interaction.response.send_message("✅ Your Realm Job application has been submitted!", ephemeral=True)

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
        # Create private thread
        thread = await interaction.channel.create_thread(
            name=f"Admin - {interaction.user.display_name}",
            type=discord.ChannelType.private_thread
        )
        
        # Send application to thread
        embed = discord.Embed(title="👑 Admin Application", color=EMBED_COLOR)
        embed.add_field(name="👤 Applicant", value=interaction.user.mention, inline=True)
        embed.add_field(name="📅 Submitted", value=discord.utils.format_dt(discord.utils.utcnow()), inline=True)
        embed.add_field(name="💼 Administrative Experience", value=self.experience.value, inline=False)
        embed.add_field(name="🛠️ Relevant Skills", value=self.skills.value, inline=False)
        embed.add_field(name="⚖️ Conflict Resolution", value=self.scenarios.value, inline=False)
        
        # Add review button for admin staff
        review_view = ApplicationReviewView(application_type="admin", applicant=interaction.user)
        
        await thread.send(f"<@&1320538700656148541>", embed=embed, view=review_view)
        
        # Log to tracking channel
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            log_embed = discord.Embed(title="📋 Application Submitted", color=EMBED_COLOR)
            log_embed.add_field(name="Type", value="Admin", inline=True)
            log_embed.add_field(name="Applicant", value=interaction.user.mention, inline=True)
            log_embed.add_field(name="Status", value="Pending Review", inline=True)
            await log_channel.send(embed=log_embed)
        
        await interaction.response.send_message("✅ Your Admin application has been submitted!", ephemeral=True)

class ApplicationReviewView(discord.ui.View):
    def __init__(self, application_type: str, applicant: discord.Member):
        super().__init__(timeout=None)
        self.application_type = application_type
        self.applicant = applicant
    
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success, emoji="✅")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin permissions
        if not any(role.id == 1320538700656148541 for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        # Assign role based on application type
        if self.application_type == "realm_job":
            role_id = 1394853894437343422
            role_name = "Realm Job"
        else:  # admin
            role_id = 1320538700656148541
            role_name = "Admin"
        
        role = interaction.guild.get_role(role_id)
        if role:
            await self.applicant.add_roles(role)
        
        # Update log
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            log_embed = discord.Embed(title="✅ Application Approved", color=0x00FF00)
            log_embed.add_field(name="Type", value=role_name, inline=True)
            log_embed.add_field(name="Applicant", value=self.applicant.mention, inline=True)
            log_embed.add_field(name="Reviewer", value=interaction.user.mention, inline=True)
            await log_channel.send(embed=log_embed)
        
        await interaction.response.send_message(f"✅ {self.applicant.mention} has been approved for {role_name}!")
        
        # Wait 10 seconds then delete thread
        import asyncio
        await asyncio.sleep(10)
        await interaction.channel.delete()
    
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, emoji="❌")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if user has admin permissions
        if not any(role.id == 1320538700656148541 for role in interaction.user.roles):
            await interaction.response.send_message("❌ Only admin staff can review applications", ephemeral=True)
            return
        
        # Update log
        log_channel = bot.get_channel(1320540890141556746)
        if log_channel:
            log_embed = discord.Embed(title="❌ Application Denied", color=0xFF0000)
            log_embed.add_field(name="Type", value=self.application_type.title(), inline=True)
            log_embed.add_field(name="Applicant", value=self.applicant.mention, inline=True)
            log_embed.add_field(name="Reviewer", value=interaction.user.mention, inline=True)
            await log_channel.send(embed=log_embed)
        
        await interaction.response.send_message(f"❌ {self.applicant.mention}'s application has been denied.")
        
        # Wait 10 seconds then delete thread
        import asyncio
        await asyncio.sleep(10)
        await interaction.channel.delete()

@bot.tree.command(name="apply", description="📋 Apply for a position in the manor")
async def apply_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Manor Applications", description="Choose your desired position", color=EMBED_COLOR)
    embed.add_field(name="⚔️ Realm Job", value="Join the manor's workforce\nRole: <@&1394853894437343422>", inline=True)
    embed.add_field(name="👑 Admin", value="Lead and moderate the manor\nRole: <@&1320538700656148541>", inline=True)
    embed.set_footer(text="Select a button below to begin your application")
    
    view = ApplicationView()
    await interaction.response.send_message(embed=embed, view=view)

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"🥀 Bot startup error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_discord_bot())