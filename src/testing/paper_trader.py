"""
Paper Trading Module
Simulates real trading with current market conditions using virtual money
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time
import os
import sys
import json

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from prediction.prediction_system import StockPredictor

class PaperTrader:
    def __init__(self, initial_capital=10000, portfolio_file=None):
        """
        Initialize paper trader
        
        Args:
            initial_capital (float): Starting virtual money
            portfolio_file (str): File to save portfolio state (default: project_root/outputs/paper_portfolio.json)
        """
        self.initial_capital = initial_capital
        
        # Set default portfolio file path relative to project root
        if portfolio_file is None:
            # Get project root (go up from src/testing to project root)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            self.portfolio_file = os.path.join(project_root, "outputs", "paper_portfolio.json")
        else:
            self.portfolio_file = portfolio_file
            
        self.predictor = StockPredictor()
        
        # Load existing portfolio or create new one
        self.load_portfolio()
    
    def load_portfolio(self):
        """Load portfolio from file or initialize new one"""
        if os.path.exists(self.portfolio_file):
            try:
                with open(self.portfolio_file, 'r') as f:
                    data = json.load(f)
                    self.cash = data.get('cash', self.initial_capital)
                    self.positions = data.get('positions', {})
                    self.trade_history = data.get('trade_history', [])
                    self.start_date = data.get('start_date', datetime.now().isoformat())
                print(f"📁 Loaded existing portfolio: ${self.cash:.2f} cash, {len(self.positions)} positions")
            except Exception as e:
                print(f"❌ Error loading portfolio: {e}")
                self.initialize_new_portfolio()
        else:
            self.initialize_new_portfolio()
    
    def initialize_new_portfolio(self):
        """Initialize a new portfolio"""
        self.cash = self.initial_capital
        self.positions = {}
        self.trade_history = []
        self.start_date = datetime.now().isoformat()
        print(f"🆕 Initialized new portfolio with ${self.initial_capital:.2f}")
    
    def save_portfolio(self):
        """Save portfolio to file"""
        os.makedirs(os.path.dirname(self.portfolio_file), exist_ok=True)
        
        portfolio_data = {
            'cash': self.cash,
            'positions': self.positions,
            'trade_history': self.trade_history,
            'start_date': self.start_date,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.portfolio_file, 'w') as f:
            json.dump(portfolio_data, f, indent=2)
    
    def get_current_price(self, symbol):
        """
        Get current market price for a symbol
        
        Args:
            symbol (str): Asset symbol
            
        Returns:
            float: Current price
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                # Fallback to daily data
                data = ticker.history(period="5d")
                if not data.empty:
                    return data['Close'].iloc[-1]
        except Exception as e:
            print(f"❌ Error getting price for {symbol}: {e}")
        
        return None
    
    def execute_trade(self, symbol, action, shares=None, amount=None):
        """
        Execute a paper trade
        
        Args:
            symbol (str): Asset symbol
            action (str): 'BUY' or 'SELL'
            shares (float): Number of shares (optional if amount specified)
            amount (float): Dollar amount to trade (optional if shares specified)
            
        Returns:
            bool: True if trade successful
        """
        current_price = self.get_current_price(symbol)
        if current_price is None:
            print(f"❌ Cannot get current price for {symbol}")
            return False
        
        timestamp = datetime.now().isoformat()
        
        if action == 'BUY':
            # Calculate shares if amount specified
            if amount and not shares:
                shares = amount / current_price
            elif shares:
                amount = shares * current_price
            else:
                print("❌ Must specify either shares or amount")
                return False
            
            # Check if we have enough cash
            if amount > self.cash:
                print(f"❌ Insufficient funds: ${amount:.2f} required, ${self.cash:.2f} available")
                return False
            
            # Execute buy
            self.cash -= amount
            
            if symbol in self.positions:
                # Add to existing position
                old_shares = self.positions[symbol]['shares']
                old_value = old_shares * self.positions[symbol]['avg_price']
                new_shares = old_shares + shares
                new_avg_price = (old_value + amount) / new_shares
                
                self.positions[symbol] = {
                    'shares': new_shares,
                    'avg_price': new_avg_price,
                    'last_updated': timestamp
                }
            else:
                # New position
                self.positions[symbol] = {
                    'shares': shares,
                    'avg_price': current_price,
                    'last_updated': timestamp
                }
            
            # Record trade
            self.trade_history.append({
                'timestamp': timestamp,
                'symbol': symbol,
                'action': 'BUY',
                'shares': shares,
                'price': current_price,
                'amount': amount,
                'cash_after': self.cash
            })
            
            print(f"🟢 BUY {shares:.4f} shares of {symbol} @ ${current_price:.2f} = ${amount:.2f}")
            return True
        
        elif action == 'SELL':
            # Check if we have the position
            if symbol not in self.positions:
                print(f"❌ No position in {symbol} to sell")
                return False
            
            available_shares = self.positions[symbol]['shares']
            
            # Calculate shares if amount specified
            if amount and not shares:
                shares = min(amount / current_price, available_shares)
            elif not shares:
                # Sell all shares if nothing specified
                shares = available_shares
            
            if shares > available_shares:
                print(f"❌ Cannot sell {shares:.4f} shares, only {available_shares:.4f} available")
                return False
            
            # Execute sell
            amount = shares * current_price
            self.cash += amount
            
            # Calculate profit/loss
            avg_cost = self.positions[symbol]['avg_price']
            profit_loss = (current_price - avg_cost) * shares
            profit_loss_pct = (current_price - avg_cost) / avg_cost * 100
            
            # Update position
            remaining_shares = available_shares - shares
            if remaining_shares > 0.0001:  # Keep position if significant shares remain
                self.positions[symbol]['shares'] = remaining_shares
                self.positions[symbol]['last_updated'] = timestamp
            else:
                # Close position completely
                del self.positions[symbol]
            
            # Record trade
            self.trade_history.append({
                'timestamp': timestamp,
                'symbol': symbol,
                'action': 'SELL',
                'shares': shares,
                'price': current_price,
                'amount': amount,
                'cash_after': self.cash,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct
            })
            
            profit_emoji = "💚" if profit_loss > 0 else "❤️"
            print(f"🔴 SELL {shares:.4f} shares of {symbol} @ ${current_price:.2f} = ${amount:.2f}")
            print(f"   {profit_emoji} P&L: ${profit_loss:.2f} ({profit_loss_pct:.1f}%)")
            return True
        
        return False
    
    def get_portfolio_value(self):
        """Calculate current portfolio value"""
        total_value = self.cash
        position_values = {}
        
        for symbol, position in self.positions.items():
            current_price = self.get_current_price(symbol)
            if current_price:
                position_value = position['shares'] * current_price
                total_value += position_value
                position_values[symbol] = {
                    'shares': position['shares'],
                    'current_price': current_price,
                    'position_value': position_value,
                    'avg_price': position['avg_price'],
                    'unrealized_pnl': (current_price - position['avg_price']) * position['shares'],
                    'unrealized_pnl_pct': (current_price - position['avg_price']) / position['avg_price'] * 100
                }
        
        return total_value, position_values
    
    def print_portfolio_status(self):
        """Print current portfolio status"""
        total_value, position_values = self.get_portfolio_value()
        
        print(f"\n{'='*60}")
        print(f"📊 PAPER TRADING PORTFOLIO STATUS")
        print(f"{'='*60}")
        
        # Overall performance
        total_return = (total_value - self.initial_capital) / self.initial_capital * 100
        start_date = datetime.fromisoformat(self.start_date)
        days_trading = (datetime.now() - start_date).days
        
        print(f"💰 Cash: ${self.cash:,.2f}")
        print(f"📈 Total Portfolio Value: ${total_value:,.2f}")
        print(f"📊 Total Return: {total_return:.2f}% over {days_trading} days")
        
        if self.positions:
            print(f"\n📋 Current Positions ({len(self.positions)}):")
            print(f"{'Symbol':<10} {'Shares':<12} {'Avg Price':<12} {'Current':<12} {'Value':<12} {'P&L %':<10}")
            print("-" * 70)
            
            for symbol, pos_data in position_values.items():
                pnl_color = "💚" if pos_data['unrealized_pnl'] > 0 else "❤️"
                print(f"{symbol:<10} {pos_data['shares']:<12.4f} ${pos_data['avg_price']:<11.2f} "
                      f"${pos_data['current_price']:<11.2f} ${pos_data['position_value']:<11.2f} "
                      f"{pnl_color}{pos_data['unrealized_pnl_pct']:<9.1f}%")
        
        # Recent trades
        if self.trade_history:
            print(f"\n📈 Recent Trades (Last 5):")
            recent_trades = self.trade_history[-5:]
            for trade in recent_trades:
                action_emoji = "🟢" if trade['action'] == 'BUY' else "🔴"
                timestamp = datetime.fromisoformat(trade['timestamp'])
                print(f"   {action_emoji} {timestamp.strftime('%m/%d %H:%M')} "
                      f"{trade['action']} {trade['shares']:.3f} {trade['symbol']} @ ${trade['price']:.2f}")
    
    def auto_trade_with_ai(self, min_confidence=0.65, max_position_size=0.2):
        """
        Automatically trade based on AI predictions
        
        Args:
            min_confidence (float): Minimum confidence for trades
            max_position_size (float): Maximum % of portfolio per position
        """
        print(f"🤖 Running AI-powered paper trading...")
        print(f"📊 Min confidence: {min_confidence:.1%}")
        print(f"💰 Max position size: {max_position_size:.1%}")
        
        # Get AI predictions
        predictions = self.predictor.predict_all()
        
        if not predictions:
            print("❌ No AI predictions available")
            return
        
        total_value, _ = self.get_portfolio_value()
        max_trade_amount = total_value * max_position_size
        
        trades_executed = 0
        
        for asset, prediction in predictions.items():
            if prediction['confidence'] < min_confidence:
                continue
            
            print(f"\n🔍 Analyzing {asset}: {prediction['prediction']} "
                  f"({prediction['confidence']:.1%} confidence)")
            
            if prediction['prediction'] == 'UP':
                # Buy signal
                if asset not in self.positions and self.cash > 100:  # Min $100 trade
                    trade_amount = min(max_trade_amount, self.cash * 0.5)  # Use up to 50% of cash
                    if self.execute_trade(asset, 'BUY', amount=trade_amount):
                        trades_executed += 1
                        self.save_portfolio()
                
            elif prediction['prediction'] == 'DOWN':
                # Sell signal
                if asset in self.positions:
                    # Sell 50% of position on DOWN signal
                    shares_to_sell = self.positions[asset]['shares'] * 0.5
                    if self.execute_trade(asset, 'SELL', shares=shares_to_sell):
                        trades_executed += 1
                        self.save_portfolio()
        
        print(f"\n✅ AI Trading completed: {trades_executed} trades executed")
        
        if trades_executed > 0:
            self.print_portfolio_status()
    
    def manual_trade_interface(self):
        """Interactive manual trading interface"""
        print(f"\n🎯 Manual Paper Trading Interface")
        print(f"Commands: buy <symbol> <amount>, sell <symbol> <shares>, status, quit")
        
        while True:
            try:
                command = input("\n📈 Enter command: ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'status':
                    self.print_portfolio_status()
                elif command.startswith('buy '):
                    parts = command.split()
                    if len(parts) >= 3:
                        symbol = parts[1].upper()
                        amount = float(parts[2])
                        if self.execute_trade(symbol, 'BUY', amount=amount):
                            self.save_portfolio()
                elif command.startswith('sell '):
                    parts = command.split()
                    if len(parts) >= 3:
                        symbol = parts[1].upper()
                        shares = float(parts[2])
                        if self.execute_trade(symbol, 'SELL', shares=shares):
                            self.save_portfolio()
                else:
                    print("❌ Invalid command. Use: buy <symbol> <amount>, sell <symbol> <shares>, status, quit")
            
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        self.save_portfolio()

if __name__ == "__main__":
    # Initialize paper trader
    trader = PaperTrader(initial_capital=10000)
    
    # Show current status
    trader.print_portfolio_status()
    
    # Run AI trading
    trader.auto_trade_with_ai(min_confidence=0.6)
    
    # Optional: Start manual interface
    # trader.manual_trade_interface()
