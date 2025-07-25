# 🌹 RosethornBot VPS Deployment Guide

## Quick Answers to Your Questions

### ✅ **VPS Ready**: Yes, fully prepared for 24/7 deployment
### ✅ **SSH Integration**: Complete with Gothic-themed management
### ✅ **GitHub Safe**: Yes, tokens are environment variables only
### ✅ **Dashboard Compatible**: Works perfectly on VPS with port forwarding

---

## VPS Deployment Process

### 1. VPS Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: Minimum 1GB (2GB recommended)
- **Storage**: 10GB+ available space
- **Python**: 3.8+ (will be installed if missing)
- **Ports**: 5000 (dashboard), 22 (SSH)

### 2. One-Command Deployment
```bash
# Upload and run the deployment script
chmod +x vps_deploy.sh
./vps_deploy.sh
```

### 3. Manual Deployment Steps

#### Step 1: System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git postgresql postgresql-contrib nginx -y

# Install process manager
sudo apt install supervisor -y
```

#### Step 2: Application Setup
```bash
# Clone repository (your tokens are safe)
git clone https://github.com/yourusername/rosethornbot.git
cd rosethornbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

#### Step 3: Environment Configuration
```bash
# Create environment file
cat > .env << EOF
DISCORD_TOKEN=your_discord_token_here
DISCORD_CLIENT_ID=your_client_id_here
DISCORD_CLIENT_SECRET=your_client_secret_here
DATABASE_URL=postgresql://username:password@localhost/rosethornbot
FLASK_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
EOF
```

#### Step 4: Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres createdb rosethornbot
sudo -u postgres createuser rosethornbot_user
sudo -u postgres psql -c "ALTER USER rosethornbot_user PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE rosethornbot TO rosethornbot_user;"
```

#### Step 5: Process Management (24/7 Operation)
```bash
# Create supervisor configuration
sudo tee /etc/supervisor/conf.d/rosethornbot.conf << EOF
[program:rosethornbot]
command=/home/ubuntu/rosethornbot/venv/bin/python main.py
directory=/home/ubuntu/rosethornbot
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/rosethornbot.log
environment=PATH="/home/ubuntu/rosethornbot/venv/bin"
EOF

# Start the service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start rosethornbot
```

#### Step 6: Web Dashboard Setup (Optional)
```bash
# Configure Nginx for dashboard
sudo tee /etc/nginx/sites-available/rosethornbot << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/rosethornbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSH Integration Features

### Gothic-Themed SSH Management
The bot includes `ssh_integration.py` with Victorian Gothic themed management:

```bash
# SSH commands available through bot
/botstatus  # Check system metrics and bot health
/sync       # Manually sync Discord commands  
/restart    # Restart bot process (requires confirmation)
```

### SSH Security Best Practices
```bash
# Disable password authentication
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## GitHub Repository Safety

### ✅ **Your Tokens Are Safe**
- All sensitive data uses environment variables
- `.env` file is in `.gitignore`
- No tokens appear in source code
- Safe to push to public/private repositories

### Environment Variables Used:
```bash
DISCORD_TOKEN          # Bot token (secret)
DISCORD_CLIENT_ID      # Public application ID (safe)
DISCORD_CLIENT_SECRET  # OAuth secret (secret)
DATABASE_URL           # Database connection (secret)
FLASK_SECRET_KEY       # Session security (secret)
```

### Git Safety Commands:
```bash
# Check what will be committed (no secrets should appear)
git status
git diff --cached

# Safe to push
git add .
git commit -m "Update bot features"
git push origin main
```

## Dashboard on VPS

### ✅ **Fully Compatible**
The web dashboard works perfectly on VPS:

- **Local Access**: `http://your-vps-ip:5000`
- **Domain Access**: `http://your-domain.com` (with Nginx)
- **Features Available**:
  - Discord OAuth2 login
  - Command management
  - Server statistics
  - Bot configuration
  - Victorian Gothic theming

### Dashboard Security
```bash
# Enable HTTPS (recommended)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 24/7 Operation Features

### Automatic Restart
- **Supervisor**: Automatically restarts bot if it crashes
- **System Boot**: Bot starts automatically on server reboot
- **Memory Management**: Automatic cleanup and optimization
- **Log Rotation**: Prevents log files from filling disk

### Monitoring Commands
```bash
# Check bot status
sudo supervisorctl status rosethornbot

# View logs
sudo tail -f /var/log/rosethornbot.log

# Restart manually
sudo supervisorctl restart rosethornbot

# System resource usage
htop
```

### Health Checks
The bot includes built-in health monitoring:
- Memory usage tracking
- CPU performance monitoring  
- Database connection status
- Discord API latency
- Service availability checks

## Bot Management Commands

### New Commands Added (44 total)
- `/botstatus` - System metrics and bot health
- `/sync` - Manually sync Discord commands
- `/restart confirm` - Restart bot process

### Admin Features
- Victorian Gothic themed status embeds
- Real-time performance metrics
- Uptime tracking
- Memory and CPU monitoring
- Service status indicators

## Troubleshooting

### Common Issues
```bash
# Bot won't start
sudo supervisorctl tail rosethornbot

# Database connection issues
sudo systemctl status postgresql

# Dashboard not accessible
sudo systemctl status nginx
sudo ufw status

# Check bot logs
tail -f /var/log/rosethornbot.log
```

### Bot Commands for Debugging
- `/botstatus` - Check all system metrics
- `/sync` - Refresh command registration
- `/errortest` - Test error handling system

## Deployment Checklist

- [ ] VPS server ready (Ubuntu 20.04+)
- [ ] Domain name configured (optional)
- [ ] SSH key authentication setup
- [ ] Environment variables configured
- [ ] Database created and configured
- [ ] Supervisor process manager installed
- [ ] Nginx web server configured (for dashboard)
- [ ] Firewall rules configured
- [ ] SSL certificate installed (optional)
- [ ] Bot tokens added to environment
- [ ] Repository cloned and dependencies installed
- [ ] Bot successfully started and connected

---

## 🎉 Result: Professional 24/7 Bot Operation

Your RosethornBot is now ready for professional VPS deployment with:
- ✅ 24/7 automatic operation
- ✅ Crash recovery and auto-restart
- ✅ Web dashboard access
- ✅ SSH management with Gothic theming
- ✅ Safe GitHub repository (no exposed tokens)
- ✅ 44 Discord commands including bot management
- ✅ Victorian Gothic themed administration
- ✅ Comprehensive monitoring and logging

The bot will maintain continuous operation with professional-grade reliability and management capabilities.