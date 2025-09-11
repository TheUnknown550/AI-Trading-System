#!/usr/bin/env python3
"""
🤖 AI Trading System - Simple Automation Scheduler
================================================

A simplified automation system that runs your existing working scripts.
This avoids import issues and uses the proven scripts you already have.

Usage:
    python automation/simple_scheduler.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
import schedule
import logging
import json
import subprocess
from datetime import datetime, timedelta

# Setup logging
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Create logs directory
os.makedirs(os.path.join(project_root, 'logs'), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'logs', 'automation.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleAutomation:
    """Simple automation using existing working scripts"""
    
    def __init__(self):
        self.project_root = project_root
        self.load_config()
        
    def load_config(self):
        """Load configuration"""
        config_file = os.path.join(self.project_root, 'automation', 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "automation": {
                    "daily_training": True,
                    "paper_trading": True,
                    "data_collection": True,
                    "retrain_frequency": 7
                }
            }
    
    def run_script(self, script_path, description):
        """Run a Python script and return success status"""
        try:
            logger.info(f"🔄 Starting: {description}")
            
            # Change to project directory
            os.chdir(self.project_root)
            
            # Run the script
            result = subprocess.run([
                sys.executable, script_path
            ], capture_output=True, text=True, timeout=1800)  # 30 minute timeout
            
            if result.returncode == 0:
                logger.info(f"✅ Completed: {description}")
                return True
            else:
                logger.error(f"❌ Failed: {description}")
                logger.error(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Timeout: {description} took too long")
            return False
        except Exception as e:
            logger.error(f"❌ Exception in {description}: {e}")
            return False
    
    def daily_data_collection(self):
        """Run daily data collection"""
        if not self.config['automation'].get('data_collection', True):
            return True
            
        return self.run_script(
            'scripts/run_complete_pipeline.py', 
            'Daily data collection and feature engineering'
        )
    
    def daily_paper_trading(self):
        """Run daily paper trading"""
        if not self.config['automation'].get('paper_trading', True):
            return True
            
        return self.run_script(
            'scripts/paper_trading.py',
            'Daily AI paper trading'
        )
    
    def get_quick_predictions(self):
        """Get AI predictions"""
        return self.run_script(
            'scripts/quick_predictions.py',
            'AI predictions for all assets'
        )
    
    def weekly_model_training(self):
        """Run weekly model retraining"""
        if not self.config['automation'].get('daily_training', True):
            return True
            
        return self.run_script(
            'scripts/run_complete_pipeline.py',
            'Weekly model retraining'
        )
    
    def check_system_health(self):
        """Basic system health check"""
        try:
            logger.info("🔍 Checking system health...")
            
            # Check if key directories exist
            required_dirs = ['data', 'models', 'scripts']
            for dir_name in required_dirs:
                dir_path = os.path.join(self.project_root, dir_name)
                if not os.path.exists(dir_path):
                    logger.warning(f"⚠️ Missing directory: {dir_name}")
                    return False
            
            # Check if models exist
            models_dir = os.path.join(self.project_root, 'models')
            if os.path.exists(models_dir):
                model_files = [f for f in os.listdir(models_dir) if f.endswith('.joblib')]
                if len(model_files) == 0:
                    logger.warning("⚠️ No trained models found")
                    return False
                else:
                    logger.info(f"✅ Found {len(model_files)} trained models")
            
            logger.info("✅ System health check passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            return False
    
    def daily_automation_task(self):
        """Complete daily automation workflow"""
        logger.info("🚀 Starting daily automation workflow...")
        start_time = datetime.now()
        
        success_count = 0
        total_tasks = 3
        
        # Task 1: System health check
        if self.check_system_health():
            success_count += 1
        
        # Task 2: Data collection and training (if needed)
        if self.daily_data_collection():
            success_count += 1
        
        # Task 3: Paper trading
        if self.daily_paper_trading():
            success_count += 1
        
        # Summary
        duration = datetime.now() - start_time
        success_rate = success_count / total_tasks
        
        if success_rate >= 0.66:  # At least 2/3 tasks successful
            logger.info(f"✅ Daily automation completed successfully!")
            logger.info(f"   Duration: {duration}")
            logger.info(f"   Success rate: {success_count}/{total_tasks}")
        else:
            logger.error(f"❌ Daily automation had issues!")
            logger.error(f"   Duration: {duration}")
            logger.error(f"   Success rate: {success_count}/{total_tasks}")
        
        # Save automation log
        self.save_automation_log(success_count, total_tasks, duration)
    
    def save_automation_log(self, success_count, total_tasks, duration):
        """Save automation results"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "success_count": success_count,
                "total_tasks": total_tasks,
                "success_rate": success_count / total_tasks,
                "duration_seconds": duration.total_seconds()
            }
            
            log_file = os.path.join(self.project_root, 'logs', 'automation_history.json')
            
            # Load existing logs
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            # Add new log
            logs.append(log_entry)
            
            # Keep only last 30 days of logs
            cutoff_date = datetime.now() - timedelta(days=30)
            logs = [log for log in logs 
                   if datetime.fromisoformat(log['timestamp']) > cutoff_date]
            
            # Save logs
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save automation log: {e}")
    
    def weekly_maintenance(self):
        """Weekly maintenance tasks"""
        logger.info("🔧 Running weekly maintenance...")
        
        # Force complete pipeline run
        success = self.run_script(
            'scripts/run_complete_pipeline.py',
            'Weekly complete pipeline maintenance'
        )
        
        if success:
            logger.info("✅ Weekly maintenance completed")
        else:
            logger.error("❌ Weekly maintenance failed")
    
    def setup_schedule(self):
        """Setup automation schedule"""
        logger.info("⏰ Setting up automation schedule...")
        
        # Daily automation at 9:00 AM
        schedule.every().day.at("09:00").do(self.daily_automation_task)
        
        # Weekly maintenance on Monday at 8:00 AM
        schedule.every().monday.at("08:00").do(self.weekly_maintenance)
        
        # Health check every 6 hours
        schedule.every(6).hours.do(self.check_system_health)
        
        logger.info("✅ Schedule configured:")
        logger.info("   Daily automation: 9:00 AM")
        logger.info("   Weekly maintenance: Monday 8:00 AM") 
        logger.info("   Health checks: Every 6 hours")
    
    def run_once(self):
        """Run automation once for testing"""
        logger.info("🧪 Running automation once for testing...")
        self.daily_automation_task()
    
    def run_continuous(self):
        """Run continuous automation"""
        logger.info("🚀 Starting continuous automation...")
        logger.info("Press Ctrl+C to stop")
        
        self.setup_schedule()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("🛑 Automation stopped by user")
        except Exception as e:
            logger.error(f"❌ Automation error: {e}")

def main():
    """Main automation interface"""
    automation = SimpleAutomation()
    
    print("🤖 AI Trading System - Simple Automation")
    print("=" * 50)
    print("1. 🔄 Run automation once (test)")
    print("2. 🚀 Start continuous automation")
    print("3. 🔍 System health check")
    print("4. 📊 Run paper trading now")
    print("5. 🧠 Get AI predictions")
    print("0. 🚪 Exit")
    
    choice = input("\nChoose option (0-5): ").strip()
    
    if choice == "0":
        print("👋 Goodbye!")
    elif choice == "1":
        automation.run_once()
    elif choice == "2":
        automation.run_continuous()
    elif choice == "3":
        automation.check_system_health()
    elif choice == "4":
        automation.daily_paper_trading()
    elif choice == "5":
        automation.get_quick_predictions()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
