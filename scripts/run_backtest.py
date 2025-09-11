"""
Backtesting Script
Test your AI trading strategy on historical data
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from testing.backtester import Backtester

def run_backtest():
    """Run a comprehensive backtest"""
    print("🔄 Starting AI Trading Backtest...")
    
    # Initialize backtester
    backtester = Backtester(
        start_date="2023-01-01",  # Start date for backtest
        end_date="2024-12-31",    # End date for backtest
        initial_capital=10000      # Starting capital
    )
    
    # Assets to test (start with liquid, well-known assets)
    test_assets = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',  # Stocks
        'BTC_USD', 'ETH_USD',                      # Crypto
        'EURUSDX', 'GBPUSDX'                      # Forex
    ]
    
    print(f"📊 Testing with {len(test_assets)} assets")
    print(f"💰 Initial Capital: $10,000")
    print(f"📅 Period: 2023-2024")
    
    # Run backtest
    results = backtester.run_backtest(
        assets=test_assets,
        min_confidence=0.6  # Only trade when confidence > 60%
    )
    
    if results:
        # Print results
        backtester.print_results(results)
        
        # Create charts
        try:
            backtester.plot_results(results)
        except Exception as e:
            print(f"⚠️ Could not create charts: {e}")
        
        # Summary insights
        print(f"\n💡 Key Insights:")
        if results['total_return_pct'] > 0:
            print(f"✅ Strategy was profitable: +{results['total_return_pct']:.1f}%")
        else:
            print(f"❌ Strategy lost money: {results['total_return_pct']:.1f}%")
        
        if results['win_rate_pct'] > 50:
            print(f"✅ Good win rate: {results['win_rate_pct']:.1f}%")
        else:
            print(f"⚠️ Low win rate: {results['win_rate_pct']:.1f}%")
        
        print(f"📈 Average return per trade: {results['avg_profit_loss_pct']:.2f}%")
        print(f"⏱️ Average holding period: {results['avg_hold_days']:.1f} days")
    
    else:
        print("❌ Backtest failed - check your data and try again")

if __name__ == "__main__":
    run_backtest()
