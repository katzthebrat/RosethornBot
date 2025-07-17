import subprocess
import requests
from datetime import datetime

# 🌿 Discord Webhook for Status Channel
WEBHOOK_URL = "https://discord.com/api/webhooks/1394662954456322189/0XYendDXn0COG_e9ewxXWm6MqQB6LG0PnJazY744CCRy_dU2eLnznCpJFGH1qpBnOLnf"

# 🧠 Get PM2 process info for Rosethorn
def get_pm2_restart_info():
    result = subprocess.run(["pm2", "describe", "Rosethorn"], capture_output=True, text=True)
    return result.stdout

# 🧾 Parse restart count and time from PM2 output
def extract_restart_data(pm2_output):
    lines = pm2_output.splitlines()
    restart_count = 0
    restart_time = None
    for line in lines:
        if "restart count" in line:
            restart_count = int(line.strip().split(":")[1])
        if "last restart" in line:
            restart_time = line.strip().split(":")[1].strip()
    return restart_count, restart_time

# 📨 Send Discord alert
def send_restart_alert(restart_count, restart_time):
    embed = {
        "title": "💥 Rosethorn Restarted",
        "description": "The manor stirred and Rosethorn has risen again.",
        "color": 11534299,
        "fields": [
            { "name": "Total Restarts", "value": str(restart_count), "inline": True },
            { "name": "Last Restart", "value": restart_time or "Unknown", "inline": True }
        ],
        "footer": { "text": "Rosethorn Watcher | Boot Alert" },
        "timestamp": datetime.utcnow().isoformat()
    }
    payload = { "embeds": [embed] }
    requests.post(WEBHOOK_URL, json=payload)

# 🧭 Main Execution
if __name__ == "__main__":
    output = get_pm2_restart_info()
    count, time_str = extract_restart_data(output)
    send_restart_alert(count, time_str)
