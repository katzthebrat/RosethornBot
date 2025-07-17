#!/bin/bash

# ────────────────────────────────────────────────
# Rosethorn Bot Setup — Ubuntu + pm2 + Node via n
# ────────────────────────────────────────────────

echo "🌿 Removing conflicting Node packages..."
sudo apt remove nodejs npm -y

echo "📦 Installing curl..."
sudo apt install curl -y

echo "🪄 Installing Node via 'n'..."
curl -L https://raw.githubusercontent.com/tj/n/master/bin/n | sudo bash -s stable

echo "✅ Verifying Node and npm versions..."
node -v
npm -v

echo "🌙 Installing pm2 globally..."
sudo npm install -g pm2

echo "🕯️ Starting Rosethorn with pm2 and watch mode..."
cd ~/RosethornBot
pm2 start bot.py --name Rosethorn --watch

echo "🔐 Configuring pm2 to auto-start on reboot..."
pm2 startup | tail -n 1 | bash
pm2 save

echo "🎉 Rosethorn is now running 24/7 under pm2 ✨"
pm2 status
