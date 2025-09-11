"""
Data Collection Module
Collects historical market data for stocks, forex, and cryptocurrency
"""

import yfinance as yf
import pandas as pd
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class DataCollector:
    def __init__(self, output_dir="../../data/raw"):
        """Initialize the data collector with output directory"""
        self.output_dir = output_dir
        
        # Symbol definitions
        self.stocks = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX", "AMD", "INTC"
        ]
        
        self.forex = [
            "EURUSD=X", "JPY=X", "GBPUSD=X", "CHF=X", "AUDUSD=X", "CAD=X"
        ]
        
        self.crypto = [
            "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD", "DOGE-USD"
        ]
        
        self.all_symbols = self.stocks + self.forex + self.crypto
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def collect_data(self, period="5y", interval="1d"):
        """
        Collect historical market data for all symbols
        
        Args:
            period (str): Data period (e.g., "5y", "2y", "1y")
            interval (str): Data interval (e.g., "1d", "1h")
        """
        print(f"📊 Starting data collection for {len(self.all_symbols)} symbols...")
        print(f"📁 Output directory: {self.output_dir}")
        
        successful_downloads = 0
        failed_downloads = 0
        
        for symbol in self.all_symbols:
            print(f"📥 Downloading {symbol}...")
            try:
                # Download data
                df = yf.download(symbol, period=period, interval=interval)
                
                if not df.empty:
                    # Reset index to make 'Date' a column
                    df.reset_index(inplace=True)
                    
                    # Create safe filename
                    safe_name = symbol.replace("=", "").replace("-", "_")
                    file_path = os.path.join(self.output_dir, f"{safe_name}.csv")
                    
                    # Save to CSV
                    df.to_csv(file_path, index=False)
                    print(f"✅ Saved: {file_path} ({len(df)} rows)")
                    successful_downloads += 1
                else:
                    print(f"⚠️ No data found for {symbol}")
                    failed_downloads += 1
                    
            except Exception as e:
                print(f"❌ Failed to download {symbol}: {e}")
                failed_downloads += 1
        
        print(f"\n📊 Data Collection Summary:")
        print(f"✅ Successful: {successful_downloads}")
        print(f"❌ Failed: {failed_downloads}")
        print(f"📁 Files saved in: {os.path.abspath(self.output_dir)}")
        
        return successful_downloads, failed_downloads

if __name__ == "__main__":
    # Initialize collector
    collector = DataCollector()
    
    # Collect data
    collector.collect_data()
    
    print("\n✅ Data collection completed!")
