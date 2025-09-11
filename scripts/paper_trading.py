"""
Paper Trading Script
Trade with virtual money using real market conditions
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from testing.paper_trader import PaperTrader

def start_paper_trading():
    """Start paper trading session"""
    print("📈 AI Paper Trading System")
    print("=" * 40)
    
    # Initialize trader with $10,000 virtual money
    trader = PaperTrader(initial_capital=10000)
    
    # Show current portfolio status
    trader.print_portfolio_status()
    
    print("\n🤖 Choose trading mode:")
    print("1. Auto AI Trading (AI makes decisions)")
    print("2. Manual Trading (You make decisions)")
    print("3. Show Portfolio Only")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🤖 Starting AI Auto-Trading...")
            trader.auto_trade_with_ai(
                min_confidence=0.6,      # Only trade with 60%+ confidence
                max_position_size=0.2    # Max 20% of portfolio per position
            )
            
        elif choice == "2":
            print("\n🎯 Starting Manual Trading Interface...")
            print("💡 Tips:")
            print("   - Use 'buy AAPL 1000' to buy $1000 worth of AAPL")
            print("   - Use 'sell AAPL 10' to sell 10 shares of AAPL")
            print("   - Use 'status' to see portfolio")
            print("   - Use 'quit' to exit")
            trader.manual_trade_interface()
            
        elif choice == "3":
            print("\n📊 Portfolio Status Only")
            trader.print_portfolio_status()
            
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

def reset_portfolio():
    """Reset paper trading portfolio"""
    portfolio_file = "outputs/paper_portfolio.json"
    if os.path.exists(portfolio_file):
        os.remove(portfolio_file)
        print("🔄 Portfolio reset! Starting fresh with $10,000")
    else:
        print("ℹ️ No existing portfolio found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        reset_portfolio()
    else:
        start_paper_trading()
