import json

# Load and analyze portfolio
with open('outputs/paper_portfolio.json', 'r') as f:
    portfolio = json.load(f)

print('🔍 PORTFOLIO VERIFICATION')
print('=' * 40)
print(f'💰 Cash: ${portfolio["cash"]:,.2f}')

total_stock_value = 0
print('\n📊 POSITION ANALYSIS:')
for symbol, pos in portfolio['positions'].items():
    shares = pos['shares']
    price = pos['avg_price']
    value = shares * price
    total_stock_value += value
    print(f'  {symbol}: {shares:.2f} shares × ${price:.2f} = ${value:,.2f}')

total_portfolio = portfolio['cash'] + total_stock_value

print(f'\n💎 FINAL CALCULATION:')
print(f'  💵 Cash: ${portfolio["cash"]:,.2f}')
print(f'  📈 Stock Value: ${total_stock_value:,.2f}')
print(f'  🏆 TOTAL PORTFOLIO: ${total_portfolio:,.2f}')

print(f'\n✅ Your portfolio is worth ${total_portfolio:,.2f}')
print(f'✅ You started with $10,000')
print(f'✅ Current performance: {((total_portfolio - 10000) / 10000) * 100:.2f}%')
