"""
Backtesting Module
Tests AI tra    def load_data(self, asset, data_type="raw"):
        Load historical data for an asset
        
        Args:
            asset (str): Asset symbol
            data_type (str): Type of data ("raw", "features", "enhanced")
            
        Returns:
            pandas.DataFrame: Historical data
        data_dir = get_data_dir(data_type)
        
        if data_type == "raw":
            filename = f"{asset}.csv"
        elif data_type == "features":
            filename = f"{asset}_features.csv"
        else:  # enhanced
            filename = f"{asset}_enhanced_features.csv"historical data to evaluate performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import sys
from glob import glob

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.paths import get_data_dir, get_outputs_dir
from prediction.prediction_system import StockPredictor

class Backtester:
    def __init__(self, start_date=None, end_date=None, initial_capital=10000):
        """
        Initialize backtester
        
        Args:
            start_date (str): Start date for backtesting (YYYY-MM-DD)
            end_date (str): End date for backtesting (YYYY-MM-DD)
            initial_capital (float): Starting capital for backtesting
        """
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}  # Current positions
        self.trade_history = []  # All trades
        self.portfolio_value_history = []  # Portfolio value over time
        
    def load_historical_data(self, asset, data_type="enhanced"):
        """
        Load historical data for an asset
        
        Args:
            asset (str): Asset symbol
            data_type (str): 'raw', 'features', or 'enhanced'
            
        Returns:
            pandas.DataFrame: Historical data
        """
        data_dir = f"../../data/{data_type}"
        
        if data_type == "raw":
            filename = f"{asset}.csv"
        elif data_type == "features":
            filename = f"{asset}_features.csv"
        else:  # enhanced
            filename = f"{asset}_enhanced_features.csv"
        
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Data file not found: {filepath}")
            return None
        
        df = pd.read_csv(filepath)
        
        # Convert Date column to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Filter by date range if specified
        if self.start_date:
            df = df[df['Date'] >= pd.to_datetime(self.start_date)]
        if self.end_date:
            df = df[df['Date'] <= pd.to_datetime(self.end_date)]
        
        return df
    
    def simulate_prediction(self, asset, row_data):
        """
        Simulate a prediction for a specific row of data
        This would normally use your trained model
        
        Args:
            asset (str): Asset symbol
            row_data (pandas.Series): Row of feature data
            
        Returns:
            dict: Prediction result
        """
        # For backtesting, we'll use a simple strategy
        # In reality, you'd use your trained model here
        
        # Simple RSI-based strategy for demonstration
        if 'RSI_14' in row_data:
            rsi = row_data['RSI_14']
            
            if rsi < 30:  # Oversold
                return {
                    'prediction': 'UP',
                    'confidence': 0.7,
                    'up_probability': 0.7,
                    'down_probability': 0.3
                }
            elif rsi > 70:  # Overbought
                return {
                    'prediction': 'DOWN',
                    'confidence': 0.7,
                    'up_probability': 0.3,
                    'down_probability': 0.7
                }
        
        # Neutral prediction if no strong signal
        return {
            'prediction': 'UP',
            'confidence': 0.5,
            'up_probability': 0.5,
            'down_probability': 0.5
        }
    
    def execute_trade(self, asset, action, price, date, confidence, position_size=0.1):
        """
        Execute a trade
        
        Args:
            asset (str): Asset symbol
            action (str): 'BUY' or 'SELL'
            price (float): Trade price
            date (datetime): Trade date
            confidence (float): Prediction confidence
            position_size (float): Fraction of capital to use (0.1 = 10%)
        """
        trade_amount = self.current_capital * position_size
        
        if action == 'BUY' and self.current_capital >= trade_amount:
            # Buy position
            shares = trade_amount / price
            self.positions[asset] = {
                'shares': shares,
                'entry_price': price,
                'entry_date': date,
                'entry_confidence': confidence
            }
            self.current_capital -= trade_amount
            
            self.trade_history.append({
                'date': date,
                'asset': asset,
                'action': 'BUY',
                'price': price,
                'shares': shares,
                'amount': trade_amount,
                'confidence': confidence,
                'capital_after': self.current_capital
            })
            
        elif action == 'SELL' and asset in self.positions:
            # Sell position
            position = self.positions[asset]
            shares = position['shares']
            sell_amount = shares * price
            
            # Calculate profit/loss
            profit_loss = sell_amount - (shares * position['entry_price'])
            profit_loss_pct = (price - position['entry_price']) / position['entry_price'] * 100
            
            self.current_capital += sell_amount
            
            self.trade_history.append({
                'date': date,
                'asset': asset,
                'action': 'SELL',
                'price': price,
                'shares': shares,
                'amount': sell_amount,
                'confidence': confidence,
                'capital_after': self.current_capital,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'hold_days': (date - position['entry_date']).days
            })
            
            # Remove position
            del self.positions[asset]
    
    def calculate_portfolio_value(self, current_prices):
        """
        Calculate current portfolio value
        
        Args:
            current_prices (dict): Current prices for all assets
            
        Returns:
            float: Total portfolio value
        """
        total_value = self.current_capital
        
        for asset, position in self.positions.items():
            if asset in current_prices:
                position_value = position['shares'] * current_prices[asset]
                total_value += position_value
        
        return total_value
    
    def run_backtest(self, assets, min_confidence=0.6):
        """
        Run backtest on multiple assets
        
        Args:
            assets (list): List of asset symbols to test
            min_confidence (float): Minimum confidence for trades
            
        Returns:
            dict: Backtest results
        """
        print(f"🔄 Running backtest...")
        print(f"📅 Period: {self.start_date} to {self.end_date}")
        print(f"💰 Initial Capital: ${self.initial_capital:,.2f}")
        print(f"📊 Assets: {', '.join(assets)}")
        
        # Load data for all assets
        asset_data = {}
        for asset in assets:
            data = self.load_historical_data(asset, "enhanced")
            if data is not None and len(data) > 0:
                asset_data[asset] = data
                print(f"✅ Loaded {len(data)} days of data for {asset}")
            else:
                print(f"❌ Failed to load data for {asset}")
        
        if not asset_data:
            print("❌ No data loaded. Cannot run backtest.")
            return None
        
        # Get all unique dates
        all_dates = set()
        for data in asset_data.values():
            all_dates.update(data['Date'].dt.date)
        all_dates = sorted(list(all_dates))
        
        print(f"📅 Trading over {len(all_dates)} days")
        
        # Simulate trading day by day
        for i, date in enumerate(all_dates):
            current_prices = {}
            
            # Process each asset for this date
            for asset, data in asset_data.items():
                day_data = data[data['Date'].dt.date == date]
                
                if len(day_data) == 0:
                    continue
                
                row = day_data.iloc[0]
                current_price = row['Close']
                current_prices[asset] = current_price
                
                # Get prediction
                prediction = self.simulate_prediction(asset, row)
                
                if prediction['confidence'] >= min_confidence:
                    # Trading logic
                    if prediction['prediction'] == 'UP' and asset not in self.positions:
                        # Buy signal and no current position
                        self.execute_trade(asset, 'BUY', current_price, 
                                         pd.to_datetime(date), prediction['confidence'])
                    
                    elif prediction['prediction'] == 'DOWN' and asset in self.positions:
                        # Sell signal and have position
                        self.execute_trade(asset, 'SELL', current_price, 
                                         pd.to_datetime(date), prediction['confidence'])
            
            # Record portfolio value
            portfolio_value = self.calculate_portfolio_value(current_prices)
            self.portfolio_value_history.append({
                'date': date,
                'portfolio_value': portfolio_value,
                'cash': self.current_capital,
                'positions_count': len(self.positions)
            })
        
        # Close any remaining positions at the end
        final_date = pd.to_datetime(all_dates[-1])
        for asset, position in list(self.positions.items()):
            if asset in current_prices:
                self.execute_trade(asset, 'SELL', current_prices[asset], 
                                 final_date, 0.5)
        
        return self.generate_results()
    
    def generate_results(self):
        """Generate comprehensive backtest results"""
        if not self.trade_history:
            return {"error": "No trades executed"}
        
        trades_df = pd.DataFrame(self.trade_history)
        portfolio_df = pd.DataFrame(self.portfolio_value_history)
        
        # Calculate metrics
        final_value = portfolio_df['portfolio_value'].iloc[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100
        
        # Trade statistics
        buy_trades = trades_df[trades_df['action'] == 'BUY']
        sell_trades = trades_df[trades_df['action'] == 'SELL']
        
        if len(sell_trades) > 0:
            profitable_trades = len(sell_trades[sell_trades['profit_loss'] > 0])
            win_rate = profitable_trades / len(sell_trades) * 100
            avg_profit_loss = sell_trades['profit_loss'].mean()
            avg_profit_loss_pct = sell_trades['profit_loss_pct'].mean()
            avg_hold_days = sell_trades['hold_days'].mean()
        else:
            win_rate = 0
            avg_profit_loss = 0
            avg_profit_loss_pct = 0
            avg_hold_days = 0
        
        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return_pct': total_return,
            'total_trades': len(buy_trades),
            'completed_trades': len(sell_trades),
            'win_rate_pct': win_rate,
            'avg_profit_loss': avg_profit_loss,
            'avg_profit_loss_pct': avg_profit_loss_pct,
            'avg_hold_days': avg_hold_days,
            'trades_df': trades_df,
            'portfolio_df': portfolio_df
        }
        
        return results
    
    def print_results(self, results):
        """Print formatted backtest results"""
        if 'error' in results:
            print(f"❌ {results['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 BACKTEST RESULTS")
        print(f"{'='*60}")
        
        print(f"💰 Initial Capital: ${results['initial_capital']:,.2f}")
        print(f"💰 Final Value: ${results['final_value']:,.2f}")
        print(f"📈 Total Return: {results['total_return_pct']:.2f}%")
        
        print(f"\n📋 Trading Statistics:")
        print(f"   Total Trades: {results['total_trades']}")
        print(f"   Completed Trades: {results['completed_trades']}")
        print(f"   Win Rate: {results['win_rate_pct']:.1f}%")
        print(f"   Avg Profit/Loss: ${results['avg_profit_loss']:.2f}")
        print(f"   Avg Return per Trade: {results['avg_profit_loss_pct']:.2f}%")
        print(f"   Avg Hold Time: {results['avg_hold_days']:.1f} days")
        
        # Show recent trades
        if len(results['trades_df']) > 0:
            print(f"\n📈 Recent Trades:")
            recent_trades = results['trades_df'].tail(5)
            for _, trade in recent_trades.iterrows():
                action_emoji = "🟢" if trade['action'] == 'BUY' else "🔴"
                print(f"   {action_emoji} {trade['date'].strftime('%Y-%m-%d')} "
                      f"{trade['action']} {trade['asset']} @ ${trade['price']:.2f}")
    
    def plot_results(self, results, save_path="../../outputs/backtest_results.png"):
        """Plot backtest results"""
        if 'error' in results:
            return
        
        portfolio_df = results['portfolio_df']
        
        # Create plots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Portfolio value over time
        ax1.plot(portfolio_df['date'], portfolio_df['portfolio_value'], 'b-', linewidth=2)
        ax1.axhline(y=self.initial_capital, color='r', linestyle='--', alpha=0.7, label='Initial Capital')
        ax1.set_title('Portfolio Value Over Time')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Cash vs Invested
        ax2.plot(portfolio_df['date'], portfolio_df['cash'], 'g-', label='Cash', linewidth=2)
        invested = portfolio_df['portfolio_value'] - portfolio_df['cash']
        ax2.plot(portfolio_df['date'], invested, 'r-', label='Invested', linewidth=2)
        ax2.set_title('Cash vs Invested Capital')
        ax2.set_ylabel('Amount ($)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Number of positions over time
        ax3.plot(portfolio_df['date'], portfolio_df['positions_count'], 'purple', linewidth=2)
        ax3.set_title('Number of Open Positions')
        ax3.set_ylabel('Positions Count')
        ax3.grid(True, alpha=0.3)
        
        # Trade profit/loss distribution
        if len(results['trades_df']) > 0:
            sell_trades = results['trades_df'][results['trades_df']['action'] == 'SELL']
            if len(sell_trades) > 0:
                ax4.hist(sell_trades['profit_loss_pct'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax4.axvline(x=0, color='red', linestyle='--', linewidth=2)
                ax4.set_title('Trade Returns Distribution')
                ax4.set_xlabel('Return (%)')
                ax4.set_ylabel('Number of Trades')
                ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Results chart saved to: {save_path}")
        
        plt.show()

if __name__ == "__main__":
    # Example backtest
    backtester = Backtester(
        start_date="2024-01-01",
        end_date="2024-12-31",
        initial_capital=10000
    )
    
    # Test with a few assets
    test_assets = ['AAPL', 'MSFT', 'GOOGL', 'BTC_USD', 'ETH_USD']
    
    # Run backtest
    results = backtester.run_backtest(test_assets, min_confidence=0.6)
    
    if results:
        backtester.print_results(results)
        backtester.plot_results(results)
