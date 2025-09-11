import yfinance as yf
import json
from datetime import datetime

print('🔍 PORTFOLIO VALUE ANALYSIS - REAL-TIME vs STORED')
print('=' * 60)

# Load portfolio
with open('outputs/paper_portfolio.json', 'r') as f:
    portfolio = json.load(f)

total_current_value = 0
total_stored_value = 0

print(f'📅 Analysis Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

for symbol, pos in portfolio['positions'].items():
    try:
        # Get current real-time price
        ticker = yf.Ticker(symbol)
        current_data = ticker.history(period='1d')
        current_price = current_data['Close'].iloc[-1] if not current_data.empty else 0
        
        # Calculate values
        shares = pos['shares']
        stored_price = pos['avg_price']
        stored_position_value = shares * stored_price
        current_position_value = shares * current_price
        
        gain_loss = current_position_value - stored_position_value
        gain_loss_pct = (gain_loss / stored_position_value) * 100 if stored_position_value > 0 else 0
        
        total_stored_value += stored_position_value
        total_current_value += current_position_value
        
        status = "🟢" if gain_loss > 0 else "🔴" if gain_loss < 0 else "🟡"
        
        print(f'{symbol}:')
        print(f'  📊 Shares: {shares:.2f}')
        print(f'  💰 Bought at: ${stored_price:.2f}')
        print(f'  📈 Current price: ${current_price:.2f}')
        print(f'  📋 Stored value: ${stored_position_value:,.2f}')
        print(f'  🔄 Real value: ${current_position_value:,.2f}')
        print(f'  {status} P/L: ${gain_loss:+,.2f} ({gain_loss_pct:+.2f}%)')
        print()
        
    except Exception as e:
        print(f'{symbol}: Error getting current price - {e}')
        print()

cash = portfolio['cash']
total_portfolio_stored = cash + total_stored_value
total_portfolio_current = cash + total_current_value
overall_gain_loss = total_portfolio_current - total_portfolio_stored
overall_pct = (overall_gain_loss / total_portfolio_stored) * 100 if total_portfolio_stored > 0 else 0

print('💎 PORTFOLIO SUMMARY:')
print(f'  💵 Cash: ${cash:,.2f}')
print(f'  📋 Stored stock value: ${total_stored_value:,.2f}')
print(f'  🔄 Current stock value: ${total_current_value:,.2f}')
print(f'  📋 Portfolio (stored): ${total_portfolio_stored:,.2f}')
print(f'  🔄 Portfolio (real-time): ${total_portfolio_current:,.2f}')

status_emoji = "🟢" if overall_gain_loss > 0 else "🔴" if overall_gain_loss < 0 else "🟡"
print(f'  {status_emoji} Total P/L: ${overall_gain_loss:+,.2f} ({overall_pct:+.2f}%)')

print('\n🎯 ANSWER:')
if abs(overall_gain_loss) < 1:
    print('📋 Portfolio shows STORED VALUES (purchase prices)')
    print('📊 Real-time updates are NOT reflected in portfolio file')
else:
    print('🔄 Portfolio values appear to be updated with real-time prices')
    print('📈 Live market changes are reflected in the portfolio')
