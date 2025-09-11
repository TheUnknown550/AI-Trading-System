"""
Feature Engineering Module
Adds technical indicators to raw market data
"""

import pandas as pd
import ta
import os
import sys
from glob import glob

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class FeatureEngineering:
    def __init__(self, input_dir="../../data/raw", output_dir="../../data/features"):
        """Initialize feature engineering with input and output directories"""
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def add_technical_indicators(self, df):
        """
        Add technical indicators to a dataframe
        
        Args:
            df (pandas.DataFrame): DataFrame with OHLCV data
            
        Returns:
            pandas.DataFrame: DataFrame with added technical indicators
        """
        # Identify numeric columns that exist in this CSV
        numeric_cols = [col for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] 
                       if col in df.columns]
        
        # Convert numeric columns to float
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Drop rows with NaN in numeric columns
        df.dropna(subset=numeric_cols, inplace=True)
        
        # --- 1) Moving averages ---
        df["SMA_10"] = ta.trend.SMAIndicator(close=df["Close"], window=10).sma_indicator()
        df["SMA_20"] = ta.trend.SMAIndicator(close=df["Close"], window=20).sma_indicator()
        df["EMA_10"] = ta.trend.EMAIndicator(close=df["Close"], window=10).ema_indicator()
        df["EMA_20"] = ta.trend.EMAIndicator(close=df["Close"], window=20).ema_indicator()
        
        # --- 2) Momentum indicators ---
        df["RSI_14"] = ta.momentum.RSIIndicator(close=df["Close"], window=14).rsi()
        macd = ta.trend.MACD(close=df["Close"])
        df["MACD"] = macd.macd()
        df["MACD_signal"] = macd.macd_signal()
        df["MACD_hist"] = macd.macd_diff()
        
        # --- 3) Volatility ---
        df["ATR_14"] = ta.volatility.AverageTrueRange(
            high=df["High"], low=df["Low"], close=df["Close"], window=14
        ).average_true_range()
        
        bb = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
        df["BB_upper"] = bb.bollinger_hband()
        df["BB_middle"] = bb.bollinger_mavg()
        df["BB_lower"] = bb.bollinger_lband()
        
        # --- 4) Volume indicator ---
        if "Volume" in df.columns:
            df["OBV"] = ta.volume.OnBalanceVolumeIndicator(
                close=df["Close"], volume=df["Volume"]
            ).on_balance_volume()
        
        # Drop rows with NaN from indicators
        df = df.dropna()
        
        return df
    
    def process_all_files(self):
        """Process all CSV files in the input directory"""
        # Get all CSV files
        csv_files = glob(os.path.join(self.input_dir, "*.csv"))
        
        if not csv_files:
            print(f"⚠️ No CSV files found in {self.input_dir}")
            return 0, 0
        
        print(f"🔧 Processing {len(csv_files)} files...")
        print(f"📁 Input directory: {self.input_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        
        successful_processing = 0
        failed_processing = 0
        
        for file_path in csv_files:
            file_name = os.path.basename(file_path)
            print(f"⚡ Processing {file_name}...")
            
            try:
                # Read CSV with Date column
                df = pd.read_csv(file_path, parse_dates=True)
                
                # Add technical indicators
                df_with_features = self.add_technical_indicators(df)
                
                # Create output filename
                output_filename = file_name.replace(".csv", "_features.csv")
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save processed data
                df_with_features.to_csv(output_path, index=False)
                print(f"✅ Saved {output_filename} ({len(df_with_features)} rows)")
                successful_processing += 1
                
            except Exception as e:
                print(f"❌ Failed to process {file_name}: {e}")
                failed_processing += 1
        
        print(f"\n🔧 Feature Engineering Summary:")
        print(f"✅ Successful: {successful_processing}")
        print(f"❌ Failed: {failed_processing}")
        print(f"📁 Files saved in: {os.path.abspath(self.output_dir)}")
        
        return successful_processing, failed_processing

if __name__ == "__main__":
    # Initialize feature engineering
    fe = FeatureEngineering()
    
    # Process all files
    fe.process_all_files()
    
    print("\n✅ Feature engineering completed!")
