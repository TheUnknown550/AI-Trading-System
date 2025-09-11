# 🛠️ Setup Guide

## System Requirements

- **Python 3.9+**
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space for data and models
- **Network**: Internet connection for real-time data

## Installation

### 1. Python Environment Setup

```bash
# Verify Python version
python --version

# Create virtual environment (recommended)
python -m venv trading_env
source trading_env/bin/activate  # On Windows: trading_env\Scripts\activate
```

### 2. Install Dependencies

```bash
# Core dependencies
pip install yfinance pandas scikit-learn joblib numpy

# Additional utilities
pip install matplotlib seaborn tabulate colorama

# Optional: Jupyter for analysis
pip install jupyter notebook
```

### 3. System Initialization

```bash
# 1. Collect market data
python CollectStocksData.py

# 2. Add technical indicators
python AddIndicatorsToStocksData.py

# 3. Train AI models
python src/training/train_models.py

# 4. Initialize portfolio
python create_portfolio.py
```

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# API Settings
YFINANCE_TIMEOUT=30
DATA_UPDATE_FREQUENCY=daily

# Trading Settings
MIN_CONFIDENCE=0.65
MAX_POSITION_SIZE=0.20
INITIAL_CAPITAL=10000

# Automation Settings
CYCLE_INTERVAL_HOURS=4
UPDATE_INTERVAL_SECONDS=30
```

### Model Configuration

Edit `src/config/model_config.py`:

```python
MODEL_PARAMS = {
    'n_estimators': 150,
    'max_depth': 10,
    'min_samples_split': 5,
    'random_state': 42
}

TRADING_PARAMS = {
    'min_confidence': 0.65,
    'max_position_size': 0.20,
    'min_trade_amount': 100
}
```

## Verification

### Test Installation

```bash
# Quick system check
python -c "import yfinance, pandas, sklearn; print('✅ All dependencies installed')"

# Verify data files
python -c "import os; print('✅ Data files exist' if os.path.exists('MarketData') else '❌ Run CollectStocksData.py')"

# Check models
python -c "import os; print(f'✅ {len(os.listdir("models"))} models found' if os.path.exists('models') else '❌ Run train_models.py')"
```

### First Run Test

```bash
# Test portfolio system
python check_portfolio.py

# Test automation menu
python automation/daily_automation.py
# Choose option 3 for system check
```

## Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'yfinance'`
```bash
Solution: pip install yfinance
```

**Issue**: `FileNotFoundError: models directory not found`
```bash
Solution: python src/training/train_models.py
```

**Issue**: `No portfolio file found`
```bash
Solution: python create_portfolio.py
```

**Issue**: Models showing low accuracy
```bash
Solution: 
1. python CollectStocksData.py  # Refresh data
2. python AddIndicatorsToStocksData.py  # Recalculate features
3. python src/training/train_models.py  # Retrain models
```

### Performance Optimization

**For faster training:**
```python
# Reduce model complexity in model_config.py
MODEL_PARAMS = {
    'n_estimators': 100,  # Reduced from 150
    'max_depth': 8,       # Reduced from 10
}
```

**For memory optimization:**
```python
# Process assets in batches
BATCH_SIZE = 5  # Process 5 assets at a time
```

## Next Steps

After successful setup:

1. **📊 [Analysis Guide](../analysis/)** - Understand your models and performance
2. **🤖 [Automation Guide](../automation/)** - Set up automated trading
3. **📈 Portfolio Management** - Learn portfolio optimization strategies

## Support

- **Documentation**: Check inline code comments
- **Logs**: Review `logs/` directory for debugging
- **Community**: GitHub Issues for questions and bug reports
