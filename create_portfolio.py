#!/usr/bin/env python3
"""
Simple script to run paper trading and create portfolio
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'testing'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from paper_trader import PaperTrader

def create_and_run_portfolio():
    print("🚀 Creating your first virtual trading portfolio!")
    print("=" * 50)
    
    # Create paper trader with $10,000 starting cash
    trader = PaperTrader(initial_capital=10000)
    
    print(f"💰 Starting cash: ${trader.cash:,.2f}")
    print(f"📁 Portfolio file: {trader.portfolio_file}")
    print(f"📈 Current positions: {len(trader.positions)}")
    
    # Save the initial portfolio
    trader.save_portfolio()
    print("✅ Portfolio saved!")
    
    # Show portfolio status
    print("\n📊 PORTFOLIO STATUS")
    print("-" * 30)
    print(f"💵 Cash Available: ${trader.cash:,.2f}")
    print(f"🏪 Positions: {len(trader.positions)}")
    print(f"📅 Created: {trader.start_date}")
    
    if trader.positions:
        print("\n📈 CURRENT HOLDINGS:")
        for symbol, position in trader.positions.items():
            print(f"  {symbol}: {position['shares']:.2f} shares @ ${position['avg_price']:.2f}")
    else:
        print("\n📝 No positions yet - ready for AI to start trading!")

if __name__ == "__main__":
    create_and_run_portfolio()
