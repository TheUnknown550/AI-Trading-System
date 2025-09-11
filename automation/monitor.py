#!/usr/bin/env python3
"""
📊 AI Trading System - Remote Monitoring Dashboard
================================================

This script provides remote monitoring capabilities for your AI trading system.
Check performance, view reports, and monitor health from anywhere!

Usage:
    python automation/monitor.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from tabulate import tabulate
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class TradingSystemMonitor:
    """Remote monitoring for AI trading system"""
    
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
            self.config = {}
    
    def get_portfolio_status(self):
        """Get current portfolio status"""
        try:
            portfolio_file = os.path.join(self.project_root, 'data', 'portfolio.json')
            if os.path.exists(portfolio_file):
                with open(portfolio_file, 'r') as f:
                    portfolio = json.load(f)
                return portfolio
            else:
                return {"error": "Portfolio file not found"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_recent_reports(self, days=7):
        """Get recent daily reports"""
        reports = []
        reports_dir = os.path.join(self.project_root, 'reports')
        
        if not os.path.exists(reports_dir):
            return reports
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for file in os.listdir(reports_dir):
            if file.startswith('daily_report_') and file.endswith('.json'):
                file_path = os.path.join(reports_dir, file)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_time >= cutoff_date:
                    try:
                        with open(file_path, 'r') as f:
                            report = json.load(f)
                            report['file'] = file
                            reports.append(report)
                    except:
                        continue
        
        # Sort by date
        reports.sort(key=lambda x: x.get('date', ''), reverse=True)
        return reports
    
    def get_system_health(self):
        """Check system health"""
        health = {
            "status": "healthy",
            "issues": [],
            "last_update": datetime.now().isoformat()
        }
        
        # Check models
        models_dir = os.path.join(self.project_root, 'models')
        if not os.path.exists(models_dir) or not os.listdir(models_dir):
            health["status"] = "warning"
            health["issues"].append("No trained models found")
        else:
            model_count = len([f for f in os.listdir(models_dir) if f.endswith('.joblib')])
            health["model_count"] = model_count
        
        # Check data freshness
        data_dir = os.path.join(self.project_root, 'data', 'raw')
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            if files:
                # Check newest file
                newest_file = max([os.path.join(data_dir, f) for f in files], 
                                key=os.path.getmtime)
                newest_time = datetime.fromtimestamp(os.path.getmtime(newest_file))
                hours_old = (datetime.now() - newest_time).total_seconds() / 3600
                
                health["data_age_hours"] = hours_old
                
                if hours_old > 48:  # More than 2 days old
                    health["status"] = "warning"
                    health["issues"].append(f"Data is {hours_old:.1f} hours old")
        
        # Check portfolio
        portfolio = self.get_portfolio_status()
        if "error" in portfolio:
            health["status"] = "error"
            health["issues"].append("Portfolio access error")
        else:
            health["portfolio_value"] = portfolio.get("total_value", 0)
        
        return health
    
    def calculate_performance_metrics(self, reports):
        """Calculate performance metrics from reports"""
        if not reports:
            return {}
        
        # Sort reports by date
        reports.sort(key=lambda x: x.get('date', ''))
        
        if len(reports) < 2:
            return {"error": "Need at least 2 reports for metrics"}
        
        first_value = reports[0].get('portfolio_value', 10000)
        last_value = reports[-1].get('portfolio_value', 10000)
        
        # Calculate total return
        total_return = (last_value - first_value) / first_value
        
        # Calculate daily returns
        daily_returns = []
        for i in range(1, len(reports)):
            prev_value = reports[i-1].get('portfolio_value', 0)
            curr_value = reports[i].get('portfolio_value', 0)
            if prev_value > 0:
                daily_return = (curr_value - prev_value) / prev_value
                daily_returns.append(daily_return)
        
        # Calculate metrics
        if daily_returns:
            avg_daily_return = sum(daily_returns) / len(daily_returns)
            volatility = (sum([(r - avg_daily_return)**2 for r in daily_returns]) / len(daily_returns))**0.5
            
            # Simple Sharpe ratio (assuming 0% risk-free rate)
            sharpe_ratio = avg_daily_return / volatility if volatility > 0 else 0
            
            # Win rate
            winning_days = len([r for r in daily_returns if r > 0])
            win_rate = winning_days / len(daily_returns)
        else:
            avg_daily_return = 0
            volatility = 0
            sharpe_ratio = 0
            win_rate = 0
        
        return {
            "total_return": total_return,
            "avg_daily_return": avg_daily_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "win_rate": win_rate,
            "days_tracked": len(daily_returns),
            "current_value": last_value,
            "initial_value": first_value
        }
    
    def display_dashboard(self):
        """Display monitoring dashboard"""
        print("\n" + "="*80)
        print("🤖 AI TRADING SYSTEM - MONITORING DASHBOARD")
        print("="*80)
        
        # System Health
        print("\n📊 SYSTEM HEALTH")
        print("-" * 40)
        health = self.get_system_health()
        
        status_emoji = {
            "healthy": "✅",
            "warning": "⚠️", 
            "error": "❌"
        }
        
        print(f"Status: {status_emoji.get(health['status'], '❓')} {health['status'].upper()}")
        
        if health.get('model_count'):
            print(f"Models: {health['model_count']} trained")
        
        if health.get('data_age_hours'):
            print(f"Data Age: {health['data_age_hours']:.1f} hours")
        
        if health.get('portfolio_value'):
            print(f"Portfolio: ${health['portfolio_value']:,.2f}")
        
        if health.get('issues'):
            print("\nIssues:")
            for issue in health['issues']:
                print(f"  ⚠️ {issue}")
        
        # Portfolio Status
        print("\n💼 PORTFOLIO STATUS")
        print("-" * 40)
        portfolio = self.get_portfolio_status()
        
        if "error" not in portfolio:
            print(f"💰 Cash: ${portfolio.get('cash', 0):,.2f}")
            print(f"📊 Total Value: ${portfolio.get('total_value', 0):,.2f}")
            print(f"🏢 Positions: {len(portfolio.get('positions', {}))}")
            print(f"📋 Total Trades: {len(portfolio.get('trade_history', []))}")
            
            # Show top positions
            positions = portfolio.get('positions', {})
            if positions:
                print("\nTop Positions:")
                for symbol, pos in list(positions.items())[:5]:
                    value = pos['shares'] * pos['avg_price']
                    print(f"  {symbol}: {pos['shares']:.2f} shares = ${value:,.2f}")
        else:
            print(f"❌ Error: {portfolio['error']}")
        
        # Performance Metrics
        print("\n📈 PERFORMANCE METRICS (Last 7 Days)")
        print("-" * 40)
        reports = self.get_recent_reports(7)
        metrics = self.calculate_performance_metrics(reports)
        
        if "error" not in metrics:
            print(f"📊 Total Return: {metrics['total_return']:.2%}")
            print(f"📅 Daily Avg Return: {metrics['avg_daily_return']:.2%}")
            print(f"📊 Win Rate: {metrics['win_rate']:.2%}")
            print(f"📈 Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
            print(f"📊 Volatility: {metrics['volatility']:.2%}")
            print(f"📅 Days Tracked: {metrics['days_tracked']}")
        else:
            print(f"❌ {metrics.get('error', 'No performance data available')}")
        
        # Recent Activity
        print("\n📋 RECENT ACTIVITY")
        print("-" * 40)
        if reports:
            print("Date | Portfolio Value | Daily Trades | Return")
            print("-" * 50)
            for i, report in enumerate(reports[:5]):  # Last 5 days
                date = report.get('date', 'Unknown')[:10]  # Just date part
                value = report.get('portfolio_value', 0)
                trades = report.get('daily_trades', 0)
                
                # Calculate daily return
                if i < len(reports) - 1:
                    prev_value = reports[i+1].get('portfolio_value', value)
                    daily_return = (value - prev_value) / prev_value if prev_value > 0 else 0
                    return_str = f"{daily_return:+.2%}"
                else:
                    return_str = "N/A"
                
                print(f"{date} | ${value:>12,.2f} | {trades:>11} | {return_str:>6}")
        else:
            print("No recent reports found")
        
        print("\n" + "="*80)
        print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def send_status_summary(self):
        """Send status summary to alerts"""
        health = self.get_system_health()
        portfolio = self.get_portfolio_status()
        reports = self.get_recent_reports(7)
        metrics = self.calculate_performance_metrics(reports)
        
        if "error" not in portfolio and "error" not in metrics:
            summary = f"""🤖 AI Trading System Status

💼 Portfolio: ${portfolio.get('total_value', 0):,.2f}
📊 7-Day Return: {metrics.get('total_return', 0):.2%}
📈 Win Rate: {metrics.get('win_rate', 0):.2%}
🏢 Active Positions: {len(portfolio.get('positions', {}))}

System Status: {health['status'].upper()}"""
            
            if health.get('issues'):
                summary += f"\n⚠️ Issues: {', '.join(health['issues'])}"
            
            return summary
        else:
            return "❌ Unable to generate status summary - system errors detected"
    
    def export_performance_report(self, days=30):
        """Export detailed performance report"""
        reports = self.get_recent_reports(days)
        metrics = self.calculate_performance_metrics(reports)
        
        report_data = {
            "generated": datetime.now().isoformat(),
            "period_days": days,
            "system_health": self.get_system_health(),
            "portfolio": self.get_portfolio_status(),
            "performance_metrics": metrics,
            "daily_reports": reports
        }
        
        # Save report
        export_file = os.path.join(self.project_root, 'reports', 
                                 f"performance_report_{datetime.now().strftime('%Y%m%d')}.json")
        
        with open(export_file, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        print(f"📊 Performance report exported: {export_file}")
        return export_file

def main():
    """Main monitoring interface"""
    monitor = TradingSystemMonitor()
    
    while True:
        print("\n🤖 AI Trading System Monitor")
        print("=" * 40)
        print("1. 📊 View Dashboard")
        print("2. 💼 Portfolio Status")
        print("3. 📈 Performance Metrics")
        print("4. 📋 System Health")
        print("5. 📤 Export Report")
        print("6. 🔄 Send Status Alert")
        print("0. 🚪 Exit")
        
        choice = input("\nChoose option (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            monitor.display_dashboard()
        elif choice == "2":
            portfolio = monitor.get_portfolio_status()
            print(json.dumps(portfolio, indent=2))
        elif choice == "3":
            reports = monitor.get_recent_reports(30)
            metrics = monitor.calculate_performance_metrics(reports)
            print(json.dumps(metrics, indent=2))
        elif choice == "4":
            health = monitor.get_system_health()
            print(json.dumps(health, indent=2))
        elif choice == "5":
            days = input("Enter number of days (default 30): ").strip()
            days = int(days) if days.isdigit() else 30
            monitor.export_performance_report(days)
        elif choice == "6":
            summary = monitor.send_status_summary()
            print("\n📤 Status Summary:")
            print(summary)
        else:
            print("❌ Invalid choice")
        
        if choice != "0":
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
