import json
import yfinance as yf
from datetime import datetime

# Load portfolio data
with open('outputs/paper_portfolio.json', 'r') as f:
    portfolio = json.load(f)

print('🔍 COMPLETE PORTFOLIO ANALYSIS WITH GROWTH')
print('=' * 60)
print(f'📅 Analysis Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# Calculate real-time values and growth
total_invested = 0
total_current_value = 0
position_details = []

print('\n📊 CURRENT POSITIONS WITH REAL-TIME GROWTH:')
print('-' * 60)

for symbol, pos in portfolio['positions'].items():
    try:
        # Get current real-time price
        ticker = yf.Ticker(symbol)
        current_data = ticker.history(period='1d')
        current_price = current_data['Close'].iloc[-1] if not current_data.empty else pos['avg_price']
        
        shares = pos['shares']
        purchase_price = pos['avg_price']
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
            'shares': shares,
            'purchase_price': purchase_price,
            'current_price': current_price,
            'invested': invested_amount,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_pct': gain_loss_pct,
            'status': status
        })
        
        print(f'  {status} {symbol}: {shares:.2f} shares')
        print(f'      💰 Bought @ ${purchase_price:.2f} → 📈 Now @ ${current_price:.2f}')
        print(f'      📋 Invested: ${invested_amount:,.2f} → 🔄 Value: ${current_value:,.2f}')
        print(f'      📊 Growth: ${gain_loss:+,.2f} ({gain_loss_pct:+.2f}%)')
        print()
        
    except Exception as e:
        print(f'  ❌ {symbol}: Error getting current price - using stored price')
        invested_amount = pos['shares'] * pos['avg_price']
        total_invested += invested_amount
        total_current_value += invested_amount
        print(f'      📋 Value: ${invested_amount:,.2f} (stored price)')
        print()

# Portfolio summary with growth metrics
cash = portfolio['cash']
total_portfolio_value = cash + total_current_value
starting_value = 10000  # Starting portfolio value

# Calculate overall performance
total_portfolio_growth = total_portfolio_value - starting_value
total_portfolio_growth_pct = (total_portfolio_growth / starting_value) * 100 if starting_value > 0 else 0

# Calculate stock-only performance
stock_growth = total_current_value - total_invested
stock_growth_pct = (stock_growth / total_invested) * 100 if total_invested > 0 else 0

print('💎 PORTFOLIO GROWTH SUMMARY:')
print('=' * 60)
print(f'  💵 Cash Available: ${cash:,.2f}')
print(f'  💰 Total Invested in Stocks: ${total_invested:,.2f}')
print(f'  🔄 Current Stock Value: ${total_current_value:,.2f}')
print(f'  📊 Stock Growth: ${stock_growth:+,.2f} ({stock_growth_pct:+.2f}%)')
print()
print(f'  🏦 Starting Portfolio: ${starting_value:,.2f}')
print(f'  🏆 Current Portfolio: ${total_portfolio_value:,.2f}')
print(f'  📈 Total Growth: ${total_portfolio_growth:+,.2f} ({total_portfolio_growth_pct:+.2f}%)')

# Performance indicators
if total_portfolio_growth > 0:
    performance_status = "🚀 GAINING"
elif total_portfolio_growth < 0:
    performance_status = "📉 LOSING"
else:
    performance_status = "🟡 FLAT"

print(f'  🎯 Status: {performance_status}')

# Best and worst performers
if position_details:
    best_performer = max(position_details, key=lambda x: x['gain_loss_pct'])
    worst_performer = min(position_details, key=lambda x: x['gain_loss_pct'])
    
    print(f'\n🏆 BEST PERFORMER: {best_performer["symbol"]}')
    print(f'    � Growth: ${best_performer["gain_loss"]:+,.2f} ({best_performer["gain_loss_pct"]:+.2f}%)')
    
    print(f'📉 WORST PERFORMER: {worst_performer["symbol"]}')
    print(f'    📊 Growth: ${worst_performer["gain_loss"]:+,.2f} ({worst_performer["gain_loss_pct"]:+.2f}%)')

print(f'\n�📝 ALL TRADE HISTORY ({len(portfolio["trade_history"])} total trades):')
print('-' * 60)
for i, trade in enumerate(portfolio['trade_history'], 1):
    timestamp = trade['timestamp'][:16].replace('T', ' ')
    action_emoji = "🟢" if trade['action'] == "BUY" else "🔴"
    print(f'  #{i} {timestamp} - {action_emoji} {trade["action"]} {trade["symbol"]} @ ${trade["price"]:.2f}')

print(f'\n📈 RECENT TRADES (Last 3 only):')
print('-' * 60)
recent_trades = portfolio["trade_history"][-3:]
for trade in recent_trades:
    timestamp = trade['timestamp'][:16].replace('T', ' ')
    action_emoji = "🟢" if trade['action'] == "BUY" else "🔴"
    print(f'  {timestamp} - {action_emoji} {trade["action"]} {trade["symbol"]} @ ${trade["price"]:.2f}')

print(f'\n✅ ANALYSIS SUMMARY:')
print(f'  📊 Current Holdings: {len(portfolio["positions"])} positions')
print(f'  📝 Total Trades: {len(portfolio["trade_history"])} transactions') 
print(f'  🔄 Sells Made: {sum(1 for t in portfolio["trade_history"] if t["action"] == "SELL")}')
print(f'  📈 Buys Made: {sum(1 for t in portfolio["trade_history"] if t["action"] == "BUY")}')

if len(portfolio["positions"]) == len(portfolio["trade_history"]):
    print(f'\n🎯 TRADING ANALYSIS: No stocks have been sold yet!')
    print(f'   All {len(portfolio["positions"])} purchases are still held.')
    print(f'   Portfolio is in BUY-AND-HOLD mode.')
else:
    print(f'\n🎯 TRADING ANALYSIS: Active trading detected.')
    print(f'   Some positions have been traded for profit/loss management.')
