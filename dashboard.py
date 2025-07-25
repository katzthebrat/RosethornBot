import os
import json
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from main import db, login_manager
from models import *
from utils import create_embed_dict, parse_duration

dashboard_bp = Blueprint('dashboard', __name__)

# Discord OAuth2 configuration  
from config import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI

# Remove duplicate user_loader (already defined in main.py)

@dashboard_bp.route('/')
def index():
    """Main dashboard page."""
    if not current_user.is_authenticated:
        return redirect(url_for('dashboard.login'))
    
    # Get real stats from database with error handling
    try:
        total_tickets = Ticket.query.count()
        total_users = Member.query.count()
        recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
    except Exception as e:
        print(f"🥀 Database error: {e}")
        total_tickets = 0
        total_users = 0
        recent_tickets = []
    
    stats = {
        'total_commands': 37,
        'total_tickets': total_tickets,
        'active_monitors': 5,
        'total_users': total_users
    }
    
    recent_commands = []  # Custom commands would go here if we had them
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_commands=recent_commands,
                         recent_tickets=recent_tickets,
                         user=current_user)

@dashboard_bp.route('/login')
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('login.html')

@dashboard_bp.route('/auth/discord')
def discord_auth():
    """Redirect to Discord OAuth2."""
    from urllib.parse import quote
    
    # URL encode the redirect URI
    encoded_redirect_uri = quote(DISCORD_REDIRECT_URI, safe='')
    
    discord_auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
    )
    
    print(f"🌹 Discord OAuth URL: {discord_auth_url}")
    print(f"🌹 Client ID: {DISCORD_CLIENT_ID}")
    print(f"🌹 Redirect URI: {DISCORD_REDIRECT_URI}")
    
    return redirect(discord_auth_url)

@dashboard_bp.route('/auth/callback')
def discord_callback():
    """Handle Discord OAuth2 callback."""
    from flask import current_app
    
    code = request.args.get('code')
    if not code:
        flash('🥀 Authentication failed', 'error')
        return redirect(url_for('dashboard.login'))
    
    # Exchange code for token
    token_data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }
    
    token_response = requests.post(
        'https://discord.com/api/oauth2/token',
        data=token_data
    )
    
    print(f"🌹 Token response status: {token_response.status_code}")
    print(f"🌹 Token response content: {token_response.text}")
    
    if token_response.status_code != 200:
        print(f"🥀 Token exchange failed: {token_response.text}")
        flash('🥀 Failed to authenticate with Discord', 'error')
        return redirect(url_for('dashboard.login'))
    
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    
    # Get user info
    user_response = requests.get(
        'https://discord.com/api/users/@me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    print(f"🌹 User response status: {user_response.status_code}")
    print(f"🌹 User response content: {user_response.text}")
    
    if user_response.status_code != 200:
        print(f"🥀 User info fetch failed: {user_response.text}")
        flash('🥀 Failed to get user information', 'error')
        return redirect(url_for('dashboard.login'))
    
    user_data = user_response.json()
    
    # Create or update user in current Flask context
    try:
        from flask import current_app
        
        # Simple login without database storage for now to test OAuth
        class SimpleUser:
            def __init__(self, discord_id, username):
                self.id = discord_id
                self.discord_id = discord_id
                self.username = username
                self.is_authenticated = True
                self.is_active = True
                self.is_anonymous = False
                
            def get_id(self):
                return str(self.id)
        
        user = SimpleUser(user_data['id'], user_data['username'])
        login_user(user)
        print(f"🌹 User {user_data['username']} logged in successfully")
        
    except Exception as e:
        print(f"🥀 Login error: {e}")
        flash('🥀 Login error occurred', 'error')
        return redirect(url_for('dashboard.login'))
    
    flash('🌹 Welcome to the Victorian Gothic Dashboard!', 'success')
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('🌹 You have been gracefully logged out', 'info')
    return redirect(url_for('dashboard.login'))

@dashboard_bp.route('/commands')
@login_required
def commands():
    """Command management page."""
    # Simplified commands without database dependency
    return render_template('commands.html', 
                         guilds=[], 
                         commands=[], 
                         selected_guild=None)

@dashboard_bp.route('/commands/create', methods=['POST'])
@login_required
def create_command():
    """Create a new custom command."""
    guild_id = request.form.get('guild_id')
    name = request.form.get('name', '').strip()
    trigger = request.form.get('trigger', '').strip()
    response = request.form.get('response', '').strip()
    embed = request.form.get('embed') == 'on'
    embed_title = request.form.get('embed_title', '').strip()
    embed_description = request.form.get('embed_description', '').strip()
    
    if not all([guild_id, name, trigger, response]):
        flash('🥀 Please fill in all required fields', 'error')
        return redirect(url_for('dashboard.commands', guild_id=guild_id))
    
    # Check if trigger already exists
    existing = CustomCommand.query.filter_by(guild_id=guild_id, trigger=trigger).first()
    if existing:
        flash('🥀 A command with that trigger already exists', 'error')
        return redirect(url_for('dashboard.commands', guild_id=guild_id))
    
    command = CustomCommand(
        guild_id=guild_id,
        name=name,
        trigger=trigger,
        response=response,
        embed=embed,
        embed_title=embed_title if embed_title else None,
        embed_description=embed_description if embed_description else None,
        created_by=current_user.discord_id
    )
    
    db.session.add(command)
    db.session.commit()
    
    flash(f'🌹 Command "{name}" created successfully!', 'success')
    return redirect(url_for('dashboard.commands', guild_id=guild_id))

@dashboard_bp.route('/commands/<int:command_id>/edit', methods=['POST'])
@login_required
def edit_command(command_id):
    """Edit an existing command."""
    command = CustomCommand.query.get_or_404(command_id)
    
    command.name = request.form.get('name', '').strip()
    command.trigger = request.form.get('trigger', '').strip()
    command.response = request.form.get('response', '').strip()
    command.embed = request.form.get('embed') == 'on'
    command.embed_title = request.form.get('embed_title', '').strip() or None
    command.embed_description = request.form.get('embed_description', '').strip() or None
    command.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash(f'🌹 Command "{command.name}" updated successfully!', 'success')
    return redirect(url_for('dashboard.commands', guild_id=command.guild_id))

@dashboard_bp.route('/commands/<int:command_id>/delete', methods=['POST'])
@login_required
def delete_command(command_id):
    """Delete a command."""
    command = CustomCommand.query.get_or_404(command_id)
    guild_id = command.guild_id
    command_name = command.name
    
    db.session.delete(command)
    db.session.commit()
    
    flash(f'🥀 Command "{command_name}" deleted', 'info')
    return redirect(url_for('dashboard.commands', guild_id=guild_id))

@dashboard_bp.route('/tickets')
@login_required
def tickets():
    """Ticket management page."""
    # Get tickets from database with error handling
    try:
        all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(50).all()
        
        # Get guild information for display
        guild_ids = list(set([ticket.guild_id for ticket in all_tickets]))
        guilds = []
        for guild_id in guild_ids:
            guild = Guild.query.filter_by(guild_id=guild_id).first()
            if guild:
                guilds.append(guild)
        
        # Filter by status if specified
        status_filter = request.args.get('status', 'all')
        if status_filter != 'all':
            tickets = [t for t in all_tickets if t.status == status_filter]
        else:
            tickets = all_tickets
    except Exception as e:
        print(f"🥀 Database error in tickets: {e}")
        tickets = []
        guilds = []
        status_filter = 'all'
    
    return render_template('tickets.html', 
                         tickets=tickets, 
                         guilds=guilds,
                         selected_guild_id=request.args.get('guild_id'),
                         status_filter=status_filter)

@dashboard_bp.route('/economy')
@login_required
def economy():
    """Economy management page."""
    # Get guild selection with error handling
    try:
        selected_guild_id = request.args.get('guild_id')
        
        # Get all guilds for selection
        guilds = Guild.query.all()
        selected_guild = None
        
        if selected_guild_id:
            selected_guild = Guild.query.filter_by(guild_id=selected_guild_id).first()
        elif guilds:
            selected_guild = guilds[0]  # Default to first guild
            selected_guild_id = selected_guild.guild_id
        
        shop_items = []
        top_earners = []
        
        if selected_guild_id:
            # Get shop items for this guild
            shop_items = ShopItem.query.filter_by(guild_id=selected_guild_id).order_by(ShopItem.price.desc()).all()
            
            # Get top earners (members with highest balance)
            top_earners = Member.query.filter_by(guild_id=selected_guild_id).order_by(Member.balance.desc()).limit(10).all()
    except Exception as e:
        print(f"🥀 Database error in economy: {e}")
        guilds = []
        selected_guild = None
        shop_items = []
        top_earners = []
        selected_guild_id = None
    
    return render_template('economy.html', 
                         guilds=guilds, 
                         guild=selected_guild, 
                         shop_items=shop_items,
                         top_earners=top_earners,
                         selected_guild_id=selected_guild_id)

@dashboard_bp.route('/api/guild/<guild_id>/config', methods=['GET', 'POST'])
@login_required
def guild_config_api(guild_id):
    """API endpoint for guild configuration."""
    guild = Guild.query.filter_by(guild_id=guild_id).first()
    if not guild:
        return jsonify({'error': 'Guild not found'}), 404
    
    if request.method == 'GET':
        return jsonify({
            'guild_id': guild.guild_id,
            'name': guild.name,
            'prefix': guild.prefix,
            'embed_color': guild.embed_color,
            'currency_name': guild.currency_name,
            'currency_symbol': guild.currency_symbol,
            'welcome_channel': guild.welcome_channel,
            'log_channel': guild.log_channel,
            'mod_role': guild.mod_role
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        
        guild.prefix = data.get('prefix', guild.prefix)
        guild.embed_color = data.get('embed_color', guild.embed_color)
        guild.currency_name = data.get('currency_name', guild.currency_name)
        guild.currency_symbol = data.get('currency_symbol', guild.currency_symbol)
        guild.welcome_channel = data.get('welcome_channel', guild.welcome_channel)
        guild.log_channel = data.get('log_channel', guild.log_channel)
        guild.mod_role = data.get('mod_role', guild.mod_role)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Configuration updated successfully!'})

@dashboard_bp.route('/api/commands/preview', methods=['POST'])
@login_required
def preview_command():
    """Preview a command before saving."""
    data = request.get_json()
    
    embed_dict = None
    if data.get('embed'):
        embed_dict = create_embed_dict(
            title=data.get('embed_title'),
            description=data.get('embed_description') or data.get('response'),
            color='#711417'
        )
    
    return jsonify({
        'success': True,
        'preview': {
            'response': data.get('response'),
            'embed': embed_dict
        }
    })

@dashboard_bp.route('/settings')
@login_required
def settings():
    """Bot settings and configuration page."""
    # Get guild selection with error handling
    try:
        selected_guild_id = request.args.get('guild_id')
        
        # Get all guilds for selection
        guilds = Guild.query.all()
        selected_guild = None
        
        if selected_guild_id:
            selected_guild = Guild.query.filter_by(guild_id=selected_guild_id).first()
        elif guilds:
            selected_guild = guilds[0]  # Default to first guild
    except Exception as e:
        print(f"🥀 Database error in settings: {e}")
        guilds = []
        selected_guild = None
        selected_guild_id = None
    
    return render_template('settings.html', 
                         guilds=guilds, 
                         guild=selected_guild,
                         selected_guild_id=selected_guild_id)

@dashboard_bp.route('/tickets/<int:ticket_id>/close', methods=['POST'])
@login_required
def close_ticket(ticket_id):
    """Close a ticket."""
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = 'closed'
    ticket.closed_at = datetime.utcnow()
    ticket.closed_by = current_user.discord_id
    
    db.session.commit()
    flash(f'🎫 Ticket #{ticket_id} has been closed', 'success')
    return redirect(url_for('dashboard.tickets'))

@dashboard_bp.route('/economy/shop/add', methods=['POST'])
@login_required  
def add_shop_item():
    """Add a new shop item."""
    guild_id = request.form.get('guild_id')
    name = request.form.get('name', '').strip()
    price = request.form.get('price', type=int)
    description = request.form.get('description', '').strip()
    rarity = request.form.get('rarity', 'common')
    emoji = request.form.get('emoji', '🎁').strip()
    stock = request.form.get('stock', type=int, default=-1)
    
    if not all([guild_id, name, price]):
        flash('🥀 Please fill in all required fields', 'error')
        return redirect(url_for('dashboard.economy', guild_id=guild_id))
    
    item = ShopItem(
        guild_id=guild_id,
        name=name,
        price=price,
        description=description,
        rarity=rarity,
        emoji=emoji,
        stock=stock
    )
    
    db.session.add(item)
    db.session.commit()
    
    flash(f'🛍️ Shop item "{name}" added successfully!', 'success')
    return redirect(url_for('dashboard.economy', guild_id=guild_id))

@dashboard_bp.route('/economy/shop/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_shop_item(item_id):
    """Delete a shop item."""
    item = ShopItem.query.get_or_404(item_id)
    guild_id = item.guild_id
    item_name = item.name
    
    db.session.delete(item)
    db.session.commit()
    
    flash(f'🗑️ Shop item "{item_name}" deleted', 'info')
    return redirect(url_for('dashboard.economy', guild_id=guild_id))

@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for dashboard statistics."""
    try:
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='open').count()
        total_members = Member.query.count()
        total_guilds = Guild.query.count()
    except Exception as e:
        print(f"🥀 Database error in API stats: {e}")
        total_tickets = 0
        open_tickets = 0
        total_members = 0
        total_guilds = 0
    
    return jsonify({
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'total_members': total_members,
        'total_guilds': total_guilds,
        'bot_status': 'online',
        'uptime': '2 days, 4 hours'
    })


# Error handlers
@dashboard_bp.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="The page you're looking for has vanished into the gothic mist."), 404

@dashboard_bp.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_message="The manor's spirits have encountered an unexpected disturbance."), 500
