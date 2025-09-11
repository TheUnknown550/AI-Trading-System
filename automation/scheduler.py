#!/usr/bin/env python3
"""
🤖 AI Trading System - Automated Training & Monitoring Scheduler
==============================================================

This script automates your entire AI trading pipeline:
- Daily data collection
- Feature engineering  
- Model retraining
- Paper trading execution
- Performance monitoring
- Email/Discord alerts

Set this to run daily and your system will operate autonomously!

Usage:
    python automation/scheduler.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
import schedule
import logging
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Try to import email modules, fall back to basic functionality if they fail
try:
    import smtplib
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("⚠️ Email functionality not available. Alerts will be logged only.")

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'logs', 'automation.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingSystemAutomation:
    """Automated AI Trading System Manager"""
    
    def __init__(self, config_file='automation/config.json'):
        """Initialize automation system"""
        self.config_file = os.path.join(project_root, config_file)
        self.load_config()
        self.setup_directories()
        
    def load_config(self):
        """Load automation configuration"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "to_email": ""
            },
            "discord": {
                "enabled": False,
                "webhook_url": ""
            },
            "automation": {
                "daily_training": True,
                "paper_trading": True,
                "data_collection": True,
                "retrain_frequency": 7,  # days
                "max_portfolio_loss": 0.1,  # 10%
                "confidence_threshold": 0.6
            },
            "monitoring": {
                "check_interval": 1,  # hours
                "alert_on_loss": 0.05,  # 5%
                "alert_on_system_error": True
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def setup_directories(self):
        """Create necessary directories"""
        dirs = ['logs', 'automation', 'reports']
        for dir_name in dirs:
            os.makedirs(os.path.join(project_root, dir_name), exist_ok=True)
    
    def send_email_alert(self, subject, message):
        """Send email notification"""
        if not self.config['email']['enabled'] or not EMAIL_AVAILABLE:
            logger.info(f"Email alert (not sent): {subject} - {message}")
            return
            
        try:
            msg = MimeMultipart()
            msg['From'] = self.config['email']['username']
            msg['To'] = self.config['email']['to_email']
            msg['Subject'] = f"🤖 AI Trading Alert: {subject}"
            
            msg.attach(MimeText(message, 'plain'))
            
            server = smtplib.SMTP(self.config['email']['smtp_server'], 
                                self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['username'], 
                        self.config['email']['password'])
            
            text = msg.as_string()
            server.sendmail(self.config['email']['username'],
                          self.config['email']['to_email'], text)
            server.quit()
            
            logger.info(f"Email alert sent: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            logger.info(f"Email alert (failed): {subject} - {message}")
    
    def send_discord_alert(self, message):
        """Send Discord notification"""
        if not self.config['discord']['enabled']:
            return
            
        try:
            data = {
                "content": f"🤖 **AI Trading System Alert**\n```{message}```"
            }
            
            response = requests.post(self.config['discord']['webhook_url'], 
                                   json=data)
            
            if response.status_code == 204:
                logger.info("Discord alert sent successfully")
            else:
                logger.error(f"Discord alert failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
    
    def alert(self, subject, message):
        """Send alert via all enabled channels"""
        logger.info(f"ALERT: {subject} - {message}")
        self.send_email_alert(subject, message)
        self.send_discord_alert(f"{subject}\n{message}")
    
    def collect_market_data(self):
        """Automated data collection"""
        try:
            logger.info("🔄 Starting automated data collection...")
            
            from data_collection.collect_data import DataCollector
            
            collector = DataCollector()
            success_count = 0
            total_symbols = 0
            
            # Collect data for all symbols
            symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'NFLX', 
                      'AMZN', 'AMD', 'INTC']  # Add your symbols
            
            for symbol in symbols:
                try:
                    collector.collect_data(symbol)
                    success_count += 1
                    logger.info(f"✅ Collected data for {symbol}")
                except Exception as e:
                    logger.error(f"❌ Failed to collect {symbol}: {e}")
                total_symbols += 1
            
            success_rate = success_count / total_symbols
            
            if success_rate < 0.8:  # Alert if less than 80% success
                self.alert("Data Collection Issues", 
                          f"Only {success_count}/{total_symbols} symbols updated successfully")
            else:
                logger.info(f"✅ Data collection completed: {success_count}/{total_symbols}")
                
            return success_rate > 0.5
            
        except Exception as e:
            logger.error(f"❌ Data collection failed: {e}")
            self.alert("Data Collection Failed", str(e))
            return False
    
    def update_features(self):
        """Automated feature engineering"""
        try:
            logger.info("🔄 Starting feature engineering...")
            
            from feature_engineering.add_indicators import FeatureEngineering
            
            fe = FeatureEngineering()
            success_count = 0
            
            # Process all data files
            raw_dir = os.path.join(project_root, 'data', 'raw')
            if not os.path.exists(raw_dir):
                logger.error("Raw data directory not found")
                return False
                
            for file in os.listdir(raw_dir):
                if file.endswith('.csv'):
                    symbol = file.replace('.csv', '')
                    try:
                        fe.add_technical_indicators(symbol)
                        success_count += 1
                        logger.info(f"✅ Updated features for {symbol}")
                    except Exception as e:
                        logger.error(f"❌ Feature engineering failed for {symbol}: {e}")
            
            logger.info(f"✅ Feature engineering completed: {success_count} symbols")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Feature engineering failed: {e}")
            self.alert("Feature Engineering Failed", str(e))
            return False
    
    def retrain_models(self):
        """Automated model retraining"""
        try:
            logger.info("🔄 Starting model retraining...")
            
            from model_training.train_models import ModelTraining
            
            trainer = ModelTraining()
            results = trainer.train_all_models()
            
            # Analyze training results
            accuracies = [r.get('accuracy', 0) for r in results.values() if 'accuracy' in r]
            avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0
            
            logger.info(f"✅ Model retraining completed. Average accuracy: {avg_accuracy:.2%}")
            
            # Alert if accuracy drops significantly
            if avg_accuracy < 0.5:
                self.alert("Low Model Accuracy", 
                          f"Average model accuracy dropped to {avg_accuracy:.2%}")
            
            return avg_accuracy > 0.4
            
        except Exception as e:
            logger.error(f"❌ Model retraining failed: {e}")
            self.alert("Model Retraining Failed", str(e))
            return False
    
    def execute_paper_trading(self):
        """Automated paper trading"""
        try:
            logger.info("🔄 Starting automated paper trading...")
            
            from testing.paper_trader import PaperTrader
            
            trader = PaperTrader()
            
            # Check current portfolio status
            portfolio = trader.portfolio
            initial_value = portfolio.get('total_value', 10000)
            
            # Execute AI trading
            results = trader.auto_trade_with_ai(
                confidence_threshold=self.config['automation']['confidence_threshold']
            )
            
            # Analyze results
            trades_executed = len(results.get('trades', []))
            new_value = results.get('portfolio_value', initial_value)
            daily_return = (new_value - initial_value) / initial_value
            
            logger.info(f"✅ Paper trading completed:")
            logger.info(f"   Trades executed: {trades_executed}")
            logger.info(f"   Portfolio value: ${new_value:,.2f}")
            logger.info(f"   Daily return: {daily_return:.2%}")
            
            # Alert on significant losses
            if daily_return < -self.config['monitoring']['alert_on_loss']:
                self.alert("Portfolio Loss Alert", 
                          f"Daily loss: {daily_return:.2%} (${new_value:,.2f})")
            
            # Alert on significant gains
            if daily_return > 0.05:  # 5% gain
                self.alert("Portfolio Gain Alert", 
                          f"Daily gain: {daily_return:.2%} (${new_value:,.2f})")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Paper trading failed: {e}")
            self.alert("Paper Trading Failed", str(e))
            return False
    
    def generate_daily_report(self):
        """Generate daily performance report"""
        try:
            logger.info("📊 Generating daily report...")
            
            from testing.paper_trader import PaperTrader
            
            trader = PaperTrader()
            portfolio = trader.portfolio
            
            # Create report
            report = {
                "date": datetime.now().isoformat(),
                "portfolio_value": portfolio.get('total_value', 0),
                "cash": portfolio.get('cash', 0),
                "positions": len(portfolio.get('positions', {})),
                "total_trades": len(portfolio.get('trade_history', [])),
                "daily_trades": 0  # Calculate today's trades
            }
            
            # Count today's trades
            today = datetime.now().date()
            for trade in portfolio.get('trade_history', []):
                trade_date = datetime.fromisoformat(trade['timestamp']).date()
                if trade_date == today:
                    report['daily_trades'] += 1
            
            # Save report
            reports_dir = os.path.join(project_root, 'reports')
            report_file = os.path.join(reports_dir, f"daily_report_{today.isoformat()}.json")
            
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=4)
            
            logger.info(f"✅ Daily report saved: {report_file}")
            
            # Send summary if significant activity
            if report['daily_trades'] > 0:
                message = f"""Daily Trading Summary:
Portfolio Value: ${report['portfolio_value']:,.2f}
Trades Today: {report['daily_trades']}
Total Positions: {report['positions']}
Cash Available: ${report['cash']:,.2f}"""
                
                self.alert("Daily Trading Summary", message)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Daily report generation failed: {e}")
            return False
    
    def daily_automation_task(self):
        """Complete daily automation workflow"""
        logger.info("🚀 Starting daily automation workflow...")
        
        start_time = datetime.now()
        
        # Step 1: Collect fresh market data
        if self.config['automation']['data_collection']:
            data_success = self.collect_market_data()
            if not data_success:
                logger.error("❌ Data collection failed, skipping remaining tasks")
                return
        
        # Step 2: Update features
        features_success = self.update_features()
        if not features_success:
            logger.error("❌ Feature engineering failed, skipping training")
        
        # Step 3: Retrain models (if scheduled)
        last_training = self.get_last_training_date()
        days_since_training = (datetime.now() - last_training).days
        
        if days_since_training >= self.config['automation']['retrain_frequency']:
            if features_success:
                models_success = self.retrain_models()
                if models_success:
                    self.save_last_training_date()
        
        # Step 4: Execute paper trading
        if self.config['automation']['paper_trading']:
            trading_success = self.execute_paper_trading()
        
        # Step 5: Generate daily report
        self.generate_daily_report()
        
        # Completion summary
        duration = datetime.now() - start_time
        logger.info(f"✅ Daily automation completed in {duration}")
        
        summary = f"""Daily Automation Completed
Duration: {duration}
Data Collection: ✅
Feature Engineering: ✅
Paper Trading: ✅
Report Generated: ✅

System running smoothly! 🚀"""
        
        self.alert("Daily Automation Complete", summary)
    
    def get_last_training_date(self):
        """Get last model training date"""
        training_file = os.path.join(project_root, 'automation', 'last_training.txt')
        if os.path.exists(training_file):
            with open(training_file, 'r') as f:
                date_str = f.read().strip()
                return datetime.fromisoformat(date_str)
        return datetime.now() - timedelta(days=30)  # Default to 30 days ago
    
    def save_last_training_date(self):
        """Save last training date"""
        training_file = os.path.join(project_root, 'automation', 'last_training.txt')
        with open(training_file, 'w') as f:
            f.write(datetime.now().isoformat())
    
    def monitor_system_health(self):
        """Monitor system health and performance"""
        try:
            logger.info("🔍 Checking system health...")
            
            # Check if models exist
            models_dir = os.path.join(project_root, 'models')
            if not os.path.exists(models_dir) or not os.listdir(models_dir):
                self.alert("System Health Warning", "No trained models found!")
                return
            
            # Check portfolio performance
            from testing.paper_trader import PaperTrader
            trader = PaperTrader()
            portfolio = trader.portfolio
            
            total_value = portfolio.get('total_value', 10000)
            initial_value = 10000  # Starting value
            total_return = (total_value - initial_value) / initial_value
            
            # Alert on significant portfolio changes
            max_loss = self.config['automation']['max_portfolio_loss']
            if total_return < -max_loss:
                self.alert("Portfolio Alert", 
                          f"Portfolio down {total_return:.2%} from initial value")
            
            logger.info(f"✅ System health check completed. Portfolio: ${total_value:,.2f}")
            
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            self.alert("System Health Check Failed", str(e))
    
    def setup_automation_schedule(self):
        """Setup automated scheduling"""
        logger.info("⏰ Setting up automation schedule...")
        
        # Daily tasks
        schedule.every().day.at("09:00").do(self.daily_automation_task)
        
        # Hourly monitoring
        schedule.every().hour.do(self.monitor_system_health)
        
        # Weekly deep check
        schedule.every().monday.at("08:00").do(self.weekly_maintenance)
        
        logger.info("✅ Automation schedule configured:")
        logger.info("   Daily automation: 9:00 AM")
        logger.info("   System monitoring: Every hour")
        logger.info("   Weekly maintenance: Monday 8:00 AM")
    
    def weekly_maintenance(self):
        """Weekly maintenance tasks"""
        logger.info("🔧 Running weekly maintenance...")
        
        # Clean old log files
        self.cleanup_old_files('logs', days=30)
        
        # Clean old reports
        self.cleanup_old_files('reports', days=90)
        
        # Force model retraining
        self.retrain_models()
        
        logger.info("✅ Weekly maintenance completed")
    
    def cleanup_old_files(self, directory, days=30):
        """Clean up old files"""
        dir_path = os.path.join(project_root, directory)
        if not os.path.exists(dir_path):
            return
            
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_date:
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {file}")
    
    def run_automation(self):
        """Run the automation system"""
        logger.info("🚀 AI Trading System Automation Started!")
        logger.info("Press Ctrl+C to stop automation")
        
        self.setup_automation_schedule()
        
        # Send startup alert
        self.alert("System Started", "AI Trading automation system is now running!")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("🛑 Automation stopped by user")
            self.alert("System Stopped", "AI Trading automation has been stopped")
        except Exception as e:
            logger.error(f"❌ Automation system error: {e}")
            self.alert("System Error", f"Automation system encountered an error: {e}")

def main():
    """Main automation entry point"""
    automation = TradingSystemAutomation()
    
    print("🤖 AI Trading System Automation")
    print("=" * 50)
    print("1. Run automation (continuous)")
    print("2. Run daily task once") 
    print("3. Configure alerts")
    print("4. System health check")
    print("5. Exit")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == "1":
        automation.run_automation()
    elif choice == "2":
        automation.daily_automation_task()
    elif choice == "3":
        print("Configure email/Discord alerts in automation/config.json")
    elif choice == "4":
        automation.monitor_system_health()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
