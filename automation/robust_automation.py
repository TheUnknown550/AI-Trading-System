#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robust 4-Hour Automation - Windows Compatible
=============================================

This script runs continuous 4-hour automation with robust error handling
and Windows-compatible display.
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Fix Windows Unicode issues
if os.name == 'nt':
    os.system('chcp 65001 >nul')

def log_with_timestamp(message):
    """Log with timestamp to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    
    # Print to console
    try:
        print(log_message)
    except UnicodeEncodeError:
        safe_message = message.encode('ascii', 'ignore').decode('ascii')
        print(f"[{timestamp}] {safe_message}")
    
    # Write to log file
    try:
        os.makedirs('logs', exist_ok=True)
        with open('logs/automation_robust.log', 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception as e:
        print(f"Log write error: {e}")

def run_single_cycle():
    """Run a single trading cycle with error handling"""
    try:
        log_with_timestamp("Starting trading cycle...")
        
        # Run the automation script
        result = subprocess.run([
            sys.executable, 'automation/daily_automation.py'
        ], input='2\n', text=True, capture_output=True, timeout=300)
        
        if result.returncode == 0:
            log_with_timestamp("Trading cycle completed successfully")
            return True
        else:
            log_with_timestamp(f"Trading cycle failed with code {result.returncode}")
            if result.stderr:
                log_with_timestamp(f"Error: {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        log_with_timestamp("Trading cycle timed out after 5 minutes")
        return False
    except Exception as e:
        log_with_timestamp(f"Error in trading cycle: {e}")
        return False

def main():
    """Main robust automation loop"""
    log_with_timestamp("Starting robust 4-hour automation")
    log_with_timestamp("This version handles Windows encoding and errors gracefully")
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            next_run = datetime.now() + timedelta(hours=4)
            
            log_with_timestamp(f"=== CYCLE {cycle_count} ===")
            
            # Run trading cycle
            success = run_single_cycle()
            
            if success:
                log_with_timestamp("Cycle completed successfully")
            else:
                log_with_timestamp("Cycle had issues, but continuing...")
            
            log_with_timestamp(f"Next cycle scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            log_with_timestamp("Waiting 4 hours...")
            
            # Wait 4 hours with periodic status updates
            start_wait = datetime.now()
            while datetime.now() < next_run:
                try:
                    time.sleep(1800)  # Check every 30 minutes
                    elapsed = datetime.now() - start_wait
                    remaining = next_run - datetime.now()
                    
                    hours_elapsed = elapsed.total_seconds() / 3600
                    hours_remaining = remaining.total_seconds() / 3600
                    
                    log_with_timestamp(f"Waiting... {hours_elapsed:.1f}h elapsed, {hours_remaining:.1f}h remaining")
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    log_with_timestamp(f"Error in wait loop: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
                    
    except KeyboardInterrupt:
        log_with_timestamp("Automation stopped by user (Ctrl+C)")
    except Exception as e:
        log_with_timestamp(f"Critical error in automation: {e}")
    finally:
        log_with_timestamp(f"Automation ended after {cycle_count} cycles")

if __name__ == "__main__":
    main()
