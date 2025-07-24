import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = 1308904661578813540
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
STREAMERS_FILE = "streamers.json"
CHECK_INTERVAL_MINUTES = 10
ALERT_CHANNEL_ID = 1325102526143664148

class TwitchWatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.access_token = None
        self.streamers = []
        self.live_status = {}
        self.twitch_check_loop.start()

    def cog_unload(self):
        self.twitch_check_loop.cancel()

    async def get_access_token(self):
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                self.access_token = data.get("access_token")

    async def load_streamers(self):
        if os.path.exists(STREAMERS_FILE):
            with open(STREAMERS_FILE, "r") as f:
                try:
                    self.streamers = json.load(f).get("streamers", [])
                except AttributeError:
                    self.streamers = json.load(f)
        else:
            self.streamers = []

    async def save_streamers(self):
        with open(STREAMERS_FILE, "w") as f:
            json.dump({"streamers": self.streamers}, f, indent=2)

    async def fetch_stream_data(self, usernames):
        if not self.access_token:
            await self.get_access_token()
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}"
        }
        params = [("user_login", u) for u in usernames]
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                return await resp.json()

    @tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
    async def twitch_check_loop(self):
        await self.load_streamers()
        if not self.streamers:
            return

        data = await self.fetch_stream_data(self.streamers)
        live_now = data.get("data", [])
        alert_channel = self.bot.get_channel(ALERT_CHANNEL_ID)
        if not alert_channel:
            return

        for stream in live_now:
            username = stream["user_login"]
            if self.live_status.get(username):
                continue

            embed = discord.Embed(
                title=f"{stream['user_name']} is live!",
                description=stream["title"],
                url=f"https://twitch.tv/{username}",
                color=discord.Color.purple()
            )
            embed.add_field(name="Game", value=stream.get("game_name", "Unknown"))
            embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{username}-640x360.jpg")
            await alert_channel.send(embed=embed)
            self.live_status[username] = True

        online_users = [s["user_login"] for s in live_now]
        self.live_status = {u: True for u in online_users}

    @app_commands.command(name="addstreamer", description="Add a Twitch streamer to watch")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def addstreamer(self, interaction: discord.Interaction, username: str):
        await self.load_streamers()
        if username.lower() in self.streamers:
            await interaction.response.send_message(f"🔄 `{username}` is already being tracked.", ephemeral=True)
            return
        self.streamers.append(username.lower())
        await self.save_streamers()
        await interaction.response.send_message(f"✅ `{username}` added to watchlist.", ephemeral=True)

    @app_commands.command(name="removestreamer", description="Remove a Twitch streamer from watchlist")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def removestreamer(self, interaction: discord.Interaction, username: str):
        await self.load_streamers()
        try:
            self.streamers.remove(username.lower())
            await self.save_streamers()
            await interaction.response.send_message(f"🗑️ `{username}` removed from watchlist.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message(f"⚠️ `{username}` not found in watchlist.", ephemeral=True)

    @app_commands.command(name="liststreamers", description="View all tracked Twitch streamers")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def liststreamers(self, interaction: discord.Interaction):
        await self.load_streamers()
        if not self.streamers:
            await interaction.response.send_message("📭 No streamers being tracked.", ephemeral=True)
        else:
            msg = "\n".join(f"- {u}" for u in self.streamers)
            await interaction.response.send_message(f"📡 Tracking:\n{msg}", ephemeral=True)

    @app_commands.command(name="twitchsync", description="Manually refresh Twitch status")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def twitchsync(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔄 Syncing stream status...", ephemeral=True)
        await self.twitch_check_loop()

    @app_commands.command(name="testalert", description="Post a fake live alert to verify Twitch channel")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.checks.has_permissions(manage_guild=True)
    async def testalert(self, interaction: discord.Interaction):
        channel = self.bot.get_channel(ALERT_CHANNEL_ID)
        if not channel:
            await interaction.response.send_message("❌ Alert channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="StreamerTest is live!",
            description="Fake stream alert for testing purposes.",
            url="https://twitch.tv/streamertest",
            color=discord.Color.purple()
        )
        embed.add_field(name="Game", value="Testing Grounds")
        embed.set_image(url="https://static-cdn.jtvnw.net/previews-ttv/live_user_streamertest-640x360.jpg")
        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Test alert sent.", ephemeral=True)

# ─── Extension Loader ───
async def setup(bot):
    await bot.add_cog(TwitchWatch(bot))
    print("[Rosethorn] TwitchWatch cog loaded.")

    # 🔒 Guild sync
    GUILD = discord.Object(id=1308904661578813540)
    bot.tree.copy_global_to(guild=GUILD)
    await bot.tree.sync(guild=GUILD)
