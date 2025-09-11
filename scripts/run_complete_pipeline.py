"""
Complete Pipeline Script
Runs the entire AI trading system pipeline from data collection to predictions
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from data_collection.collect_data import DataCollector
from feature_engineering.add_indicators import FeatureEngineering
from news_analysis.news_analyzer import NewsFeatureEnhancer
from model_training.train_models import ModelTrainer
from prediction.prediction_system import StockPredictor, PredictionDisplay

def run_complete_pipeline():
    """Run the complete AI trading pipeline"""
    print("🚀 Starting Complete AI Trading Pipeline...")
    print("=" * 60)
    
    # Step 1: Data Collection
    print("\n📊 Step 1: Data Collection")
    collector = DataCollector()
    successful_downloads, failed_downloads = collector.collect_data()
    
    if successful_downloads == 0:
        print("❌ No data collected. Exiting pipeline.")
        return
    
    # Step 2: Feature Engineering
    print("\n🔧 Step 2: Feature Engineering")
    fe = FeatureEngineering()
    successful_features, failed_features = fe.process_all_files()
    
    if successful_features == 0:
        print("❌ No features created. Exiting pipeline.")
        return
    
    # Step 3: News Analysis Enhancement
    print("\n📰 Step 3: News Analysis Enhancement")
    enhancer = NewsFeatureEnhancer()
    successful_enhancements, failed_enhancements = enhancer.enhance_all_datasets()
    
    if successful_enhancements == 0:
        print("❌ No datasets enhanced. Exiting pipeline.")
        return
    
    # Step 4: Model Training
    print("\n🤖 Step 4: Model Training")
    trainer = ModelTrainer()
    results = trainer.train_all_models()
    
    successful_models = len([r for r in results if r['success']])
    if successful_models == 0:
        print("❌ No models trained. Exiting pipeline.")
        return
    
    # Step 5: Make Predictions
    print("\n🔮 Step 5: Making Predictions")
    predictor = StockPredictor()
    top_predictions = predictor.get_top_predictions(min_confidence=0.55)
    
    # Display results
    PredictionDisplay.display_predictions(top_predictions, "FINAL AI TRADING PREDICTIONS")
    
    if top_predictions:
        PredictionDisplay.save_predictions_to_file(top_predictions)
    
    # Final Summary
    print(f"\n🎯 PIPELINE SUMMARY:")
    print(f"=" * 60)
    print(f"📊 Data Collection: {successful_downloads} assets")
    print(f"🔧 Feature Engineering: {successful_features} datasets")
    print(f"📰 News Enhancement: {successful_enhancements} datasets")
    print(f"🤖 Model Training: {successful_models} models")
    print(f"🔮 High-Confidence Predictions: {len(top_predictions)}")
    print(f"=" * 60)
    print("✅ Complete AI Trading Pipeline Finished!")

if __name__ == "__main__":
    run_complete_pipeline()
