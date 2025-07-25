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

- **Playful Onboarding Tutorial System**:
  - Implemented interactive tutorial with Lady Rosalind character guide
  - Created 6-step guided tour covering key commands (balance, rosenotes, trivia/8ball, tickets)
  - Added automatic progress tracking that detects when users complete tutorial steps
  - Built reward system (100 Rosebuds + Manor Initiate title upon completion)
  - Interactive UI with buttons, progress indicators, and skip functionality

- **Complete Registration & Approval Workflow**:
  - Added /onboard command with modal form (preferred name, gamertag, birthdate, referral)
  - Created approval system with individual tracking embeds that update through lifecycle
  - Approval assigns role 1311529774946193460 and changes nickname to "Preferred name [gamertag]"
  - Denial system prompts admin reason modal and DMs member with feedback
  - All submissions/approvals logged to channel 1320540890141556746

- **Rules Agreement System**:
  - Implemented /rules command displaying complete manor rules from user specifications
  - Added "I Agree" button that assigns role 1394518008570970172
  - Rules embed includes all 12 specified rules with Victorian Gothic formatting
  - Agreement tracking and logging system

- **Simplified DM Onboarding**:
  - "thorn" DM trigger sends simplified onboarding guide
  - Explains registration process and directs users to Discord server
  - Automatic logging of DM interactions for admin tracking

- **Core Features Previously Implemented**:
  - Complete economy system (/balance, /daily, /shop, /transfer, /work)
  - Rosenotes system for member lore (/rosenotes)
  - Comprehensive ticket and application systems (/tickets, /apply)
  - Moderation tools (/warn, /mute, /ban, /kick, /purgechat, /deletechannel)
  - Engagement features (/level, /leaderboard, /trivia)
  - Utility commands (/serverinfo, /avatar, /invite)
  - AFK detection and member management (/afk, /purge, /announce)
  - Total of 29+ Discord slash commands now available

- **Technical Architecture**:
  - Maintained #711417 deep red color scheme throughout
  - All commands feature Victorian Gothic theming with Lady Rosalind character
  - Individual tracking messages for each ticket/application/registration
  - Bot successfully connecting and syncing 29 commands

## User Preferences
*To be updated as user expresses preferences*

## Completed Features
✅ Economy System (Rosebuds currency, daily rewards, shop)
✅ Rosenotes System (Member lore and admin notes)
✅ Ticket System (Support tickets with tracking)
✅ AFK Detection (Member retention management)
✅ VPS Deployment (Complete deployment infrastructure)
✅ SSH Integration (Victorian Gothic themed management)
✅ Comprehensive Documentation (README, deployment guides)
✅ Victorian Gothic Theming (Consistent #711417 throughout)
✅ Playful Onboarding Tutorial (Lady Rosalind interactive guide with 6-step progression)
✅ Complete Registration Workflow (/onboard modal, admin approval/denial system)
✅ Rules Agreement System (/rules command with "I Agree" button and role assignment)
✅ Simplified DM Onboarding ("thorn" trigger for quick registration guidance)

## Ready for Deployment
- All core features implemented and tested
- Complete onboarding and tutorial systems operational
- VPS deployment scripts ready
- SSH integration with Gothic theming
- Comprehensive documentation provided
- 29 Discord slash commands fully functional
- Tutorial system with Lady Rosalind guide working perfectly
- Registration and rules agreement workflows complete