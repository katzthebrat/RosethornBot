# RosethornBot - Victorian Gothic Discord Server Management Bot

## Project Overview
A comprehensive AI-powered Discord server management bot with a beautiful Victorian Gothic theme featuring deep red (#711417) embeds and an elegant web dashboard. The bot provides complete automation features including moderation, economy, ticketing, social monitoring, and administrative tools.

## Architecture
- **Backend**: Python Flask web application with SQLAlchemy ORM
- **Bot Framework**: Discord.py with custom command system
- **Database**: PostgreSQL (configured via DATABASE_URL)
- **Frontend**: HTML templates with Gothic-themed CSS styling
- **Authentication**: Discord OAuth2 integration
- **Services**: Modular service architecture for different bot features

## Key Features
- 🌹 Victorian Gothic themed embeds with #711417 deep red color
- 🎭 Web dashboard for command editing and server management
- 🛡️ Comprehensive moderation tools and automation
- 💰 Economy system with currency and transactions
- 🎫 Advanced ticket system for user support
- 📱 Social media monitoring and integration
- 🎵 Voice channel management
- 🤖 AI-powered features and responses
- 📊 Analytics and logging system

## Current Structure
```
├── main.py                 # Application entry point and Flask setup
├── bot.py                  # Discord bot main class and configuration
├── dashboard.py            # Web dashboard routes and OAuth
├── models.py               # Database models and relationships
├── config.py               # Configuration management
├── utils.py                # Helper utilities
├── commands/               # Discord command modules
│   ├── admin.py           # Administrative commands
│   ├── moderation.py      # Moderation commands
│   ├── economy.py         # Economy system commands
│   ├── social.py          # Social features
│   ├── tickets.py         # Ticket system
│   ├── voice.py           # Voice management
│   └── fun.py             # Entertainment commands
├── services/              # Business logic services
│   ├── discord_service.py # Core Discord operations
│   ├── moderation.py      # Moderation automation
│   ├── economy_service.py # Economy management
│   ├── ticket_service.py  # Ticket handling
│   ├── ai_service.py      # AI integration
│   └── social_monitor.py  # Social media monitoring
├── templates/             # HTML templates for dashboard
└── static/                # CSS and JavaScript assets
```

## Environment Variables Required
- `DISCORD_TOKEN`: Discord bot token
- `DISCORD_CLIENT_ID`: Discord application client ID
- `DISCORD_CLIENT_SECRET`: Discord OAuth2 client secret
- `DATABASE_URL`: PostgreSQL connection string
- `FLASK_SECRET_KEY`: Flask session security key

## Recent Changes
*Date: July 25, 2025*
- Project structure analysis completed
- Documentation created for future development sessions
- Successfully pushed all project files to GitHub repository: katzthebrat/RosethornBot2.0.git

## User Preferences
*To be updated as user expresses preferences*

## Next Steps
- Awaiting user instructions for further development or modifications