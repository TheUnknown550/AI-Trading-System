#!/usr/bin/env python3
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
            print("\n🛑 Stopping automation...")
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
