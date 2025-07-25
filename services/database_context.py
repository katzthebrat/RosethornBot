"""
Database context manager for Discord bot operations
Handles Flask app context when bot is running in separate thread
"""

import os
from contextlib import asynccontextmanager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a separate Flask app instance for database operations
db_app = None
db_instance = None

def initialize_database_context():
    """Initialize database context for Discord bot"""
    global db_app, db_instance
    
    if db_app is None:
        db_app = Flask(__name__)
        db_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        db_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db_instance = SQLAlchemy()
        db_instance.init_app(db_app)
    
    return db_app, db_instance

@asynccontextmanager
async def database_context():
    """Async context manager for database operations in Discord bot"""
    app, db = initialize_database_context()
    
    with app.app_context():
        try:
            yield db
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.remove()