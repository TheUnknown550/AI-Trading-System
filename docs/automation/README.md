# 🤖 Automation Guide

## Overview

The AI Trading System provides multiple automation levels, from simple portfolio checks to full 4-hour trading cycles with real-time monitoring.

## Automation Levels

### 1. 🎮 Real-Time Automation (Recommended)

**Features:**
- 4-hour trading cycles
- 30-second portfolio updates
- Live price monitoring
- Growth tracking
- Visual countdown timers

**Usage:**
```bash
python automation/daily_automation.py
# Choose option 1: Real-time automation with display
```

**What you'll see:**
- Live portfolio value updates
- Real-time P&L calculations
- Best/worst performer indicators
- Recent trading activity
- Countdown to next cycle

### 2. 🔄 Standard Automation

**Features:**
- 4-hour trading cycles
- Background operation
- Comprehensive logging
- Error recovery

**Usage:**
```bash
python automation/daily_automation.py
# Choose option 4: Basic 4-hour automation
```

### 3. 📊 Manual Operations

**Single Trade Cycle:**
```bash
python automation/daily_automation.py
# Choose option 2: Run one trading cycle
```

**Portfolio Check:**
```bash
python automation/daily_automation.py
# Choose option 3: Check portfolio status
```

## Automation Workflow

### Complete Trading Cycle

1. **System Health Check**
   - Verify models are loaded
   - Check data availability
   - Validate portfolio state

2. **Market Analysis**
   - Collect latest market data
   - Generate AI predictions
   - Filter by confidence (>65%)

3. **Trading Decisions**
   - Evaluate position sizing
   - Apply risk management
   - Execute paper trades

4. **Portfolio Update**
   - Update holdings
   - Calculate performance
   - Log all activities

5. **Real-Time Monitoring** (Option 1 only)
   - Display live portfolio
   - Show growth metrics
   - Update every 30 seconds

## Configuration

### Trading Parameters

Edit automation settings in `daily_automation.py`:

```python
# Confidence threshold
MIN_CONFIDENCE = 0.65  # 65% minimum

# Position sizing
MAX_POSITION_SIZE = 0.20  # 20% maximum per asset

# Update frequency (real-time mode)
UPDATE_INTERVAL = 30  # seconds

# Cycle frequency
CYCLE_HOURS = 4  # hours between trading cycles
```

### Risk Management

**Position Limits:**
- Maximum 20% of portfolio per asset
- Minimum $100 per trade
- Automatic diversification

**Confidence Filtering:**
- Only trades with >65% AI confidence
- Conservative approach prioritizes safety

**Error Handling:**
- Graceful API failure recovery
- Automatic retry mechanisms
- Comprehensive error logging

## Monitoring & Logging

### Real-Time Display

**Portfolio Status Display:**
```
🏪 CURRENT HOLDINGS:
------------------------------------------------------------
🟢 AAPL: 8.70 shares @ $230.03
    Growth: $+1.73 (+0.09%) | Value: $2,001.73
🟢 MSFT: 3.99 shares @ $501.01
    Growth: $+1.48 (+0.07%) | Value: $2,001.48
------------------------------------------------------------
💎 PORTFOLIO SUMMARY:
Total Portfolio: $10,012.58
Total Growth: $+12.58 (+0.13%)
Status: 🚀 GAINING
Best: TSLA (+0.53%)
```

### Log Files

**Automation Logs:**
- `logs/automation_YYYY-MM-DD.log`
- `logs/trading_YYYY-MM-DD.log`
- `logs/errors_YYYY-MM-DD.log`

**Log Levels:**
- **INFO**: Normal operations
- **WARNING**: Recoverable issues
- **ERROR**: Serious problems
- **DEBUG**: Detailed troubleshooting

## Advanced Features

### Custom Automation Scripts

Create your own automation:

```python
from automation.daily_automation import run_paper_trading, check_system_status

def custom_automation():
    # Your custom logic here
    if check_system_status():
        success = run_paper_trading()
        if success:
            print("✅ Trading successful")
        else:
            print("❌ Trading had issues")

if __name__ == "__main__":
    custom_automation()
```

### Scheduled Automation

**Using Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily, repeat every 4 hours
4. Action: Start program `python.exe`
5. Arguments: `automation/daily_automation.py`
6. Start in: `C:\path\to\TradingAiCode`

**Using cron (Linux/macOS):**
```bash
# Edit crontab
crontab -e

# Add entry for every 4 hours
0 */4 * * * cd /path/to/TradingAiCode && python automation/daily_automation.py
```

## Performance Optimization

### Memory Management

**Large Portfolio Optimization:**
```python
# Process positions in batches
BATCH_SIZE = 10
```

**Model Loading Optimization:**
```python
# Lazy loading for better memory usage
LAZY_MODEL_LOADING = True
```

### Speed Optimization

**Parallel Processing:**
```python
# Enable parallel predictions
PARALLEL_PREDICTIONS = True
N_JOBS = 4  # Use 4 CPU cores
```

## Troubleshooting

### Common Issues

**Automation stops unexpectedly:**
- Check log files for errors
- Verify internet connection
- Ensure sufficient disk space

**Predictions seem incorrect:**
- Retrain models with fresh data
- Check data quality
- Verify feature calculations

**Real-time display not updating:**
- Check yfinance API connectivity
- Verify portfolio file permissions
- Restart automation

### Recovery Procedures

**Restart from failure:**
```bash
# Check system status
python automation/daily_automation.py
# Choose option 3: System check

# If models missing, retrain
python src/training/train_models.py

# If portfolio corrupted, recreate
python create_portfolio.py
```

## Best Practices

### 📋 Daily Checklist

- [ ] Check overnight log files
- [ ] Verify portfolio performance
- [ ] Monitor system resources
- [ ] Review AI predictions accuracy

### 🔒 Security Guidelines

- Never run with real money without thorough testing
- Keep portfolio files backed up
- Monitor for unusual trading patterns
- Set reasonable position limits

### 📈 Performance Monitoring

- Track accuracy trends over time
- Monitor portfolio growth consistency
- Review risk-adjusted returns
- Analyze prediction confidence distributions

## Next Steps

- **📊 [Analysis Guide](../analysis/)** - Deep dive into performance metrics
- **🏛️ [Archive](../archive/)** - Historical documentation and lessons learned
