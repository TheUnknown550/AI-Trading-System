"""
Quick Prediction Script
Makes predictions using existing trained models
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from prediction.prediction_system import StockPredictor, PredictionDisplay

def quick_predictions():
    """Make quick predictions with existing models"""
    print("🔮 Quick AI Trading Predictions...")
    print("=" * 50)
    
    try:
        # Initialize predictor
        predictor = StockPredictor()
        
        # Make predictions
        top_predictions = predictor.get_top_predictions(min_confidence=0.55)
        
        # Display results
        PredictionDisplay.display_predictions(top_predictions)
        
        if top_predictions:
            PredictionDisplay.save_predictions_to_file(top_predictions)
        
        print(f"\n📊 Summary:")
        print(f"Total models loaded: {len(predictor.models)}")
        print(f"High-confidence predictions: {len(top_predictions)}")
        
    except Exception as e:
        print(f"❌ Error making predictions: {e}")
        print("💡 Try running the complete pipeline first: python scripts/run_complete_pipeline.py")

if __name__ == "__main__":
    quick_predictions()
