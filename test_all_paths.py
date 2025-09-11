#!/usr/bin/env python3
"""
Complete Path Testing Script
Tests all components to ensure proper file paths
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_data_collection():
    """Test data collection paths"""
    try:
        from data_collection.collect_data import DataCollector
        collector = DataCollector()
        print("✅ Data collection module loaded successfully")
        
        # Test data directory
        from utils.paths import get_data_dir
        data_dir = get_data_dir("raw")
        print(f"✅ Raw data will be saved to: {data_dir}")
        return True
    except Exception as e:
        print(f"❌ Data collection test failed: {e}")
        return False

def test_feature_engineering():
    """Test feature engineering paths"""
    try:
        from feature_engineering.add_indicators import FeatureEngineering
        fe = FeatureEngineering()
        print("✅ Feature engineering module loaded successfully")
        
        from utils.paths import get_data_dir
        features_dir = get_data_dir("features")
        print(f"✅ Features will be saved to: {features_dir}")
        return True
    except Exception as e:
        print(f"❌ Feature engineering test failed: {e}")
        return False

def test_model_training():
    """Test model training paths"""
    try:
        from model_training.train_models import ModelTrainer
        trainer = ModelTrainer()
        print("✅ Model training module loaded successfully")
        
        from utils.paths import get_models_dir
        models_dir = get_models_dir()
        print(f"✅ Models will be saved to: {models_dir}")
        return True
    except Exception as e:
        print(f"❌ Model training test failed: {e}")
        return False

def test_prediction_system():
    """Test prediction system paths"""
    try:
        from prediction.prediction_system import StockPredictor
        predictor = StockPredictor()
        print("✅ Prediction system module loaded successfully")
        
        from utils.paths import get_outputs_dir
        outputs_dir = get_outputs_dir()
        print(f"✅ Predictions will be saved to: {outputs_dir}")
        return True
    except Exception as e:
        print(f"❌ Prediction system test failed: {e}")
        return False

def test_paper_trader():
    """Test paper trader paths"""
    try:
        from testing.paper_trader import PaperTrader
        trader = PaperTrader()
        print("✅ Paper trader module loaded successfully")
        
        portfolio_file = trader.portfolio_file
        print(f"✅ Portfolio will be saved to: {portfolio_file}")
        return True
    except Exception as e:
        print(f"❌ Paper trader test failed: {e}")
        return False

def test_directory_structure():
    """Test that all required directories exist or can be created"""
    from utils.paths import get_data_dir, get_models_dir, get_outputs_dir
    
    directories = [
        ("Raw Data", get_data_dir("raw")),
        ("Features", get_data_dir("features")),
        ("Enhanced Features", get_data_dir("enhanced")),
        ("Models", get_models_dir()),
        ("Outputs", get_outputs_dir())
    ]
    
    for name, path in directories:
        path_obj = Path(path)
        if not path_obj.exists():
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                print(f"✅ Created {name} directory: {path}")
            except Exception as e:
                print(f"❌ Failed to create {name} directory: {e}")
                return False
        else:
            print(f"✅ {name} directory exists: {path}")
    
    return True

def main():
    """Run all path tests"""
    print("🧪 Testing All AI Trading System Paths")
    print("=" * 50)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Data Collection", test_data_collection),
        ("Feature Engineering", test_feature_engineering),
        ("Model Training", test_model_training),
        ("Prediction System", test_prediction_system),
        ("Paper Trader", test_paper_trader)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Tests Passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All path tests passed! Your system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
