#!/usr/bin/env python3
"""
AI Trading System - Enhanced 4-Hour Automation with Real-Time Updates
====================================================================

A working automation system that runs every 4 hours with real-time portfolio
monitoring and growth tracking display.

Usage:
    python automation/daily_automation.py

Author: AI Assistant
Date: 2024
"""

import os
import sys
import subprocess
import time
import json
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

def log_message(message):
    """Simple logging without emoji"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_portfolio_status():
    """Display real-time portfolio status with growth"""
    try:
        portfolio_file = 'outputs/paper_portfolio.json'
        if not os.path.exists(portfolio_file):
            print("No portfolio file found yet.")
            return
        
        with open(portfolio_file, 'r') as f:
            portfolio = json.load(f)
        
        print("=" * 60)
        print(f"📊 LIVE PORTFOLIO STATUS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        cash = portfolio.get('cash', 0)
        positions = portfolio.get('positions', {})
        
        total_invested = 0
        total_current_value = 0
        position_summary = []
        
        if positions:
            print("\n🏪 CURRENT HOLDINGS:")
            print("-" * 60)
            
            for symbol, pos in positions.items():
                try:
                    # Get current price
                    ticker = yf.Ticker(symbol)
                    current_data = ticker.history(period='1d')
                    current_price = current_data['Close'].iloc[-1] if not current_data.empty else pos['avg_price']
                    
                    shares = pos['shares']
                    purchase_price = pos['avg_price']
                    invested = shares * purchase_price
                    current_value = shares * current_price
                    gain_loss = current_value - invested
                    gain_loss_pct = (gain_loss / invested) * 100 if invested > 0 else 0
                    
                    total_invested += invested
                    total_current_value += current_value
                    
                    status = "🟢" if gain_loss > 0 else "🔴" if gain_loss < 0 else "🟡"
                    
                    print(f"  {status} {symbol}: {shares:.2f} shares @ ${current_price:.2f}")
                    print(f"      Growth: ${gain_loss:+.2f} ({gain_loss_pct:+.2f}%) | Value: ${current_value:,.2f}")
                    
                    position_summary.append({
                        'symbol': symbol,
                        'gain_loss_pct': gain_loss_pct,
                        'current_value': current_value
                    })
                    
                except Exception as e:
                    # Fallback to stored price
                    invested = pos['shares'] * pos['avg_price']
                    total_invested += invested
                    total_current_value += invested
                    print(f"  🟡 {symbol}: {pos['shares']:.2f} shares @ ${pos['avg_price']:.2f} (stored)")
        
        # Portfolio summary
        total_portfolio = cash + total_current_value
        starting_value = 10000
        total_growth = total_portfolio - starting_value
        total_growth_pct = (total_growth / starting_value) * 100 if starting_value > 0 else 0
        
        print(f"\n💎 PORTFOLIO SUMMARY:")
        print("-" * 60)
        print(f"  💵 Cash: ${cash:,.2f}")
        print(f"  📈 Stock Value: ${total_current_value:,.2f}")
        print(f"  🏆 Total Portfolio: ${total_portfolio:,.2f}")
        print(f"  📊 Total Growth: ${total_growth:+,.2f} ({total_growth_pct:+.2f}%)")
        
        if total_growth > 0:
            status_msg = "🚀 GAINING"
        elif total_growth < 0:
            status_msg = "📉 LOSING"
        else:
            status_msg = "🟡 FLAT"
        print(f"  🎯 Status: {status_msg}")
        
        # Show best performer
        if position_summary:
            best = max(position_summary, key=lambda x: x['gain_loss_pct'])
            print(f"  🏆 Best: {best['symbol']} ({best['gain_loss_pct']:+.2f}%)")
        
        # Recent trades
        if portfolio.get('trade_history'):
            recent_trades = portfolio['trade_history'][-3:]
            print(f"\n📝 RECENT ACTIVITY:")
            print("-" * 60)
            for trade in recent_trades:
                timestamp = trade.get('timestamp', '')[:16].replace('T', ' ')
                action = trade.get('action', '')
                symbol = trade.get('symbol', '')
                price = trade.get('price', 0)
                shares = trade.get('shares', 0)
                action_emoji = "🟢" if action == "BUY" else "🔴"
                print(f"  {action_emoji} {timestamp} - {action} {shares:.2f} {symbol} @ ${price:.2f}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"Error displaying portfolio: {e}")

def show_next_run_countdown(next_run_time):
    """Show countdown to next automation run"""
    now = datetime.now()
    if next_run_time > now:
        time_diff = next_run_time - now
        hours = int(time_diff.total_seconds() // 3600)
        minutes = int((time_diff.total_seconds() % 3600) // 60)
        seconds = int(time_diff.total_seconds() % 60)
        print(f"\n⏰ Next automation run in: {hours:02d}:{minutes:02d}:{seconds:02d}")
    else:
        print(f"\n🔥 AUTOMATION RUNNING NOW...")

def run_paper_trading():
    """Run paper trading directly"""
    try:
        log_message("Starting AI paper trading...")
        
        # Change to project directory
        project_root = Path(__file__).parent.parent.resolve()
        os.chdir(project_root)
        
        # Import and run paper trading directly to avoid subprocess issues
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        from testing.paper_trader import PaperTrader
        
        trader = PaperTrader()
        log_message("Loaded paper trader successfully")
        
        # Execute AI trading
        results = trader.auto_trade_with_ai()
        
        # Report results
        trades = results.get('trades', [])
        portfolio_value = results.get('portfolio_value', 0)
        
        log_message(f"Paper trading completed successfully!")
        log_message(f"Trades executed: {len(trades)}")
        log_message(f"Portfolio value: ${portfolio_value:,.2f}")
        
        # Show trade details
        for trade in trades:
            symbol = trade.get('symbol', 'Unknown')
            action = trade.get('action', 'Unknown')
            shares = trade.get('shares', 0)
            price = trade.get('price', 0)
            log_message(f"  {action} {shares:.2f} shares of {symbol} at ${price:.2f}")
        
        return True
        
    except Exception as e:
        log_message(f"Error in paper trading: {e}")
        return False

def check_system_status():
    """Check if system is ready"""
    try:
        project_root = Path(__file__).parent.parent.resolve()
        
        # Check models directory
        models_dir = project_root / 'models'
        if not models_dir.exists():
            log_message("ERROR: Models directory not found")
            return False
        
        model_files = [f for f in models_dir.iterdir() if f.suffix == '.joblib']
        if len(model_files) == 0:
            log_message("ERROR: No trained models found")
            return False
        
        log_message(f"System check passed - Found {len(model_files)} models")
        return True
        
    except Exception as e:
        log_message(f"System check failed: {e}")
        return False

def run_4_hour_automation_with_display():
    """Main 4-hour automation loop with real-time portfolio display"""
    log_message("Starting 4-Hour AI Trading Automation with Real-Time Display")
    log_message("Press Ctrl+C to stop")
    
    # Check system first
    if not check_system_status():
        log_message("System check failed. Please run the complete pipeline first.")
        return
    
    run_count = 0
    
    try:
        while True:
            run_count += 1
            next_run = datetime.now() + timedelta(hours=4)
            
            log_message(f"=== AUTOMATION CYCLE #{run_count} ===")
            
            # Run trading
            success = run_paper_trading()
            
            if success:
                log_message("Trading cycle completed successfully")
            else:
                log_message("Trading cycle had issues, but continuing...")
            
            # Display current portfolio status
            clear_screen()
            print(f"🤖 AI TRADING AUTOMATION - CYCLE #{run_count}")
            display_portfolio_status()
            
            log_message(f"Next run scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            log_message("Monitoring portfolio every 30 seconds...")
            
            # Wait 4 hours with periodic updates
            start_wait = datetime.now()
            update_count = 0
            
            while datetime.now() < next_run:
                try:
                    time.sleep(30)  # Update every 30 seconds
                    update_count += 1
                    
                    # Clear screen and show updated portfolio every 30 seconds
                    clear_screen()
                    print(f"🤖 AI TRADING AUTOMATION - CYCLE #{run_count}")
                    display_portfolio_status()
                    show_next_run_countdown(next_run)
                    
                    # Show monitoring activity
                    elapsed = datetime.now() - start_wait
                    progress = (elapsed.total_seconds() / 14400) * 100
                    print(f"\n📊 Cycle Progress: {progress:.1f}% | Update #{update_count}")
                    print("💡 Portfolio updates every 30 seconds | Press Ctrl+C to stop")
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    log_message(f"Error in monitoring loop: {e}")
                    time.sleep(30)
            
    except KeyboardInterrupt:
        log_message("Automation stopped by user")
    except Exception as e:
        log_message(f"Automation error: {e}")

def main():
    """Enhanced main function with real-time portfolio display"""
    print("🤖 AI Trading System - Enhanced 4-Hour Automation")
    print("=" * 60)
    print("1. Start 4-hour automation with REAL-TIME DISPLAY (recommended)")
    print("2. Run one trading cycle only")  
    print("3. Check current portfolio status")
    print("4. Basic 4-hour automation (no display)")
    print("5. Exit")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting enhanced automation with real-time portfolio updates...")
        print("💡 Your portfolio will update every 30 seconds")
        print("📊 You'll see live prices and growth in real-time")
        input("Press Enter to start...")
        run_4_hour_automation_with_display()
        
    elif choice == "2":
        if check_system_status():
            run_paper_trading()
            print("\n" + "="*60)
            display_portfolio_status()
        else:
            log_message("System check failed")
            
    elif choice == "3":
        display_portfolio_status()
        
    elif choice == "4":
        print("Starting basic 4-hour automation...")
        try:
            while True:
                if check_system_status():
                    run_paper_trading()
                log_message("Waiting 4 hours until next cycle...")
                time.sleep(4 * 60 * 60)  # 4 hours
        except KeyboardInterrupt:
            log_message("Basic automation stopped by user")
            
    elif choice == "5":
        log_message("Goodbye!")
    else:
        log_message("Invalid choice")

if __name__ == "__main__":
    main()
