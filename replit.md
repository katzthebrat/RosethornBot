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

- **Custom Modal Form System Implemented**:
  - Created comprehensive custom modal form system with dynamic question builder
  - Added /createform command with interactive form builder using buttons and modals
  - Added /showform command to display forms with "Fill Out Form" button for users
  - Added /formresponses command to view, export, and manage form submissions
  - Added /listforms command to see all available custom forms
  - Forms support up to 5 questions each with customizable labels, placeholders, and requirements
  - Automatic response logging to specified channels with Victorian Gothic theming
  - Form responses can be exported as text files for analysis
  - Now 48 total commands (up from 44) with complete form creation and management

- **Simplified Sticky Messages & Bot Management Commands Added**:
  - Simplified sticky message embeds to show only title and message (removed extra channel/user info)
  - Added /botstatus command with system metrics, uptime, CPU/memory usage, and service status
  - Added /sync command for manual Discord command synchronization
  - Added /restart command for bot process restart (VPS-ready with confirmation)
  - Bot management commands include Victorian Gothic theming and admin-only access

- **Auto-Resending Sticky Message System Implemented**:
  - Fixed sticky command to automatically resend messages to keep them at bottom instead of just pinning
  - Created StickyMessageService with automatic message tracking and resending after 3 messages
  - Added comprehensive sticky management with create, remove, status, toggle, and manual resend actions
  - Sticky messages automatically delete old versions and resend with updated timestamps
  - Added real-time message counting and configurable resend threshold
  - Victorian Gothic themed auto-sticky messages with proper embed formatting
  - Service integrates with on_message event handler for automatic triggering
  - Bot now maintains 41 total commands with improved sticky functionality

- **Elegant Error Message Design System Implemented**:
  - Created comprehensive Victorian Gothic error handling system with themed error messages
  - Added ErrorType enum with 16 different error categories (permission_denied, user_not_found, database_error, etc.)
  - Implemented ErrorSeverity levels (LOW, MEDIUM, HIGH, CRITICAL) with color-coded embeds
  - Built VictorianErrorHandler class with elegant error embeds featuring recovery suggestions
  - Added ErrorTemplates with pre-built error messages for common scenarios
  - Created error demonstration system with /errortest command for testing all error types
  - Added @handle_errors decorator for automatic error handling on all commands
  - Global error handler catches all slash command errors with elegant Victorian messaging
  - Error messages include user context, severity indicators, technical details, and recovery actions
  - Bot now has sophisticated error handling with 41 commands total (added errortest command)

- **Animated Welcome Banner System Complete**:
  - Created sophisticated welcome banner service with PIL image generation
  - Added 4 Victorian-themed templates: victorian_rose, gothic_manor, elegant_throne, mystical_garden
  - Implemented automatic member avatar processing with decorative borders
  - Built welcome banner database models (WelcomeBanner, WelcomeBannerHistory)
  - Added `/welcomebanner` command with setup, status, test, and toggle actions
  - Automatic welcome banner detection and configuration on member join
  - Victorian welcome messages with randomized titles (Lady, Lord, Sir, Dame, Noble)
  - Configurable auto-deletion after specified hours
  - Successfully tested: Banner creation working (19KB images generated)
  - Bot now syncing 40 commands (up from 39, added welcomebanner command)

- **Free AI Integration Complete**:
  - Implemented completely free AI capabilities using TextBlob and VADER sentiment analysis
  - Added content moderation system with keyword detection, spam detection, and sentiment analysis
  - Created fallback system: tries OpenAI first (if available), then uses free AI as backup
  - Added `/aitest` command to demonstrate free AI sentiment analysis and moderation
  - Victorian Gothic welcome message generation with randomized templates
  - All AI features work without any API keys or external costs
  - Libraries installed: textblob, vaderSentiment for intelligent text analysis

- **Comprehensive Feature Expansion**:
  - Added reputation/virtue system with 7 Victorian manor ranks (New Arrival to Manor Lord/Lady)
  - Implemented event management with RSVP tracking and automated reminders
  - Created Victorian quote collection system with rarity-based rewards (common/rare/legendary)
  - Built voice activity tracking with participation ranks and leaderboards
  - Added weekly member spotlight system for community recognition
  - Enhanced announcement system with scheduling capabilities
  - Implemented custom role self-assignment system
  - Expanded database models with 8 new tables for advanced features

*Previous Changes:*

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

- **Enhanced Feature Set**:
  - Complete economy system (/balance, /daily, /shop, /transfer, /work)
  - Rosenotes system for member lore (/rosenotes)
  - Comprehensive ticket and application systems (/tickets, /apply)
  - Moderation tools (/warn, /mute, /ban, /kick, /purgechat, /deletechannel, /sticky)
  - Engagement features (/level, /leaderboard, /trivia)
  - Utility commands (/serverinfo, /avatar, /invite)
  - AFK detection and member management (/afk, /purge, /announce)
  - **NEW: Reputation system** (/reputation - Victorian virtue tracking with ranks)
  - **NEW: Event management** (/event - Manor gatherings with RSVP tracking)
  - **NEW: Quote collection** (/quote - Victorian wisdom with rarity system)
  - **NEW: Voice activity** (/voice - Voice channel participation tracking)
  - **NEW: Member spotlight** (/spotlight - Weekly community recognition)
  - **NEW: Role management** (/rolemanage - Self-assignable custom roles)
  - **NEW: Enhanced announcements** (/announce - Immediate and scheduled)
  - Total of 37+ Discord slash commands now available

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
✅ Reputation System (Victorian virtue tracking with 7 manor ranks)
✅ Event Management (Manor gatherings with RSVP and scheduling)
✅ Quote Collection (Victorian wisdom with rarity-based collection)
✅ Voice Activity Tracking (Participation monitoring and ranking)
✅ Member Spotlight (Weekly community recognition system)
✅ Enhanced Announcements (Immediate and scheduled messaging)
✅ Custom Role Management (Self-assignable roles and admin controls)
✅ Sticky Message System (Channel pinned message management)

## Ready for Deployment
- All core features implemented and tested
- Complete onboarding and tutorial systems operational
- VPS deployment scripts ready
- SSH integration with Gothic theming
- Comprehensive documentation provided
- 37+ Discord slash commands fully functional
- Tutorial system with Lady Rosalind guide working perfectly
- Registration and rules agreement workflows complete