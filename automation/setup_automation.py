#!/usr/bin/env python3
"""
🚀 AI Trading System - Quick Setup Automation
============================================

This script sets up your trading system for complete automation.
Run this once to enable hands-off operation!

Usage:
    python automation/setup_automation.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
import json
import subprocess

def setup_automation():
    """Setup complete automation for AI trading system"""
    
    print("🚀 AI Trading System - Automation Setup")
    print("=" * 50)
    print()
    
    # Get user preferences
    print("📧 Email Notifications Setup")
    email_enabled = input("Enable email alerts? (y/n): ").lower().strip() == 'y'
    
    email_config = {"enabled": False}
    if email_enabled:
        email_config = {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": input("Gmail address: ").strip(),
            "password": input("Gmail app password (not regular password): ").strip(),
            "to_email": input("Alert email (can be same): ").strip()
        }
        print("✅ Email alerts configured")
    
    print("\n💬 Discord Notifications Setup")
    discord_enabled = input("Enable Discord alerts? (y/n): ").lower().strip() == 'y'
    
    discord_config = {"enabled": False}
    if discord_enabled:
        print("To get Discord webhook:")
        print("1. Go to your Discord server settings")
        print("2. Click 'Integrations' → 'Webhooks'")
        print("3. Create new webhook and copy URL")
        
        webhook_url = input("Discord webhook URL: ").strip()
        discord_config = {
            "enabled": True,
            "webhook_url": webhook_url
        }
        print("✅ Discord alerts configured")
    
    print("\n⚙️ Trading Settings")
    confidence = float(input("Minimum confidence for trades (0.6 recommended): ") or "0.6")
    max_loss = float(input("Maximum portfolio loss before alert (0.1 = 10%): ") or "0.1")
    retrain_days = int(input("Retrain models every X days (7 recommended): ") or "7")
    
    # Create configuration
    config = {
        "email": email_config,
        "discord": discord_config,
        "automation": {
            "daily_training": True,
            "paper_trading": True,
            "data_collection": True,
            "retrain_frequency": retrain_days,
            "max_portfolio_loss": max_loss,
            "confidence_threshold": confidence
        },
        "monitoring": {
            "check_interval": 1,
            "alert_on_loss": 0.05,
            "alert_on_system_error": True
        },
        "symbols": [
            "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA", 
            "META", "NFLX", "AMZN", "AMD", "INTC"
        ]
    }
    
    # Save configuration
    config_file = "automation/config.json"
    os.makedirs("automation", exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"\n✅ Configuration saved to {config_file}")
    
    # Create directories
    dirs = ['logs', 'reports', 'automation']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("\n📁 Created automation directories")
    
    # Create startup script
    create_startup_script()
    
    print("\n🎯 Automation Setup Complete!")
    print("\nYour AI trading system is now ready for automation:")
    print("\n✅ What's Automated:")
    print("   • Daily data collection")
    print("   • Feature engineering")
    print("   • Model retraining (weekly)")
    print("   • Paper trading execution")
    print("   • Performance monitoring")
    print("   • Email/Discord alerts")
    
    print("\n🚀 How to Run:")
    print("   1. Manual: python automation/scheduler.py")
    print("   2. Background: python automation/start_automation.py")
    print("   3. Monitor: python automation/monitor.py")
    
    print("\n⏰ Schedule:")
    print("   • Daily automation: 9:00 AM")
    print("   • System monitoring: Every hour")
    print("   • Weekly maintenance: Monday 8:00 AM")
    
    print("\n📊 Monitoring:")
    print("   • Run: python automation/monitor.py")
    print("   • View dashboard, performance, alerts")
    print("   • Export reports")
    
    print("\n⚠️ Important:")
    print("   • This is paper trading (virtual money)")
    print("   • Monitor for 1-2 weeks before real trading")
    print("   • Check performance regularly")
    
    print(f"\n🎉 Ready to automate! Start with: python automation/scheduler.py")

def create_startup_script():
    """Create startup script for background automation"""
    
    startup_script = '''#!/usr/bin/env python3
"""
Background Automation Starter for AI Trading System
"""

import os
import sys
import subprocess
import signal
import time
from datetime import datetime

def start_automation():
    """Start automation in background"""
    print("🚀 Starting AI Trading System Automation...")
    
    # Start scheduler in background
    try:
        process = subprocess.Popen([
            sys.executable, 
            "automation/scheduler.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Automation started! Process ID: {process.pid}")
        print("📊 Monitor with: python automation/monitor.py")
        print("🛑 Stop with: Ctrl+C or kill process")
        
        # Save PID for later stopping
        with open("automation/automation.pid", "w") as f:
            f.write(str(process.pid))
        
        # Wait for process
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\\n🛑 Stopping automation...")
            process.terminate()
            process.wait()
            
    except Exception as e:
        print(f"❌ Failed to start automation: {e}")

def stop_automation():
    """Stop background automation"""
    pid_file = "automation/automation.pid"
    
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        
        try:
            os.kill(pid, signal.SIGTERM)
            os.remove(pid_file)
            print(f"✅ Stopped automation (PID: {pid})")
        except:
            print("❌ Process not found or already stopped")
    else:
        print("❌ No automation process found")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_automation()
    else:
        start_automation()
'''
    
    with open("automation/start_automation.py", "w", encoding='utf-8') as f:
        f.write(startup_script)
    
    print("✅ Created startup script: automation/start_automation.py")

if __name__ == "__main__":
    setup_automation()
