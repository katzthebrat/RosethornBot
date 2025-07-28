import os
import asyncio
import threading
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.serving import make_server
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "rosethorn_gothic_secret_key")
    
    # Use Replit Database if DATABASE_URL not set, fallback to SQLite
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # Use SQLite for development - this will allow the bot to start immediately
        database_url = "sqlite:///rosethorn.db"
        logger.info("🌹 Using SQLite database for development")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'dashboard.login'
    login_manager.login_message = 'Please login to access the Victorian Gothic Dashboard'
    login_manager.login_message_category = 'gothic-warning'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Simple user loader that creates user object from session
        try:
            # For now, create a simple user object for authentication
            class SimpleUser:
                def __init__(self, user_id):
                    self.id = user_id
                    self.discord_id = user_id
                    self.username = f"User_{user_id}"
                    self.is_authenticated = True
                    self.is_active = True
                    self.is_anonymous = False
                    
                def get_id(self):
                    return str(self.id)
            
            return SimpleUser(user_id)
        except:
            return None
    
    # Import models to ensure they're registered
    with app.app_context():
        import models
        try:
            db.create_all()
            logger.info("🌹 Database tables created successfully")
        except Exception as e:
            logger.error(f"🥀 Database initialization error: {e}")
            # Fallback to SQLite on any database connection failure
            logger.info("🌹 Falling back to SQLite database...")
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rosethorn_fallback.db"
            db.create_all()
            logger.info("🌹 Fallback database initialized successfully")
    

    
    # Register blueprints
    from dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    # Add health check endpoint for deployment monitoring
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
    
    return app

def init_sample_data(app):
    """Initialize sample data for testing dashboard functionality."""
    with app.app_context():
        from models import Guild, Member, Ticket, ShopItem
        
        try:
            if Guild.query.count() == 0:
                # Create a sample guild for testing
                sample_guild = Guild(
                    guild_id="1234567890123456789",
                    name="Victorian Manor Test Server",
                    prefix="!",
                    embed_color="#711417",
                    currency_name="Rosebuds",
                    currency_symbol="🌹",
                    welcome_channel="1234567890123456790",
                    log_channel="1234567890123456791"
                )
                db.session.add(sample_guild)
                
                # Create sample members
                sample_member1 = Member(
                    user_id="9876543210987654321",
                    guild_id="1234567890123456789",
                    username="LadyVictoria",
                    display_name="Lady Victoria",
                    balance=2500,
                    level=15,
                    xp=3750
                )
                sample_member2 = Member(
                    user_id="1111222233334444555",
                    guild_id="1234567890123456789",
                    username="LordEdward", 
                    display_name="Lord Edward",
                    balance=1800,
                    level=12,
                    xp=2400
                )
                db.session.add_all([sample_member1, sample_member2])
                
                # Create sample tickets
                sample_ticket1 = Ticket(
                    guild_id="1234567890123456789",
                    user_id="9876543210987654321",
                    subject="Need help with manor etiquette",
                    description="I'm new to the manor and need guidance on proper Victorian behavior.",
                    category="general",
                    status="open",
                    priority="normal",
                    channel_id="1234567890123456792"
                )
                sample_ticket2 = Ticket(
                    guild_id="1234567890123456789",
                    user_id="1111222233334444555",
                    subject="Application for Butler position",
                    description="I would like to apply for the Butler role in the manor.",
                    category="application",
                    status="in_progress",
                    priority="high",
                    channel_id="1234567890123456793"
                )
                db.session.add_all([sample_ticket1, sample_ticket2])
                
                # Create sample shop items
                shop_item1 = ShopItem(
                    guild_id="1234567890123456789",
                    name="Victorian Tea Set",
                    description="An elegant porcelain tea set for proper afternoon tea.",
                    price=500,
                    rarity="rare",
                    emoji="🫖",
                    stock=5
                )
                shop_item2 = ShopItem(
                    guild_id="1234567890123456789",
                    name="Gothic Rose Bouquet", 
                    description="A mysterious bouquet of deep red roses.",
                    price=150,
                    rarity="common",
                    emoji="🌹",
                    stock=-1
                )
                shop_item3 = ShopItem(
                    guild_id="1234567890123456789",
                    name="Manor Lord's Crown",
                    description="A prestigious crown reserved for the most distinguished residents.",
                    price=10000,
                    rarity="legendary",
                    emoji="👑",
                    stock=1
                )
                db.session.add_all([shop_item1, shop_item2, shop_item3])
                
                db.session.commit()
                logger.info("🌹 Sample data added to database for testing")
        except Exception as e:
            logger.error(f"🥀 Error creating sample data: {e}")
            db.session.rollback()

def run_bot():
    """Run the Discord bot in a separate thread."""
    try:
        from bot_clean import run_discord_bot
        asyncio.run(run_discord_bot())
    except Exception as e:
        logger.error(f"🥀 Discord bot error: {e}")

def run_flask_app():
    """Run the Flask web application."""
    app = create_app()
    
    # Initialize sample data after app is fully configured
    init_sample_data(app)
    
    # Start Discord bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("🌹 Discord bot started in background thread")
    
    # Run Flask app
    logger.info("🌹 Starting Victorian Gothic Dashboard on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == "__main__":
    run_flask_app()
