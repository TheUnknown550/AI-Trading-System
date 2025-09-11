import os
import json
import yfinance as yf
from datetime import datetime

# Check the correct portfolio location within the project
portfolio_file = 'outputs/paper_portfolio.json'

if os.path.exists(portfolio_file):
    with open(portfolio_file, 'r') as f:
        portfolio_data = json.load(f)
    
    print('📊 CURRENT VIRTUAL PORTFOLIO WITH GROWTH')
    print('=' * 50)
    print(f'� Analysis Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'�💰 Cash: ${portfolio_data.get("cash", 0):.2f}')
    print(f'📈 Positions: {len(portfolio_data.get("positions", {}))}')
    print(f'📅 Started: {portfolio_data.get("start_date", "N/A")}')
    print(f'📝 Trades Made: {len(portfolio_data.get("trade_history", []))}')
    print(f'📁 File location: {portfolio_file}')
    
    if portfolio_data.get('positions'):
        print('\n🏪 CURRENT HOLDINGS WITH REAL-TIME GROWTH:')
        print('-' * 50)
        
        total_invested = 0
        total_current_value = 0
        position_details = []
        
        for symbol, pos in portfolio_data['positions'].items():
            try:
                # Get current real-time price
                ticker = yf.Ticker(symbol)
                current_data = ticker.history(period='1d')
                current_price = current_data['Close'].iloc[-1] if not current_data.empty else pos["avg_price"]
                
                shares = pos["shares"]
                purchase_price = pos["avg_price"]
                invested_amount = shares * purchase_price
                current_value = shares * current_price
                
                gain_loss = current_value - invested_amount
                gain_loss_pct = (gain_loss / invested_amount) * 100 if invested_amount > 0 else 0
                
                total_invested += invested_amount
                total_current_value += current_value
                
                # Status emoji based on performance
                if gain_loss > 0:
                    status = "🟢"
                elif gain_loss < 0:
                    status = "🔴"
                else:
                    status = "🟡"
                
                position_details.append({
                    'symbol': symbol,
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                })
                
                print(f'  {status} {symbol}: {shares:.2f} shares')
                print(f'      💰 Bought @ ${purchase_price:.2f} → 📈 Now @ ${current_price:.2f}')
                print(f'      📋 Value: ${invested_amount:.2f} → 🔄 Current: ${current_value:.2f}')
                print(f'      📊 Growth: ${gain_loss:+.2f} ({gain_loss_pct:+.2f}%)')
                
            except Exception as e:
                # Fallback to stored values if real-time data fails
                invested_amount = shares * purchase_price
                total_invested += invested_amount
                total_current_value += invested_amount
                print(f'  🟡 {symbol}: {shares:.2f} shares @ ${purchase_price:.2f} = ${invested_amount:.2f}')
                print(f'      ⚠️ Using stored price (live data unavailable)')
        
        # Portfolio summary with growth
        cash = portfolio_data.get("cash", 0)
        total_portfolio_stored = cash + total_invested
        total_portfolio_current = cash + total_current_value
        
        # Calculate overall performance
        starting_value = 10000  # Starting portfolio value
        total_growth = total_portfolio_current - starting_value
        total_growth_pct = (total_growth / starting_value) * 100 if starting_value > 0 else 0
        
        # Stock-only performance
        stock_growth = total_current_value - total_invested
        stock_growth_pct = (stock_growth / total_invested) * 100 if total_invested > 0 else 0
        
        print(f'\n💎 PORTFOLIO GROWTH SUMMARY:')
        print('-' * 50)
        print(f'  💵 Cash: ${cash:,.2f}')
        print(f'  💰 Total Invested: ${total_invested:,.2f}')
        print(f'  � Current Stock Value: ${total_current_value:,.2f}')
        print(f'  📊 Stock Growth: ${stock_growth:+,.2f} ({stock_growth_pct:+.2f}%)')
        print()
        print(f'  🏦 Starting Portfolio: ${starting_value:,.2f}')
        print(f'  🏆 Current Total Value: ${total_portfolio_current:,.2f}')
        print(f'  📈 Total Growth: ${total_growth:+,.2f} ({total_growth_pct:+.2f}%)')
        
        # Performance status
        if total_growth > 0:
            performance_status = "🚀 GAINING"
        elif total_growth < 0:
            performance_status = "📉 LOSING"
        else:
            performance_status = "🟡 FLAT"
        
        print(f'  🎯 Status: {performance_status}')
        
        # Best and worst performers
        if position_details and len(position_details) > 1:
            best_performer = max(position_details, key=lambda x: x['gain_loss_pct'])
            worst_performer = min(position_details, key=lambda x: x['gain_loss_pct'])
            
            print(f'\n🏆 Top Performer: {best_performer["symbol"]} ({best_performer["gain_loss_pct"]:+.2f}%)')
            print(f'📉 Bottom Performer: {worst_performer["symbol"]} ({worst_performer["gain_loss_pct"]:+.2f}%)')
        
        if portfolio_data.get("trade_history"):
            print(f'\n📝 RECENT TRADES (Last 3):')
            print('-' * 50)
            recent_trades = portfolio_data["trade_history"][-3:]  # Last 3 trades
            for trade in recent_trades:
                timestamp = trade.get("timestamp", "")[:16].replace('T', ' ')
                action = trade.get("action", "")
                symbol = trade.get("symbol", "")
                price = trade.get("price", 0)
                action_emoji = "🟢" if action == "BUY" else "🔴"
                print(f'  {action_emoji} {timestamp} - {action} {symbol} @ ${price:.2f}')
else:
    print('❌ No portfolio file found yet')
    print('Portfolio will be created when you run automation')
