import yfinance as yf
import pandas as pd
import os

# --- 1) Symbols lists ---
stocks = [
    "AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","NFLX","AMD","INTC"
]

forex = [
    "EURUSD=X","JPY=X","GBPUSD=X","CHF=X","AUDUSD=X","CAD=X"
]

crypto = [
    "BTC-USD","ETH-USD","SOL-USD","BNB-USD","ADA-USD","DOGE-USD"
]

all_symbols = stocks + forex + crypto

# --- 2) Output folder ---
output_dir = "MarketData"
os.makedirs(output_dir, exist_ok=True)

# --- 3) Download function ---
for symbol in all_symbols:
    print(f"📥 Downloading {symbol} ...")
    try:
        df = yf.download(symbol, period="5y", interval="1d")
        if not df.empty:
            safe_name = symbol.replace("=", "").replace("-", "_")
            file_path = os.path.join(output_dir, f"{safe_name}.csv")
            df.to_csv(file_path)
            print(f"✅ Saved: {file_path}")
        else:
            print(f"⚠️ No data for {symbol}")
    except Exception as e:
        print(f"❌ Failed {symbol}: {e}")

print("\n✅ All downloads finished.")
