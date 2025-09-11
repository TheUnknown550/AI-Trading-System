# AI Trading System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/TheUnknown550/TradingAiCode)

A machine learning-powered trading system that predicts stock market movements using technical indicators and news sentiment analysis.

## Features

- **🤖 AI Predictions**: Random Forest models with 52.7% average accuracy
- **📊 Technical Analysis**: 17+ indicators (RSI, MACD, Bollinger Bands, etc.)
- **📰 News Sentiment**: Real-time news analysis for market sentiment
- **💼 Paper Trading**: Virtual portfolio with $10,000 starting capital
- **🔄 Automation**: Continuous trading every 4 hours
- **📈 Multi-Asset**: Stocks, crypto, and forex support

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/TheUnknown550/TradingAiCode.git
cd TradingAiCode
```

2. **Install dependencies**
```bash
pip install yfinance pandas scikit-learn ta newsapi-python textblob vaderSentiment schedule tabulate
```

3. **Configure Python environment**
```bash
python -c "import sys; print(f'Python {sys.version}')"
```

### Usage

#### Option 1: Manual Trading
```bash
python automation/daily_automation.py
# Choose option 1: Run daily automation
```

#### Option 2: Continuous Automation
```bash
python automation/daily_automation.py
# Choose option 5: Continuous automation (every 4 hours)
```

#### Option 3: Get AI Predictions Only
```bash
python automation/daily_automation.py
# Choose option 4: Get AI predictions
```

## How It Works

1. **Data Collection**: Downloads 5 years of historical market data
2. **Feature Engineering**: Calculates 17+ technical indicators
3. **Model Training**: Trains Random Forest classifiers for each asset
4. **Prediction**: Makes UP/DOWN predictions with confidence scores
5. **Trading**: Executes virtual trades with high-confidence predictions (>65%)
6. **Portfolio Management**: Tracks performance with virtual $10,000 portfolio

## Supported Assets

### Stocks
- **Tech**: AAPL, MSFT, GOOGL, NVDA, TSLA, META, AMZN, NFLX
- **Other**: AMD, INTC

### Cryptocurrency
- Bitcoin (BTC), Ethereum (ETH), Solana (SOL)
- Binance Coin (BNB), Cardano (ADA), Dogecoin (DOGE)

### Forex
- EUR/USD, GBP/USD, AUD/USD, USD/CAD, USD/CHF, USD/JPY

## Project Structure

```
TradingAiCode/
├── src/
│   ├── data/           # Data collection and processing
│   ├── features/       # Technical indicator calculations
│   ├── models/         # ML model training and evaluation
│   ├── prediction/     # Prediction system
│   └── testing/        # Paper trading and backtesting
├── automation/         # Automated trading scripts
├── models/            # Trained model files (44 .joblib files)
├── MarketData/        # Raw market data (CSV files)
├── MarketData_Features/ # Processed features (CSV files)
└── outputs/           # Portfolio and results
```

## Configuration

### Technical Indicators
- RSI, MACD, Bollinger Bands, Stochastic Oscillator
- Moving Averages (SMA, EMA), ATR, CCI, Williams %R
- Volume indicators, Momentum indicators

### Model Parameters
- **Algorithm**: Random Forest Classifier
- **Trees**: 150
- **Max Depth**: 10
- **Min Confidence**: 65%
- **Max Position Size**: 20% of portfolio

### Risk Management
- Maximum 20% of portfolio per position
- Minimum $100 per trade
- Stop loss at 50% position size on DOWN signals

## Performance

- **Average Model Accuracy**: 52.7%
- **Best Performing Models**: MSFT (77.7%), BNB_USD (68.8%), GBPUSDX (67.3%)
- **Portfolio Starting Capital**: $10,000 (virtual)
- **Risk-Adjusted Returns**: Tracked in portfolio history

## API Reference

### Key Classes

#### `StockPredictor`
```python
from src.prediction.prediction_system import StockPredictor

predictor = StockPredictor()
predictions = predictor.predict_all()
```

#### `PaperTrader`
```python
from src.testing.paper_trader import PaperTrader

trader = PaperTrader(initial_capital=10000)
results = trader.auto_trade_with_ai()
```

### Command Line Tools

| Command | Description |
|---------|-------------|
| `python automation/daily_automation.py` | Main automation interface |
| `python check_portfolio.py` | View current portfolio status |
| `python create_portfolio.py` | Initialize new virtual portfolio |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

⚠️ **Important**: This system uses virtual money for paper trading only. Past performance does not guarantee future results. This is for educational purposes and should not be considered financial advice.

## Support

- 📧 Issues: [GitHub Issues](https://github.com/TheUnknown550/TradingAiCode/issues)
- 📖 Documentation: See inline code comments
- 💬 Discussions: [GitHub Discussions](https://github.com/TheUnknown550/TradingAiCode/discussions)
