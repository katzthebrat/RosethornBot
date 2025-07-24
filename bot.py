import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio
import psutil
import os
import logging
from dotenv import load_dotenv

# ─── Environment & Logging ───
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
start_time = time.time()
logging.basicConfig(level=logging.INFO)

# ─── Constants ───
PRIMARY_GUILD_ID = 1308904661578813540
HEARTBEAT_CHANNEL_ID = 1394659138591526992
EXTENSIONS = [
    "events", "tickets", "twitchwatch", "thorn", "moderation", "application",
    "review_flow", "realm_membership", "help_panel", "rosenotes", "announce", "rosestatus"
]

# ─── Intents & Bot Instance ───
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

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
resync_lock = asyncio.Lock()

@bot.tree.command(name="resync", description="Force-refresh Rosethorn's slash commands")
@app_commands.checks.has_permissions(administrator=True)
async def resync(interaction: discord.Interaction):
    if resync_lock.locked():
        await interaction.response.send_message("⏳ Already syncing — please wait a moment.", ephemeral=True)
        return

    try:
        await interaction.response.defer(thinking=True, ephemeral=True)
    except discord.NotFound:
        print("Interaction expired — skipping defer.")
        return

    async with resync_lock:
        try:
            guild = discord.Object(id=PRIMARY_GUILD_ID)
            bot.tree.clear_commands(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            await interaction.followup.send(
                f"✅ Resynced {len(synced)} command(s) at <t:{int(time.time())}:T>",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(f"❌ Sync failed: `{e}`", ephemeral=True)

# ─── Setup Hook ───
@bot.event
async def setup_hook():
    print(f"[Startup] Extension loading began at {time.strftime('%X')}")

    for cog_name in EXTENSIONS:
        try:
            await bot.load_extension(cog_name)
            print(f"[Rosethorn] Loaded extension: {cog_name}")
        except Exception as e:
            print(f"[Rosethorn] Failed to load {cog_name}: {e}")

    guild = discord.Object(id=PRIMARY_GUILD_ID)
    bot.tree.clear_commands(guild=guild)
    synced = await bot.tree.sync(guild=guild)

    print(f"[Startup] Synced {len(synced)} command(s) to guild {PRIMARY_GUILD_ID}:")
    for cmd in synced:
        print(f" - /{cmd.name} → {cmd.description}")

    asyncio.create_task(memory_monitor())

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
        print(f"[Rosethorn] Heartbeat sent to #{channel.name} at {time.strftime('%X')}")
    else:
        print("[Rosethorn] Heartbeat channel not found.")

# ─── Command: !testjoin ───
@bot.command(name="testjoin")
@commands.is_owner()
async def testjoin(ctx):
    member = ctx.author
    bot.dispatch("member_join", member)
    await ctx.send("🧪 Simulated member join.")

# ─── Memory Monitor ───
async def memory_monitor():
    await bot.wait_until_ready()
    process = psutil.Process()
    channel = bot.get_channel(HEARTBEAT_CHANNEL_ID)
    process.cpu_percent(interval=None)

    while not bot.is_closed():
        mem = process.memory_info().rss / (1024 * 1024)
        cpu = process.cpu_percent(interval=None)

        if mem > 300:
            msg = f"⚠️ Rosethorn memory high: {mem:.1f}MB"
            logging.warning(msg)
            if channel:
                await channel.send(msg)

        await asyncio.sleep(60)

# ─── Launch ───
bot.run(TOKEN)
