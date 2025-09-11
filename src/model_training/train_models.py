"""
Model Training Module
Trains machine learning models for stock prediction
"""

import pandas as pd
import os
import sys
from glob import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.paths import get_data_dir, get_models_dir

class ModelTrainer:
    def __init__(self, data_dir=None, models_dir=None):
        """Initialize model trainer"""
        if data_dir is None:
            self.data_dir = get_data_dir("enhanced")  # MarketData_Features_Enhanced
        else:
            self.data_dir = data_dir
            
        if models_dir is None:
            self.models_dir = get_models_dir()  # models/
        else:
            self.models_dir = models_dir
        
        # Create models directory
        os.makedirs(self.models_dir, exist_ok=True)
    
    def create_labels(self, df):
        """
        Create binary labels for price movement prediction
        
        Args:
            df (pandas.DataFrame): DataFrame with 'Close' column
            
        Returns:
            pandas.DataFrame: DataFrame with labels added
        """
        if 'Close' not in df.columns:
            raise ValueError("'Close' column not found in dataframe")
        
        # Create label: 1 if next day's close > today's close, else 0
        df['NextClose'] = df['Close'].shift(-1)
        df['Label'] = (df['NextClose'] > df['Close']).astype(int)
        
        # Drop last row (no next day)
        df = df[:-1]
        
        return df
    
    def prepare_features(self, df):
        """
        Prepare features for training by removing non-feature columns
        
        Args:
            df (pandas.DataFrame): DataFrame with features and labels
            
        Returns:
            tuple: (X, y) features and labels
        """
        # Remove non-feature columns
        exclude_cols = ['NextClose', 'Label', 'Date', 'Close']
        X = df.drop(exclude_cols, axis=1, errors='ignore')
        y = df['Label']
        
        return X, y
    
    def train_model(self, X, y, model_params=None):
        """
        Train a Random Forest model
        
        Args:
            X (pandas.DataFrame): Features
            y (pandas.Series): Labels
            model_params (dict): Model parameters
            
        Returns:
            tuple: (model, accuracy, classification_report)
        """
        if model_params is None:
            model_params = {
                'n_estimators': 150,
                'max_depth': 10,
                'random_state': 42
            }
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        clf = RandomForestClassifier(**model_params)
        clf.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return clf, accuracy, report, X.columns.tolist()
    
    def train_single_asset(self, data_file):
        """
        Train a model for a single asset
        
        Args:
            data_file (str): Path to asset data file
            
        Returns:
            dict: Training results
        """
        asset = os.path.basename(data_file).replace('_enhanced_features.csv', '')
        
        try:
            # Load data
            df = pd.read_csv(data_file)
            
            # Create labels
            df_with_labels = self.create_labels(df)
            
            if len(df_with_labels) < 10:
                return {
                    'asset': asset,
                    'success': False,
                    'error': 'Not enough data'
                }
            
            # Prepare features
            X, y = self.prepare_features(df_with_labels)
            
            # Train model
            model, accuracy, report, feature_names = self.train_model(X, y)
            
            # Save model
            model_filename = f'{asset}_enhanced_rf_model.joblib'
            model_path = os.path.join(self.models_dir, model_filename)
            joblib.dump(model, model_path)
            
            # Get feature importance
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            return {
                'asset': asset,
                'success': True,
                'accuracy': accuracy,
                'report': report,
                'feature_importance': feature_importance,
                'model_path': model_path,
                'features_used': len(feature_names)
            }
            
        except Exception as e:
            return {
                'asset': asset,
                'success': False,
                'error': str(e)
            }
    
    def train_all_models(self):
        """Train models for all enhanced datasets"""
        enhanced_files = glob(os.path.join(self.data_dir, '*_enhanced_features.csv'))
        
        if not enhanced_files:
            print(f"⚠️ No enhanced feature files found in {self.data_dir}")
            return []
        
        print(f"🤖 Training models for {len(enhanced_files)} assets...")
        print(f"📁 Data directory: {self.data_dir}")
        print(f"📁 Models directory: {self.models_dir}")
        
        results = []
        successful_training = 0
        failed_training = 0
        
        for file in enhanced_files:
            asset = os.path.basename(file).replace('_enhanced_features.csv', '')
            print(f"\n🔧 Training model for {asset}...")
            
            result = self.train_single_asset(file)
            results.append(result)
            
            if result['success']:
                print(f"✅ {asset} - Accuracy: {result['accuracy']:.3f}")
                print(f"📊 Top 3 features:")
                for i, row in result['feature_importance'].head(3).iterrows():
                    print(f"   {row['feature']}: {row['importance']:.3f}")
                successful_training += 1
            else:
                print(f"❌ {asset} - Error: {result['error']}")
                failed_training += 1
        
        print(f"\n🤖 Model Training Summary:")
        print(f"✅ Successful: {successful_training}")
        print(f"❌ Failed: {failed_training}")
        
        if successful_training > 0:
            avg_accuracy = sum([r['accuracy'] for r in results if r['success']]) / successful_training
            print(f"📊 Average Accuracy: {avg_accuracy:.3f}")
        
        print(f"📁 Models saved in: {os.path.abspath(self.models_dir)}")
        
        return results

if __name__ == "__main__":
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Train all models
    results = trainer.train_all_models()
    
    print("\n✅ Model training completed!")
