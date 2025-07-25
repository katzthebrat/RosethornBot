import os

# Discord Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "your_discord_bot_token_here")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "your_client_id")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "your_client_secret")

# Bot Configuration
BOT_PREFIX = "r!"
EMBED_COLOR = 0x711417  # Deep red Victorian color
BOT_NAME = "RosethornBot"
BOT_VERSION = "2.0.0"

# Web Dashboard Configuration  
REPLIT_DEV_DOMAIN = os.getenv("REPLIT_DEV_DOMAIN", "")
if REPLIT_DEV_DOMAIN:
    DASHBOARD_URL = f"https://{REPLIT_DEV_DOMAIN}"
else:
    DASHBOARD_URL = "http://localhost:5000"
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "rosethorn_gothic_secret")
DISCORD_REDIRECT_URI = f"{DASHBOARD_URL}/auth/callback"

# Social Media API Keys
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

# AI Services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rosethorn.db")

# Feature Toggles
ENABLE_AI_FEATURES = os.getenv("ENABLE_AI_FEATURES", "true").lower() == "true"
ENABLE_VOICE_FEATURES = os.getenv("ENABLE_VOICE_FEATURES", "true").lower() == "true"
ENABLE_SOCIAL_MONITORING = os.getenv("ENABLE_SOCIAL_MONITORING", "true").lower() == "true"

# Victorian Gothic Theme Settings
GOTHIC_EMOJIS = {
    "rose": "🌹",
    "thorn": "🌿",
    "candle": "🕯️",
    "skull": "💀",
    "cross": "✝️",
    "moon": "🌙",
    "star": "⭐",
    "key": "🗝️",
    "crown": "👑",
    "gem": "💎"
}

GOTHIC_MESSAGES = {
    "welcome": "Welcome to our Gothic Victorian realm, {user}... 🌹",
    "goodbye": "Farewell, {user}. May the roses remember thee... 🥀",
    "error": "Alas, something has gone awry in our Gothic manor... 🕯️",
    "success": "Thy command has been fulfilled with Victorian grace... ✨",
    "permission_denied": "Thou dost not possess the noble rank for this command... 👑"
}
