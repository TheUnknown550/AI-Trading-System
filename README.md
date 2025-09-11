# 🤖 AI Trading System

A comprehensive machine learning system for predicting stock market movements using technical indicators and news sentiment analysis.

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🏗️ System Architecture](#️-system-architecture)
- [📊 Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 Installation](#-installation)
- [📖 Usage Guide](#-usage-guide)
- [🤖 Machine Learning Pipeline](#-machine-learning-pipeline)
- [📈 Performance](#-performance)
- [🛠️ Configuration](#️-configuration)
- [📝 API Documentation](#-api-documentation)
- [🤝 Contributing](#-contributing)
- [⚠️ Disclaimer](#️-disclaimer)

## 🎯 Overview

This AI Trading System combines traditional technical analysis with modern machine learning and news sentiment analysis to predict short-term price movements in financial markets. The system supports:

- **Stocks**: Major US equities (AAPL, MSFT, GOOGL, etc.)
- **Forex**: Major currency pairs (EUR/USD, GBP/USD, etc.)
- **Cryptocurrency**: Popular crypto assets (BTC, ETH, SOL, etc.)

### Key Capabilities

✅ **Automated Data Collection** - Historical price data via yfinance  
✅ **Technical Analysis** - 17+ technical indicators  
✅ **News Sentiment Analysis** - Real-time news sentiment scoring  
✅ **Machine Learning** - Random Forest classification models  
✅ **Prediction System** - Binary UP/DOWN predictions with confidence scores  
✅ **Performance Tracking** - Model evaluation and backtesting metrics  

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Sources   │    │   Processing    │    │    Outputs      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Yahoo Finance │───▶│ • Technical     │───▶│ • Predictions   │
│ • News APIs     │    │   Indicators    │    │ • Confidence    │
│ • Market Data   │    │ • Sentiment     │    │ • Reports       │
│                 │    │   Analysis      │    │ • Visualizations│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Features

### 🔍 Technical Indicators
- **Trend**: SMA, EMA, MACD (Signal, Histogram)
- **Momentum**: RSI (14-period)
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV (On-Balance Volume)

### 📰 News Sentiment Analysis
- **Text Processing**: TextBlob and VADER sentiment analysis
- **News Sources**: Yahoo Finance RSS feeds
- **Features**: Polarity, subjectivity, compound scores
- **Real-time Updates**: Current sentiment integration

### 🤖 Machine Learning
- **Algorithm**: Random Forest Classifier
- **Features**: 17 technical + 6 sentiment features
- **Target**: Binary classification (UP/DOWN)
- **Validation**: 80/20 train-test split

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install yfinance pandas scikit-learn ta newsapi-python textblob vaderSentiment beautifulsoup4 requests joblib
```

### 2. Run Complete Pipeline
```bash
python scripts/run_complete_pipeline.py
```

### 3. Quick Predictions (if models exist)
```bash
python scripts/quick_predictions.py
```

## 📁 Project Structure

```
TradingAiCode/
├── 📂 src/                          # Source code modules
│   ├── 📂 data_collection/          # Data fetching logic
│   │   ├── __init__.py
│   │   └── collect_data.py          # Yahoo Finance data collection
│   ├── 📂 feature_engineering/      # Technical analysis
│   │   ├── __init__.py
│   │   └── add_indicators.py        # Technical indicators calculation
│   ├── 📂 news_analysis/            # Sentiment analysis
│   │   ├── __init__.py
│   │   └── news_analyzer.py         # News sentiment processing
│   ├── 📂 model_training/           # ML model training
│   │   ├── __init__.py
│   │   └── train_models.py          # Model training pipeline
│   ├── 📂 prediction/               # Prediction system
│   │   ├── __init__.py
│   │   └── prediction_system.py     # Real-time predictions
│   └── __init__.py
├── 📂 data/                         # Data storage
│   ├── 📂 raw/                      # Raw OHLCV data
│   ├── 📂 features/                 # Data with technical indicators
│   └── 📂 enhanced/                 # Data with sentiment features
├── 📂 models/                       # Trained ML models (.joblib files)
├── 📂 outputs/                      # Prediction outputs and reports
├── 📂 scripts/                      # Executable scripts
│   ├── run_complete_pipeline.py     # Full pipeline execution
│   └── quick_predictions.py         # Quick prediction script
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

## 🔧 Installation

### Prerequisites
- Python 3.7+
- Internet connection (for data fetching)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd TradingAiCode
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python scripts/quick_predictions.py
   ```

## 📖 Usage Guide

### Basic Usage

#### 1. Complete Pipeline (Recommended for first run)
```bash
python scripts/run_complete_pipeline.py
```
This will:
- Collect 5 years of historical data
- Calculate technical indicators
- Fetch and analyze news sentiment
- Train machine learning models
- Generate predictions

#### 2. Quick Predictions (For subsequent runs)
```bash
python scripts/quick_predictions.py
```
Uses existing trained models to make current predictions.

### Advanced Usage

#### Individual Components

**Data Collection Only:**
```python
from src.data_collection.collect_data import DataCollector
collector = DataCollector()
collector.collect_data()
```

**Feature Engineering Only:**
```python
from src.feature_engineering.add_indicators import FeatureEngineering
fe = FeatureEngineering()
fe.process_all_files()
```

**News Analysis Only:**
```python
from src.news_analysis.news_analyzer import NewsFeatureEnhancer
enhancer = NewsFeatureEnhancer()
enhancer.enhance_all_datasets()
```

**Model Training Only:**
```python
from src.model_training.train_models import ModelTrainer
trainer = ModelTrainer()
trainer.train_all_models()
```

**Predictions Only:**
```python
from src.prediction.prediction_system import StockPredictor
predictor = StockPredictor()
predictions = predictor.get_top_predictions(min_confidence=0.6)
```

## 🤖 Machine Learning Pipeline

### 1. Data Preprocessing
- **Cleaning**: Remove NaN values, handle missing data
- **Feature Engineering**: Calculate 17 technical indicators
- **Sentiment Integration**: Add 6 news sentiment features

### 2. Label Creation
- **Target Variable**: Binary classification (1 = UP, 0 = DOWN)
- **Logic**: Next day's close price > today's close price
- **Time Horizon**: 1-day ahead prediction

### 3. Model Training
- **Algorithm**: Random Forest Classifier
- **Parameters**: 150 trees, max depth 10
- **Validation**: 20% holdout test set
- **Metrics**: Accuracy, precision, recall, F1-score

### 4. Feature Importance
Top features typically include:
1. RSI (Relative Strength Index)
2. Volume indicators
3. MACD components
4. News sentiment scores
5. Bollinger Bands

## 📈 Performance

### Model Accuracy Results
```
Asset Class          Average Accuracy
────────────────────────────────────
Stocks               52.3%
Cryptocurrency       53.1%
Forex                52.8%
────────────────────────────────────
Overall Average      52.7%
```

### Top Performing Assets
1. **SOL_USD**: 57.1%
2. **INTC**: 56.3%
3. **AMZN**: 55.5%
4. **DOGE_USD**: 55.2%
5. **ADA_USD**: 54.9%

### Performance Notes
- Accuracy above 50% indicates predictive value
- Results vary by market conditions
- Higher accuracy in trending markets
- Consider ensemble methods for improvement

## 🛠️ Configuration

### Supported Assets

**Stocks:**
- AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, NFLX, AMD, INTC

**Forex:**
- EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD

**Cryptocurrency:**
- BTC-USD, ETH-USD, SOL-USD, BNB-USD, ADA-USD, DOGE-USD

### Customization Options

**Adding New Assets:**
Edit the symbol lists in `src/data_collection/collect_data.py`

**Modifying Technical Indicators:**
Update `src/feature_engineering/add_indicators.py`

**Changing Model Parameters:**
Modify parameters in `src/model_training/train_models.py`

**Adjusting Confidence Thresholds:**
Update threshold in prediction scripts

## 📝 API Documentation

### Core Classes

#### DataCollector
```python
class DataCollector:
    def __init__(self, output_dir="../../data/raw")
    def collect_data(self, period="5y", interval="1d")
```

#### FeatureEngineering
```python
class FeatureEngineering:
    def __init__(self, input_dir="../../data/raw", output_dir="../../data/features")
    def add_technical_indicators(self, df)
    def process_all_files(self)
```

#### NewsAnalyzer
```python
class NewsAnalyzer:
    def __init__(self)
    def get_sentiment_features(self, symbol)
    def analyze_sentiment(self, text)
```

#### ModelTrainer
```python
class ModelTrainer:
    def __init__(self, data_dir="../../data/enhanced", models_dir="../../models")
    def train_single_asset(self, data_file)
    def train_all_models(self)
```

#### StockPredictor
```python
class StockPredictor:
    def __init__(self, models_dir="../../models", data_dir="../../data/enhanced")
    def predict(self, asset)
    def predict_all(self)
    def get_top_predictions(self, min_confidence=0.6)
```

### Output Format

#### Prediction Output
```python
{
    'prediction': 'UP' | 'DOWN',
    'confidence': float,  # 0.0 to 1.0
    'up_probability': float,
    'down_probability': float
}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make changes with proper documentation
5. Add tests for new features
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to all functions
- Include type hints where appropriate

### Testing
```bash
python -m pytest tests/
```

## ⚠️ Disclaimer

**IMPORTANT LEGAL NOTICE:**

This AI Trading System is provided for **educational and research purposes only**. 

### Risk Warning
- **Financial Risk**: Trading financial instruments involves substantial risk of loss
- **No Guarantees**: Past performance does not guarantee future results
- **Model Limitations**: AI predictions are probabilistic, not deterministic
- **Market Volatility**: Markets can be unpredictable and highly volatile

### Legal Disclaimer
- **Not Financial Advice**: This system does not constitute financial advice
- **Professional Consultation**: Consult qualified financial advisors before trading
- **Regulatory Compliance**: Ensure compliance with local financial regulations
- **Liability**: Authors are not liable for any financial losses

### Best Practices
- **Paper Trading**: Test strategies with virtual money first
- **Risk Management**: Never risk more than you can afford to lose
- **Diversification**: Don't put all funds in one investment
- **Continuous Learning**: Stay informed about market conditions

---

## 📞 Support

For questions, issues, or contributions:

- **Issues**: Submit via GitHub Issues
- **Documentation**: Check the README and code comments
- **Community**: Join discussions in GitHub Discussions

---

**Built with ❤️ for the trading community**

*Last Updated: September 2025*
