#!/usr/bin/env python3
"""
🚀 AI Trading System - Complete Testing Suite
==========================================

This script provides a comprehensive testing interface for your AI trading system.
Choose from backtesting, paper trading, or quick predictions.

Usage:
    python test_trading_system.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def display_menu():
    """Display the main testing menu"""
    print("\n" + "="*60)
    print("🚀 AI TRADING SYSTEM - TESTING SUITE")
    print("="*60)
    print()
    print("Choose your testing method:")
    print()
    print("1. 📈 Paper Trading (Live Market Test)")
    print("   → Test AI with real current prices")
    print("   → Virtual money, real market conditions")
    print("   → See live AI trading decisions")
    print()
    print("2. 📊 Backtesting (Historical Test)")
    print("   → Test strategy on past market data")
    print("   → See how AI would have performed")
    print("   → Generate performance charts")
    print()
    print("3. 🔮 Quick Predictions")
    print("   → Get AI predictions for all assets")
    print("   → See confidence levels")
    print("   → No trading, just predictions")
    print()
    print("4. 💼 Portfolio Status")
    print("   → Check current paper trading portfolio")
    print("   → View open positions and cash")
    print("   → See trade history")
    print()
    print("5. 🔄 Reset Paper Portfolio")
    print("   → Start fresh with $10,000")
    print("   → Clear all positions")
    print("   → Reset trade history")
    print()
    print("6. 📋 System Status")
    print("   → Check if all models are trained")
    print("   → Verify data availability")
    print("   → System health check")
    print()
    print("0. 🚪 Exit")
    print()
    print("="*60)

def run_paper_trading():
    """Run paper trading test"""
    print("\n🚀 Starting Paper Trading...")
    print("This will use real market prices to make AI trading decisions with virtual money.")
    
    confirm = input("\nProceed with paper trading? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Paper trading cancelled.")
        return
    
    try:
        # Import and run paper trading
        from testing.paper_trader import PaperTrader
        
        trader = PaperTrader()
        print("\n📊 Running AI analysis and trading...")
        
        # Run auto trading
        results = trader.auto_trade_with_ai()
        
        print(f"\n✅ Paper trading completed!")
        print(f"Trades executed: {len(results.get('trades', []))}")
        print(f"Portfolio value: ${results.get('portfolio_value', 0):,.2f}")
        
    except Exception as e:
        print(f"❌ Error in paper trading: {e}")
        print("Make sure all models are trained and data is available.")

def run_backtesting():
    """Run historical backtesting"""
    print("\n📊 Starting Backtesting...")
    print("This will test your strategy on historical market data.")
    
    # Get date range
    print("\nSelect backtesting period:")
    print("1. Last 6 months")
    print("2. Last 1 year") 
    print("3. Last 2 years")
    print("4. Custom date range")
    
    choice = input("\nChoose option (1-4): ").strip()
    
    from datetime import datetime, timedelta
    end_date = datetime.now()
    
    if choice == "1":
        start_date = end_date - timedelta(days=180)
    elif choice == "2":
        start_date = end_date - timedelta(days=365)
    elif choice == "3":
        start_date = end_date - timedelta(days=730)
    elif choice == "4":
        start_str = input("Enter start date (YYYY-MM-DD): ")
        end_str = input("Enter end date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")
        except:
            print("Invalid date format. Using last 1 year.")
            start_date = end_date - timedelta(days=365)
    else:
        print("Invalid choice. Using last 1 year.")
        start_date = end_date - timedelta(days=365)
    
    try:
        from testing.backtester import Backtester
        
        backtester = Backtester()
        print(f"\n📈 Running backtest from {start_date.date()} to {end_date.date()}...")
        
        # You can modify this to test specific symbols
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
        
        results = backtester.run_backtest(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"\n✅ Backtesting completed!")
        print(f"Total return: {results.get('total_return', 0):.2%}")
        print(f"Win rate: {results.get('win_rate', 0):.2%}")
        print(f"Sharpe ratio: {results.get('sharpe_ratio', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Error in backtesting: {e}")
        print("Make sure all models are trained and data is available.")

def get_quick_predictions():
    """Get AI predictions for all assets"""
    print("\n🔮 Getting AI Predictions...")
    
    try:
        from prediction.predictor import Predictor
        
        predictor = Predictor()
        print("📊 Loading models and making predictions...")
        
        predictions = predictor.predict_all_assets()
        
        print(f"\n✅ Predictions generated for {len(predictions)} assets!")
        print("\nTop predictions (>60% confidence):")
        print("-" * 50)
        
        high_confidence = []
        for symbol, pred in predictions.items():
            if pred.get('confidence', 0) > 0.6:
                high_confidence.append((symbol, pred))
        
        # Sort by confidence
        high_confidence.sort(key=lambda x: x[1]['confidence'], reverse=True)
        
        for symbol, pred in high_confidence[:10]:  # Top 10
            direction = pred['prediction']
            confidence = pred['confidence'] * 100
            print(f"{symbol:8} → {direction:4} ({confidence:.1f}% confidence)")
        
        if not high_confidence:
            print("No high-confidence predictions found.")
            
    except Exception as e:
        print(f"❌ Error getting predictions: {e}")
        print("Make sure all models are trained.")

def check_portfolio_status():
    """Check current paper trading portfolio"""
    print("\n💼 Portfolio Status...")
    
    try:
        from testing.paper_trader import PaperTrader
        
        trader = PaperTrader()
        portfolio = trader.get_portfolio_status()
        
        print(f"\n📊 Current Portfolio:")
        print("-" * 40)
        print(f"💰 Cash: ${portfolio.get('cash', 0):,.2f}")
        print(f"📈 Total Value: ${portfolio.get('total_value', 0):,.2f}")
        
        positions = portfolio.get('positions', {})
        if positions:
            print(f"\n🏢 Positions ({len(positions)}):")
            for symbol, pos in positions.items():
                print(f"  {symbol}: {pos['shares']:.2f} shares @ ${pos['avg_price']:.2f}")
        else:
            print("\nNo open positions.")
            
        print(f"\n📋 Total Trades: {len(portfolio.get('trade_history', []))}")
        
    except Exception as e:
        print(f"❌ Error checking portfolio: {e}")

def reset_portfolio():
    """Reset paper trading portfolio"""
    print("\n🔄 Reset Portfolio...")
    
    confirm = input("This will delete all positions and reset to $10,000. Continue? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Reset cancelled.")
        return
    
    try:
        from testing.paper_trader import PaperTrader
        
        trader = PaperTrader()
        trader.reset_portfolio()
        
        print("✅ Portfolio reset successfully!")
        print("💰 Cash: $10,000")
        print("📊 Positions: None")
        
    except Exception as e:
        print(f"❌ Error resetting portfolio: {e}")

def check_system_status():
    """Check system status and readiness"""
    print("\n📋 System Status Check...")
    
    # Check if data directories exist
    data_dirs = [
        'data/raw',
        'data/features', 
        'data/enhanced',
        'models'
    ]
    
    print("\n📁 Directory Structure:")
    for dir_path in data_dirs:
        full_path = project_root / dir_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_path}")
    
    # Check if models exist
    models_dir = project_root / 'models'
    if models_dir.exists():
        model_files = [f for f in models_dir.iterdir() if f.suffix == '.joblib']
        print(f"\n🤖 Trained Models: {len(model_files)}")
        if model_files:
            print("  ✅ Models ready for prediction")
        else:
            print("  ❌ No trained models found")
            print("  Run: python scripts/run_complete_pipeline.py")
    else:
        print("\n❌ Models directory not found")
    
    # Check data files
    features_dir = project_root / 'MarketData_Features_Enhanced'
    if features_dir.exists():
        feature_files = [f for f in features_dir.iterdir() if f.suffix == '.csv']
        print(f"\n📊 Feature Files: {len(feature_files)}")
    else:
        print("\n❌ Features directory not found")
    
    print(f"\n🐍 Python Version: {sys.version}")
    print("✅ System check completed!")

def main():
    """Main testing interface"""
    while True:
        display_menu()
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye! Happy trading!")
            break
        elif choice == "1":
            run_paper_trading()
        elif choice == "2":
            run_backtesting()
        elif choice == "3":
            get_quick_predictions()
        elif choice == "4":
            check_portfolio_status()
        elif choice == "5":
            reset_portfolio()
        elif choice == "6":
            check_system_status()
        else:
            print("❌ Invalid choice. Please select 0-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your installation and try again.")
