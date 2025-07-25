# 🌹 RosethornBot - Victorian Gothic Discord Management

A comprehensive AI-powered Discord server management bot with an elegant Victorian Gothic aesthetic and powerful automation features.

## 🏰 Features Overview

### 🌹 Core Management
- **Economy System**: Rosebuds currency with shop, daily rewards, and transactions
- **Rosenotes**: Member lore and administrative notes system
- **Advanced Moderation**: Auto-mod, word filtering, warnings, and member management
- **Ticket System**: Customizable support tickets with status tracking
- **AFK Detection**: Member retention with automated inactive user management

### 🎭 Engagement & Social
- **Leveling System**: Member progression with Victorian ranks and achievements
- **Reaction Roles**: Automated role assignment through reactions
- **Polls & Giveaways**: Interactive community engagement tools
- **Social Media Integration**: Twitter, Facebook posting capabilities
- **Voice Features**: Text-to-speech with female voice, dynamic voice channels

### 🤖 AI & Automation
- **Personality Learning**: Adaptive AI responses based on server culture
- **Sentiment Analysis**: Monitor and respond to community mood
- **Content Summarization**: Automatic message and activity summaries
- **Smart Moderation**: AI-powered content filtering and member behavior analysis

### ⚙️ Technical Features
- **Web Dashboard**: Beautiful Victorian Gothic themed control panel
- **Discord OAuth2**: Secure authentication with role-based access
- **VPS Ready**: Optimized for easy deployment and SSH management
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Command Editing**: Live command modification through dashboard

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Discord Bot Token
- Discord OAuth2 Application

### Installation

1. **Clone and Setup**
```bash
git clone <repository>
cd rosethornbot
pip install -r requirements.txt
```

2. **Environment Variables**
```bash
export DISCORD_TOKEN="your_bot_token"
export DISCORD_CLIENT_ID="your_client_id"
export DISCORD_CLIENT_SECRET="your_client_secret"
export DATABASE_URL="postgresql://user:pass@host:port/db"
export FLASK_SECRET_KEY="your_secret_key"
```

3. **Run the Bot**
```bash
python main.py
```

The bot will start on port 5000 with both Discord bot and web dashboard running.

## 📋 Available Commands

### 💰 Economy System
- `/balance` - Check your rosebud balance and rank
- `/daily` - Claim daily rosebud allowance
- `/shop` - Browse manor boutique items
- `/transfer` - Send rosebuds to other members

### 🛡️ Moderation
- `/warn` - Issue warnings to members
- `/mute` - Temporarily mute members
- `/ban` - Remove members from the server
- `/purge` - Clean up inactive members
- `/afk` - Set away status

### 🎫 Support & Tickets
- `/ticket` - Create support tickets
- `/rosenotes` - View/add member notes (Admin)
- `/announce` - Create announcements (Admin)

### 🎭 Engagement
- `/poll` - Create interactive polls
- `/giveaway` - Host giveaways
- `/level` - Check member level and XP
- `/leaderboard` - View server rankings

### ⚙️ Utility
- `/sync` - Sync bot commands (Admin)
- `/stats` - View server statistics
- `/help` - Command help and information

## 🎨 Victorian Gothic Theme

The bot features a consistent deep red (#711417) color scheme throughout:
- Discord embeds with Victorian styling
- Gothic-themed web dashboard
- Elegant typography and manor-inspired language
- Rose and thorn emoji motifs

## 🔧 VPS Deployment

### SSH Management
The bot includes Victorian-themed SSH messages and restart capabilities:

```bash
# SSH into your VPS
ssh user@your-server.com

# Navigate to bot directory
cd /path/to/rosethornbot

# Restart bot with Gothic flair
🌹 Welcome Kate, Rosethorn Manor is up and running ⚡
```

### File Structure for Easy Deployment
```
rosethornbot/
├── main.py              # Application entry point
├── bot_simple.py        # Discord bot core
├── dashboard.py         # Web dashboard
├── models.py            # Database models
├── config.py            # Configuration
├── commands/            # Command modules
├── services/            # Business logic
├── templates/           # HTML templates
├── static/              # CSS/JS assets
└── requirements.txt     # Dependencies
```

## 🌐 Web Dashboard

Access the dashboard at `http://your-server:5000`

Features:
- Discord OAuth2 authentication
- Live command editing and management
- Server statistics and analytics
- Member management tools
- Victorian Gothic styling
- Mobile-responsive design

## 🔒 Security & Permissions

- Role-based access control
- Admin-only sensitive commands
- Secure OAuth2 implementation
- Environment variable protection
- Database security best practices

## 📊 Database Schema

The bot uses PostgreSQL with the following main tables:
- `users` - Member profiles and economy data
- `guilds` - Server configurations and settings
- `tickets` - Support ticket tracking
- `transactions` - Economy transaction history
- `moderation` - Warning and action logs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🌹 Support

For support and questions:
- Create a ticket using `/ticket` in Discord
- Check the web dashboard for documentation
- Review command help with `/help`

---

*"In the shadows of the Victorian manor, technology and elegance converge."* 🌹