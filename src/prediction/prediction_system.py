"""
Prediction System Module
Makes real-time predictions using trained models
"""

import pandas as pd
import joblib
import os
import sys
from glob import glob
from datetime import datetime
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from news_analysis.news_analyzer import NewsAnalyzer

class StockPredictor:
    def __init__(self, models_dir="../../models", data_dir="../../data/enhanced"):
        """Initialize the stock predictor"""
        self.models_dir = models_dir
        self.data_dir = data_dir
        self.models = {}
        self.news_analyzer = NewsAnalyzer()
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        model_files = glob(os.path.join(self.models_dir, '*_enhanced_rf_model.joblib'))
        
        for model_file in model_files:
            asset = os.path.basename(model_file).replace('_enhanced_rf_model.joblib', '')
            try:
                self.models[asset] = joblib.load(model_file)
                print(f"✅ Loaded model for {asset}")
            except Exception as e:
                print(f"❌ Failed to load model for {asset}: {e}")
        
        print(f"📊 Loaded {len(self.models)} models")
    
    def get_latest_features(self, asset):
        """
        Get the latest features for an asset (simulated with last row of data)
        
        Args:
            asset (str): Asset symbol
            
        Returns:
            numpy.ndarray: Feature array for prediction
        """
        feature_file = os.path.join(self.data_dir, f'{asset}_enhanced_features.csv')
        
        if not os.path.exists(feature_file):
            print(f"Feature file not found for {asset}")
            return None
        
        df = pd.read_csv(feature_file)
        
        # Get the last row (most recent data) and prepare features
        last_row = df.iloc[-1].copy()
        
        # Remove non-feature columns
        exclude_cols = ['Date', 'Close', 'NextClose', 'Label']
        for col in exclude_cols:
            if col in last_row.index:
                last_row = last_row.drop(col)
        
        # Get current news sentiment (this would be real-time in production)
        current_sentiment = self.news_analyzer.get_sentiment_features(asset)
        
        # Update news features with current sentiment
        for key, value in current_sentiment.items():
            last_row[f'news_{key}'] = value
        
        return last_row.values.reshape(1, -1)
    
    def predict(self, asset):
        """
        Make a prediction for an asset
        
        Args:
            asset (str): Asset symbol
            
        Returns:
            tuple: (prediction_dict, error_message)
        """
        if asset not in self.models:
            return None, f"No model available for {asset}"
        
        features = self.get_latest_features(asset)
        if features is None:
            return None, f"Could not get features for {asset}"
        
        try:
            # Get prediction (0 = down, 1 = up)
            prediction = self.models[asset].predict(features)[0]
            
            # Get prediction probability
            proba = self.models[asset].predict_proba(features)[0]
            confidence = max(proba)
            
            return {
                'prediction': 'UP' if prediction == 1 else 'DOWN',
                'confidence': confidence,
                'up_probability': proba[1] if len(proba) > 1 else 0,
                'down_probability': proba[0] if len(proba) > 0 else 0
            }, None
            
        except Exception as e:
            return None, f"Prediction failed for {asset}: {e}"
    
    def predict_all(self):
        """Make predictions for all available assets"""
        predictions = {}
        
        print(f"🔮 Making predictions for {len(self.models)} assets...")
        
        for asset in self.models.keys():
            pred, error = self.predict(asset)
            if pred:
                predictions[asset] = pred
            else:
                print(f"❌ Error predicting {asset}: {error}")
        
        return predictions
    
    def get_top_predictions(self, min_confidence=0.6):
        """
        Get top predictions with high confidence
        
        Args:
            min_confidence (float): Minimum confidence threshold
            
        Returns:
            list: List of (asset, prediction) tuples sorted by confidence
        """
        all_predictions = self.predict_all()
        
        # Filter by confidence and sort
        high_confidence = {
            asset: pred for asset, pred in all_predictions.items() 
            if pred['confidence'] >= min_confidence
        }
        
        # Sort by confidence
        sorted_predictions = sorted(
            high_confidence.items(), 
            key=lambda x: x[1]['confidence'], 
            reverse=True
        )
        
        return sorted_predictions

class PredictionDisplay:
    """Class for displaying predictions in a nice format"""
    
    @staticmethod
    def display_predictions(predictions, title="AI TRADING PREDICTIONS"):
        """
        Display predictions in a formatted table
        
        Args:
            predictions (list): List of (asset, prediction) tuples
            title (str): Title for the display
        """
        print(f"\n{'='*70}")
        print(f"{title} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        if not predictions:
            print("No high-confidence predictions available.")
            return
        
        # Header
        print(f"{'Asset':<12} {'Prediction':<10} {'Confidence':<12} {'Up Prob':<10} {'Down Prob':<10}")
        print("-" * 70)
        
        # Predictions
        for asset, pred in predictions:
            print(f"{asset:<12} {pred['prediction']:<10} {pred['confidence']:<12.3f} "
                  f"{pred['up_probability']:<10.3f} {pred['down_probability']:<10.3f}")
    
    @staticmethod
    def save_predictions_to_file(predictions, output_dir="../../outputs"):
        """
        Save predictions to a CSV file
        
        Args:
            predictions (list): List of (asset, prediction) tuples
            output_dir (str): Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert to DataFrame
        data = []
        for asset, pred in predictions:
            data.append({
                'asset': asset,
                'prediction': pred['prediction'],
                'confidence': pred['confidence'],
                'up_probability': pred['up_probability'],
                'down_probability': pred['down_probability'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(data)
        
        # Save to file
        filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        
        print(f"💾 Predictions saved to: {filepath}")

if __name__ == "__main__":
    print("🚀 Initializing Stock Prediction System...")
    predictor = StockPredictor()
    
    print("\n🔮 Getting high-confidence predictions...")
    top_predictions = predictor.get_top_predictions(min_confidence=0.55)
    
    # Display predictions
    PredictionDisplay.display_predictions(top_predictions)
    
    # Save predictions to file
    if top_predictions:
        PredictionDisplay.save_predictions_to_file(top_predictions)
    
    print(f"\n📊 Summary:")
    print(f"Total assets analyzed: {len(predictor.models)}")
    print(f"High-confidence predictions: {len(top_predictions)}")
    
    print("\n✅ Prediction system completed!")
