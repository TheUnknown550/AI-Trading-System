#!/usr/bin/env python3
"""
Test script to verify all paths are correct and files are created in the right directories
"""

import os
import sys

# Add src to path
sys.path.append('src')

def test_data_collection():
    """Test data collection paths"""
    print("🔍 Testing Data Collection...")
    
    from data_collection.collect_data import DataCollector
    collector = DataCollector()
    
    print(f"✅ Data collector output dir: {collector.output_dir}")
    expected = os.path.join(os.getcwd(), "MarketData")
    if os.path.abspath(collector.output_dir) == expected:
        print("✅ Data collection path is correct!")
    else:
        print(f"❌ Expected: {expected}")
        print(f"❌ Got: {os.path.abspath(collector.output_dir)}")

def test_feature_engineering():
    """Test feature engineering paths"""
    print("\n🔍 Testing Feature Engineering...")
    
    from feature_engineering.add_indicators import FeatureEngineering
    feature_eng = FeatureEngineering()
    
    print(f"✅ Input dir: {feature_eng.input_dir}")
    print(f"✅ Output dir: {feature_eng.output_dir}")
    
    expected_input = os.path.join(os.getcwd(), "MarketData")
    expected_output = os.path.join(os.getcwd(), "MarketData_Features")
    
    if os.path.abspath(feature_eng.input_dir) == expected_input:
        print("✅ Feature input path is correct!")
    else:
        print(f"❌ Input Expected: {expected_input}")
        print(f"❌ Input Got: {os.path.abspath(feature_eng.input_dir)}")
        
    if os.path.abspath(feature_eng.output_dir) == expected_output:
        print("✅ Feature output path is correct!")
    else:
        print(f"❌ Output Expected: {expected_output}")
        print(f"❌ Output Got: {os.path.abspath(feature_eng.output_dir)}")

def test_model_training():
    """Test model training paths"""
    print("\n🔍 Testing Model Training...")
    
    from model_training.train_models import ModelTrainer
    trainer = ModelTrainer()
    
    print(f"✅ Data dir: {trainer.data_dir}")
    print(f"✅ Models dir: {trainer.models_dir}")
    
    expected_data = os.path.join(os.getcwd(), "MarketData_Features_Enhanced")
    expected_models = os.path.join(os.getcwd(), "models")
    
    if os.path.abspath(trainer.data_dir) == expected_data:
        print("✅ Model training data path is correct!")
    else:
        print(f"❌ Data Expected: {expected_data}")
        print(f"❌ Data Got: {os.path.abspath(trainer.data_dir)}")
        
    if os.path.abspath(trainer.models_dir) == expected_models:
        print("✅ Model training models path is correct!")
    else:
        print(f"❌ Models Expected: {expected_models}")
        print(f"❌ Models Got: {os.path.abspath(trainer.models_dir)}")

def test_prediction_system():
    """Test prediction system paths"""
    print("\n🔍 Testing Prediction System...")
    
    from prediction.prediction_system import StockPredictor
    predictor = StockPredictor()
    
    print(f"✅ Models dir: {predictor.models_dir}")
    print(f"✅ Data dir: {predictor.data_dir}")
    
    expected_models = os.path.join(os.getcwd(), "models")
    expected_data = os.path.join(os.getcwd(), "MarketData_Features_Enhanced")
    
    if os.path.abspath(predictor.models_dir) == expected_models:
        print("✅ Predictor models path is correct!")
    else:
        print(f"❌ Models Expected: {expected_models}")
        print(f"❌ Models Got: {os.path.abspath(predictor.models_dir)}")
        
    if os.path.abspath(predictor.data_dir) == expected_data:
        print("✅ Predictor data path is correct!")
    else:
        print(f"❌ Data Expected: {expected_data}")
        print(f"❌ Data Got: {os.path.abspath(predictor.data_dir)}")

def test_portfolio_path():
    """Test portfolio file path"""
    print("\n🔍 Testing Portfolio Path...")
    
    from testing.paper_trader import PaperTrader
    trader = PaperTrader()
    
    print(f"✅ Portfolio file: {trader.portfolio_file}")
    
    expected = os.path.join(os.getcwd(), "outputs", "paper_portfolio.json")
    
    if os.path.abspath(trader.portfolio_file) == expected:
        print("✅ Portfolio path is correct!")
    else:
        print(f"❌ Expected: {expected}")
        print(f"❌ Got: {os.path.abspath(trader.portfolio_file)}")

def main():
    print("🧪 TESTING ALL FILE PATHS")
    print("=" * 50)
    
    try:
        test_data_collection()
        test_feature_engineering()
        test_model_training()
        test_prediction_system()
        test_portfolio_path()
        
        print("\n🎉 ALL PATH TESTS COMPLETED!")
        print("All files should now be created within the project directory.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
