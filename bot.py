import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio
import psutil
import os
from dotenv import load_dotenv

# ─── External Cog Imports ───
from events import setup_events
from tickets import setup_tickets
from moderation import setup_moderation
from twitchwatch import setup_twitchwatch

# ─── Logging ───
import logging
logging.basicConfig(level=logging.INFO)

# ─── Environment & Token ───
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
start_time = time.time()

# ─── Bot Setup ───
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
PRIMARY_GUILD_ID = 1308904661578813540
HEARTBEAT_CHANNEL_ID = 1394659138591526992  # ⛑️ Where alerts + startup embeds are sent

# ─── Slash Command: /heartbeat ───
@bot.tree.command(name="heartbeat", description="Check if Rosethorn is alive")
async def heartbeat(interaction: discord.Interaction):
    uptime = int(time.time() - start_time)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60

    embed = discord.Embed(
        title="💓 Rosethorn Heartbeat",
        description="My flame flickers — I am listening.",
        color=discord.Color.from_rgb(113, 20, 23)
    )
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m", inline=True)
    embed.add_field(name="Time", value=f"<t:{int(time.time())}:F>", inline=True)
    embed.set_footer(text="Rosethorn Bot | Vitality")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ─── Slash Command: /resync ───
@bot.tree.command(name="resync", description="Force Rosethorn to sync all commands")
@app_commands.guild_only()
async def resync(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Syncing slash commands...", ephemeral=True)
    try:
        await bot.tree.sync()
        await interaction.followup.send("✅ Global slash commands synced.")
    except Exception as e:
        await interaction.followup.send(f"❌ Sync failed: `{e}`")

# ─── Command: !testjoin ───
@bot.command(name="testjoin")
@commands.is_owner()
async def testjoin(ctx):
    member = ctx.author
    bot.dispatch("member_join", member)
    await ctx.send("🧪 Simulated member join.")

# ─── Setup Hook ───
@bot.event
async def setup_hook():
    await setup_events(bot)
    await setup_tickets(bot)
    await setup_moderation(bot)
    await setup_twitchwatch(bot)

    await bot.load_extension("application")
    await bot.load_extension("review_flow")
    await bot.tree.sync()

    asyncio.create_task(memory_monitor())  # ✅ Fixed loop error
    print("[Rosethorn] Slash commands globally synced.")

# ─── On Ready ───
@bot.event
async def on_ready():
    uptime = int(time.time() - start_time)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60

    embed = discord.Embed(
        title="💓 Rosethorn Awakens",
        description="My candle is lit. The manor breathes.",
        color=discord.Color.from_rgb(113, 20, 23)
    )
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m", inline=True)
    embed.add_field(name="Time", value=f"<t:{int(time.time())}:F>", inline=True)
    embed.set_footer(text="Rosethorn Bot | Heartbeat")

    channel = bot.get_channel(HEARTBEAT_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        print(f"[Rosethorn] Heartbeat sent to #{channel.name}")
    else:
        print("[Rosethorn] Heartbeat channel not found.")

# ─── Memory Watchdog ───
async def memory_monitor():
    await bot.wait_until_ready()
    process = psutil.Process()
    channel = bot.get_channel(HEARTBEAT_CHANNEL_ID)

    while not bot.is_closed():
        mem = process.memory_info().rss / (1024 * 1024)  # MB
        cpu = process.cpu_percent(interval=1)

        if mem > 300:
            msg = f"⚠️ Rosethorn memory high: {mem:.1f}MB"
            logging.warning(msg)
            if channel:
                await channel.send(msg)

        await asyncio.sleep(60)

# ─── Launch ───
bot.run(TOKEN)
