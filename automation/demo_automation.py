#!/usr/bin/env python3
"""
Demo version of the enhanced automation for testing real-time display
"""

import sys
import os
from pathlib import Path
import time
from datetime import datetime, timedelta

# Add paths
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root / "automation"))

# Import the enhanced functions from daily_automation
from daily_automation import display_portfolio_status, clear_screen, show_next_run_countdown, log_message

def demo_real_time_monitoring():
    """Demo the real-time monitoring for 2 minutes"""
    print("🎮 DEMO: Real-Time Portfolio Monitoring")
    print("This will update every 10 seconds for 2 minutes")
    print("In the real automation, it updates every 30 seconds for 4 hours")
    print("\nPress Ctrl+C to stop early\n")
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=2)
    update_count = 0
    
    try:
        while datetime.now() < end_time:
            update_count += 1
            
            # Clear and display
            clear_screen()
            print(f"🎮 DEMO MODE - Real-Time Portfolio Monitoring")
            print(f"📊 Update #{update_count} | Demo Duration: 2 minutes")
            display_portfolio_status()
            
            # Show countdown
            remaining = end_time - datetime.now()
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            print(f"\n⏰ Demo ends in: {minutes:02d}:{seconds:02d}")
            print("💡 Real automation runs for 4 hours with 30-second updates")
            
            time.sleep(10)  # Update every 10 seconds for demo
            
    except KeyboardInterrupt:
        print("\n\n🛑 Demo stopped by user")
    
    print("\n✅ Demo completed! Your real-time automation is ready!")
    print("Use option 1 in daily_automation.py to start the full 4-hour cycle")

if __name__ == "__main__":
    demo_real_time_monitoring()
