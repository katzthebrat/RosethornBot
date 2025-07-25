#!/usr/bin/env python3
"""
🌹 RosethornBot SSH Integration
Victorian Gothic themed SSH utilities and server management
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

class VictorianSSH:
    """Gothic-themed SSH management for RosethornBot"""
    
    def __init__(self):
        self.colors = {
            'red': '\033[0;31m',
            'green': '\033[0;32m',
            'yellow': '\033[1;33m',
            'purple': '\033[0;35m',
            'cyan': '\033[0;36m',
            'white': '\033[1;37m',
            'reset': '\033[0m'
        }
    
    def gothic_print(self, message, color='purple'):
        """Print with Victorian Gothic styling"""
        print(f"{self.colors[color]}🌹 {message}{self.colors['reset']}")
    
    def success_print(self, message):
        """Print success message"""
        print(f"{self.colors['green']}✅ {message}{self.colors['reset']}")
    
    def error_print(self, message):
        """Print error message"""
        print(f"{self.colors['red']}🥀 {message}{self.colors['reset']}")
    
    def warning_print(self, message):
        """Print warning message"""
        print(f"{self.colors['yellow']}⚠️  {message}{self.colors['reset']}")
    
    def welcome_message(self, username="Noble Guest"):
        """Display Victorian welcome message"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        print(f"""
{self.colors['purple']}
╔══════════════════════════════════════════════════════════════╗
║                    🌹 ROSETHORN MANOR 🌹                     ║
║                   Victorian Gothic Estate                    ║
╠══════════════════════════════════════════════════════════════╣
║  Welcome, {username:<44} ║
║  Current Time: {timestamp:<38} ║
║                                                              ║
║  "In shadows deep and roses red,                             ║
║   Where Victorian elegance is bred,                          ║
║   The manor's secrets you shall tend,                        ║
║   As guardian of this Gothic blend." ⚡                       ║
╚══════════════════════════════════════════════════════════════╝
{self.colors['reset']}""")
    
    def show_manor_status(self):
        """Display RosethornBot status"""
        self.gothic_print("Checking manor systems...")
        
        # Check if bot process is running
        try:
            result = subprocess.run(['systemctl', 'is-active', 'rosethornbot'], 
                                  capture_output=True, text=True)
            bot_status = result.stdout.strip()
        except:
            bot_status = "unknown"
        
        # Check if web dashboard is accessible
        try:
            result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:5000'], 
                                  capture_output=True, text=True)
            web_status = "online" if result.stdout.strip() == "200" else "offline"
        except:
            web_status = "unknown"
        
        # Check database
        try:
            result = subprocess.run(['systemctl', 'is-active', 'postgresql'], 
                                  capture_output=True, text=True)
            db_status = result.stdout.strip()
        except:
            db_status = "unknown"
        
        print(f"""
{self.colors['cyan']}┌─ Manor Status Report ─────────────────────────────┐{self.colors['reset']}
{self.colors['cyan']}│{self.colors['reset']} 🤖 Discord Bot:     {self._status_color(bot_status):<15} {self.colors['cyan']}│{self.colors['reset']}
{self.colors['cyan']}│{self.colors['reset']} 🌐 Web Dashboard:   {self._status_color(web_status):<15} {self.colors['cyan']}│{self.colors['reset']}
{self.colors['cyan']}│{self.colors['reset']} 🗄️  Database:       {self._status_color(db_status):<15} {self.colors['cyan']}│{self.colors['reset']}
{self.colors['cyan']}└───────────────────────────────────────────────────┘{self.colors['reset']}""")
    
    def _status_color(self, status):
        """Color code status messages"""
        if status == "active":
            return f"{self.colors['green']}🟢 Online{self.colors['cyan']}"
        elif status == "online":
            return f"{self.colors['green']}🟢 Running{self.colors['cyan']}"
        elif status == "inactive" or status == "offline":
            return f"{self.colors['red']}🔴 Offline{self.colors['cyan']}"
        else:
            return f"{self.colors['yellow']}🟡 Unknown{self.colors['cyan']}"
    
    def restart_bot(self):
        """Restart RosethornBot with Gothic flair"""
        self.gothic_print("Awakening the slumbering manor spirits...")
        
        try:
            # Stop the service
            subprocess.run(['sudo', 'systemctl', 'stop', 'rosethornbot'], check=True)
            self.warning_print("Manor temporarily closes its doors...")
            
            # Start the service
            subprocess.run(['sudo', 'systemctl', 'start', 'rosethornbot'], check=True)
            self.success_print("The manor awakens! Rosethorn is once again online! ⚡")
            
            # Check status
            result = subprocess.run(['systemctl', 'is-active', 'rosethornbot'], 
                                  capture_output=True, text=True)
            if result.stdout.strip() == "active":
                self.success_print("Victorian halls echo with digital life once more")
            else:
                self.error_print("The manor remains in shadows. Check the logs for mysteries...")
                
        except subprocess.CalledProcessError as e:
            self.error_print(f"Failed to restart manor: {e}")
            self.warning_print("Consider checking permissions or service configuration")
    
    def show_logs(self, lines=20):
        """Show recent bot logs with Gothic styling"""
        self.gothic_print(f"Examining the manor's recent chronicles (last {lines} entries)...")
        
        try:
            result = subprocess.run(['sudo', 'journalctl', '-u', 'rosethornbot', '-n', str(lines), '--no-pager'], 
                                  capture_output=True, text=True)
            
            print(f"\n{self.colors['cyan']}── Manor Chronicles ──{self.colors['reset']}")
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            self.error_print(f"Cannot access manor chronicles: {e}")
    
    def interactive_menu(self):
        """Interactive SSH menu"""
        while True:
            print(f"""
{self.colors['purple']}┌─ Manor Management ────────────────────────────────┐{self.colors['reset']}
{self.colors['purple']}│{self.colors['reset']} 1. 📊 View Manor Status                           {self.colors['purple']}│{self.colors['reset']}
{self.colors['purple']}│{self.colors['reset']} 2. 🔄 Restart RosethornBot                        {self.colors['purple']}│{self.colors['reset']}
{self.colors['purple']}│{self.colors['reset']} 3. 📜 View Recent Logs                            {self.colors['purple']}│{self.colors['reset']}
{self.colors['purple']}│{self.colors['reset']} 4. 🌐 Open Web Dashboard                          {self.colors['purple']}│{self.colors['reset']}
{self.colors['purple']}│{self.colors['reset']} 5. 🚪 Exit Manor                                  {self.colors['purple']}│{self.colors['reset']}
{self.colors['purple']}└───────────────────────────────────────────────────┘{self.colors['reset']}""")
            
            try:
                choice = input(f"\n{self.colors['yellow']}🌹 Choose your path through the manor: {self.colors['reset']}")
                
                if choice == '1':
                    self.show_manor_status()
                elif choice == '2':
                    self.restart_bot()
                elif choice == '3':
                    lines = input(f"{self.colors['cyan']}How many log entries to examine? (default 20): {self.colors['reset']}")
                    lines = int(lines) if lines.isdigit() else 20
                    self.show_logs(lines)
                elif choice == '4':
                    self.gothic_print("Opening web portal to the manor...")
                    print(f"{self.colors['cyan']}Visit: http://localhost:5000 or your server's IP{self.colors['reset']}")
                elif choice == '5':
                    self.gothic_print("Farewell, noble administrator. May the roses bloom in your absence.")
                    break
                else:
                    self.warning_print("Invalid choice. Please select 1-5.")
                    
            except KeyboardInterrupt:
                print(f"\n{self.colors['purple']}🌹 Departing manor gracefully...{self.colors['reset']}")
                break
            except ValueError:
                self.warning_print("Please enter a valid number.")

def main():
    """Main SSH integration entry point"""
    ssh = VictorianSSH()
    
    # Get username
    username = os.getenv('USER', 'Noble Guest')
    if username == 'root':
        username = "Administrator"
    
    # Show welcome
    ssh.welcome_message(username.title())
    
    # Show initial status
    ssh.show_manor_status()
    
    # Check if this is an interactive session
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'status':
            ssh.show_manor_status()
        elif command == 'restart':
            ssh.restart_bot()
        elif command == 'logs':
            lines = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 20
            ssh.show_logs(lines)
        else:
            ssh.error_print(f"Unknown command: {command}")
            print("Available commands: status, restart, logs")
    else:
        # Interactive mode
        ssh.interactive_menu()

if __name__ == "__main__":
    main()