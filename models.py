from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from main import db
import json

class User(UserMixin, db.Model):
    """User model for dashboard authentication."""
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    discriminator = db.Column(db.String(4), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

class Guild(db.Model):
    """Discord guild/server configuration."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    prefix = db.Column(db.String(10), default='!')
    embed_color = db.Column(db.String(7), default='#711417')  # Victorian deep red
    currency_name = db.Column(db.String(50), default='Roses')
    currency_symbol = db.Column(db.String(10), default='🌹')
    welcome_channel = db.Column(db.String(20), nullable=True)
    log_channel = db.Column(db.String(20), nullable=True)
    mod_role = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Member(db.Model):
    """Guild member data and statistics."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    guild_id = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    display_name = db.Column(db.String(80), nullable=True)
    balance = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    warnings = db.Column(db.Integer, default=0)
    reputation = db.Column(db.Integer, default=0)
    voice_minutes = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    check_in_streak = db.Column(db.Integer, default=0)
    last_check_in = db.Column(db.Date, nullable=True)
    is_afk = db.Column(db.Boolean, default=False)
    afk_reason = db.Column(db.Text, nullable=True)
    afk_since = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'guild_id'),)

class CustomCommand(db.Model):
    """Custom commands created through dashboard."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    trigger = db.Column(db.String(50), nullable=False)
    response = db.Column(db.Text, nullable=False)
    embed = db.Column(db.Boolean, default=True)
    embed_title = db.Column(db.String(256), nullable=True)
    embed_description = db.Column(db.Text, nullable=True)
    embed_color = db.Column(db.String(7), default='#711417')
    permissions = db.Column(db.Text, nullable=True)  # JSON array of role IDs
    usage_count = db.Column(db.Integer, default=0)
    created_by = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('guild_id', 'trigger'),)

class Ticket(db.Model):
    """Support ticket system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, closed
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    assigned_staff = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    embed_message_id = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    closed_by = db.Column(db.String(20), nullable=True)

class Warning(db.Model):
    """Member warning system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    moderator_id = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='normal')  # low, normal, high, severe
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)

class ShopItem(db.Model):
    """Economy shop items."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), default='general')
    rarity = db.Column(db.String(20), default='common')  # common, uncommon, rare, epic, legendary
    stock = db.Column(db.Integer, default=-1)  # -1 for unlimited
    purchasable = db.Column(db.Boolean, default=True)
    role_reward = db.Column(db.String(20), nullable=True)  # Role ID to give on purchase
    emoji = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Purchase(db.Model):
    """Purchase history."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('shop_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_cost = db.Column(db.Integer, nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    """Application system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # staff, moderator, custom
    status = db.Column(db.String(20), default='pending')  # pending, approved, denied
    questions = db.Column(db.Text, nullable=True)  # JSON of questions and answers
    reviewer_id = db.Column(db.String(20), nullable=True)
    review_notes = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

class SocialMediaConfig(db.Model):
    """Social media monitoring configuration."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    platform = db.Column(db.String(20), nullable=False)  # twitter, youtube, twitch, etc.
    username = db.Column(db.String(100), nullable=False)
    announcement_channel = db.Column(db.String(20), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    last_post_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BotLog(db.Model):
    """Bot activity and error logging."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=True)
    level = db.Column(db.String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    module = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(20), nullable=True)
    channel_id = db.Column(db.String(20), nullable=True)
    extra_data = db.Column(db.Text, nullable=True)  # JSON for additional context
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VoiceSession(db.Model):
    """Voice channel activity tracking."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

class CheckIn(db.Model):
    """Daily check-in tracking."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    streak = db.Column(db.Integer, default=1)
    reward_amount = db.Column(db.Integer, default=0)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('guild_id', 'user_id', 'date'),)

class TodoItem(db.Model):
    """Todo list system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    assigned_to = db.Column(db.String(20), nullable=True)  # Can assign to other users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

class StickyMessage(db.Model):
    """Sticky message system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), nullable=False)
    message_id = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text, nullable=False)
    embed_data = db.Column(db.Text, nullable=True)  # JSON embed data
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('channel_id'),)  # One sticky per channel

class Reputation(db.Model):
    """Reputation/Manor Standing system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    given_by = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500))
    virtue_type = db.Column(db.String(50), default='general')  # kindness, wisdom, leadership, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ManorEvent(db.Model):
    """Manor event system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20))
    max_attendees = db.Column(db.Integer, default=-1)  # -1 for unlimited
    reminder_sent = db.Column(db.Boolean, default=False)
    event_type = db.Column(db.String(50), default='social')  # social, educational, gaming
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EventRSVP(db.Model):
    """Event RSVP tracking."""
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('manor_event.id'), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='attending')  # attending, maybe, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id'),)

class VictorianQuote(db.Model):
    """Victorian wisdom and quotes."""
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(50), default='wisdom')  # wisdom, love, mystery, etc.
    rarity = db.Column(db.String(20), default='common')  # common, rare, legendary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserQuoteCollection(db.Model):
    """User's collected quotes."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('victorian_quote.id'), nullable=False)
    collected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'quote_id'),)

class MemberSpotlight(db.Model):
    """Weekly member spotlight system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    week_of = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    nominated_by = db.Column(db.String(20), nullable=False)
    spotlight_message_id = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('guild_id', 'week_of'),)

class AutoModeration(db.Model):
    """Auto-moderation configuration."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # spam, profanity, caps, etc.
    enabled = db.Column(db.Boolean, default=True)
    action = db.Column(db.String(50), default='warn')  # warn, mute, kick, ban
    threshold = db.Column(db.Integer, default=3)
    duration_minutes = db.Column(db.Integer, nullable=True)
    whitelist_roles = db.Column(db.Text, nullable=True)  # JSON array of role IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScheduledAnnouncement(db.Model):
    """Scheduled announcement system."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    schedule_type = db.Column(db.String(20), default='once')  # once, daily, weekly, monthly
    next_send = db.Column(db.DateTime, nullable=False)
    last_sent = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WelcomeBanner(db.Model):
    """Welcome banner settings and history."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)
    banner_template = db.Column(db.String(50), default="victorian_rose")
    custom_message = db.Column(db.Text, nullable=True)
    show_member_count = db.Column(db.Boolean, default=True)
    show_rules_reminder = db.Column(db.Boolean, default=True)
    include_role_assignment = db.Column(db.Boolean, default=True)
    delete_after_hours = db.Column(db.Integer, default=24)  # Auto-delete after X hours
    created_by = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class WelcomeBannerHistory(db.Model):
    """Track welcome banners sent to members."""
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.String(20), nullable=False)
    message_id = db.Column(db.String(20), nullable=True)
    banner_template = db.Column(db.String(50), nullable=False)
    member_count_at_join = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
