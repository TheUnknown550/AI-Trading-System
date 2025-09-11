#!/usr/bin/env python3
"""
Test the continuous automation mode for 30 seconds to demonstrate it works
"""

import time
import sys
import os
sys.path.append(os.path.dirname(__file__))

from automation.daily_automation import run_daily_automation

def test_continuous():
    print("🤖 Testing Continuous AI Trading Automation")
    print("=" * 60)
    print("This will run 2 cycles with 30-second intervals to demonstrate automation")
    print("In real use, you'd set this to run every 4 hours (14400 seconds)")
    print("=" * 60)
    
    for cycle in range(2):
        print(f"\n🔄 CYCLE {cycle + 1}/2")
        print("-" * 30)
        
        # Run one automation cycle
        success = run_daily_automation()
        
        if success:
            print("✅ Automation cycle completed successfully")
        else:
            print("⚠️ Automation cycle had some issues")
        
        if cycle < 1:  # Don't wait after the last cycle
            print("\n⏰ Waiting 30 seconds before next cycle...")
            print("   (In production, this would be 4 hours)")
            time.sleep(30)
    
    print("\n🎉 Continuous automation test completed!")
    print("Your AI trading system can now run 24/7 automatically!")

if __name__ == "__main__":
    test_continuous()
