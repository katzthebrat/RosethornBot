#!/bin/bash

# 🌹 RosethornBot VPS Deployment Script
# Victorian Gothic Discord Bot Deployment

echo "🌹 Welcome to Rosethorn Manor Deployment 🌹"
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Gothic-themed functions
manor_echo() {
    echo -e "${PURPLE}🌹 $1${NC}"
}

success_echo() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning_echo() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error_echo() {
    echo -e "${RED}🥀 $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    warning_echo "Running as root. Consider using a dedicated user for security."
fi

# Update system
manor_echo "Updating the manor's foundations..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
manor_echo "Installing Python and essential packages..."
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# Create application directory
APP_DIR="/opt/rosethornbot"
manor_echo "Creating manor directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or copy application files
if [ -d ".git" ]; then
    manor_echo "Detected git repository, copying files..."
    cp -r . $APP_DIR/
else
    manor_echo "Please ensure RosethornBot files are in $APP_DIR"
fi

cd $APP_DIR

# Create virtual environment
manor_echo "Setting up Victorian Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
manor_echo "Installing manor dependencies..."
pip install -r requirements.txt

# Create systemd service
manor_echo "Creating manor service..."
sudo tee /etc/systemd/system/rosethornbot.service > /dev/null <<EOF
[Unit]
Description=RosethornBot - Victorian Gothic Discord Bot
After=network.target postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create environment file template
manor_echo "Creating environment configuration..."
tee $APP_DIR/.env.example > /dev/null <<EOF
# 🌹 RosethornBot Environment Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_CLIENT_ID=your_discord_client_id_here
DISCORD_CLIENT_SECRET=your_discord_client_secret_here
DATABASE_URL=postgresql://rosethornbot:password@localhost:5432/rosethornbot
FLASK_SECRET_KEY=your_very_secure_secret_key_here
EOF

# Setup PostgreSQL
manor_echo "Setting up manor database..."
sudo -u postgres psql -c "CREATE USER rosethornbot WITH PASSWORD 'rosethorn_password_123';"
sudo -u postgres psql -c "CREATE DATABASE rosethornbot OWNER rosethornbot;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE rosethornbot TO rosethornbot;"

# Create nginx configuration
manor_echo "Configuring manor web portal..."
sudo tee /etc/nginx/sites-available/rosethornbot > /dev/null <<EOF
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/rosethornbot /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Enable and start services
manor_echo "Starting manor services..."
sudo systemctl daemon-reload
sudo systemctl enable rosethornbot
sudo systemctl enable nginx
sudo systemctl enable postgresql

# Create restart script
manor_echo "Creating manor restart script..."
tee $APP_DIR/restart_manor.sh > /dev/null <<'EOF'
#!/bin/bash
echo "🌹 Restarting Rosethorn Manor..."
sudo systemctl restart rosethornbot
sleep 3
if systemctl is-active --quiet rosethornbot; then
    echo "✅ Manor is back online and running smoothly! 🌹"
    echo "⚡ Welcome back, the Victorian halls await your return"
else
    echo "🥀 Manor failed to restart. Check logs with: sudo journalctl -u rosethornbot -f"
fi
EOF

chmod +x $APP_DIR/restart_manor.sh

# Create status script
tee $APP_DIR/manor_status.sh > /dev/null <<'EOF'
#!/bin/bash
echo "🌹 Rosethorn Manor Status Report 🌹"
echo "=================================="

if systemctl is-active --quiet rosethornbot; then
    echo "✅ Manor Bot: Online and serving"
else
    echo "🥀 Manor Bot: Offline"
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Web Portal: Available"
else
    echo "🥀 Web Portal: Unavailable"
fi

if systemctl is-active --quiet postgresql; then
    echo "✅ Database: Connected"
else
    echo "🥀 Database: Disconnected"
fi

echo ""
echo "📊 Recent manor activity:"
sudo journalctl -u rosethornbot --since="1 hour ago" -n 5 --no-pager
EOF

chmod +x $APP_DIR/manor_status.sh

# Final instructions
success_echo "Victorian manor deployment complete! 🏰"
echo ""
echo "🔧 Next steps:"
echo "1. Copy .env.example to .env and configure your tokens:"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "2. Start the manor:"
echo "   sudo systemctl start rosethornbot"
echo ""
echo "3. Check status:"
echo "   ./manor_status.sh"
echo ""
echo "4. Restart when needed:"
echo "   ./restart_manor.sh"
echo ""
echo "🌐 Web dashboard will be available at: http://your_server_ip"
echo "📱 Bot will connect to Discord once tokens are configured"
echo ""
manor_echo "Welcome to Rosethorn Manor! May your Victorian Discord server flourish! 🌹"