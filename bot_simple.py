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

async def run_discord_bot():
    """Run the Discord bot."""
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"🥀 Bot startup error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_discord_bot())