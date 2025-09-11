"""
News Analysis Module
Fetches and analyzes news sentiment for financial assets
"""

import pandas as pd
import requests
import xml.etree.ElementTree as ET
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class NewsAnalyzer:
    def __init__(self):
        """Initialize the news analyzer"""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def get_yahoo_finance_news(self, symbol, max_articles=10):
        """
        Fetch news from Yahoo Finance for a given symbol
        
        Args:
            symbol (str): Financial symbol (e.g., 'AAPL', 'BTC-USD')
            max_articles (int): Maximum number of articles to fetch
            
        Returns:
            list: List of news articles with title, date, and description
        """
        try:
            # Yahoo Finance RSS feed for news
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Parse RSS feed
                root = ET.fromstring(response.content)
                
                news_items = []
                for item in root.findall('.//item')[:max_articles]:
                    title = item.find('title')
                    pub_date = item.find('pubDate')
                    description = item.find('description')
                    
                    if title is not None:
                        news_items.append({
                            'title': title.text,
                            'date': pub_date.text if pub_date is not None else '',
                            'description': description.text if description is not None else ''
                        })
                
                return news_items
            else:
                print(f"Failed to fetch news for {symbol}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")
            return []
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text using both TextBlob and VADER
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment scores
        """
        if not text:
            return {
                'polarity': 0, 'subjectivity': 0, 'compound': 0, 
                'pos': 0, 'neu': 0, 'neg': 0
            }
        
        # TextBlob sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # VADER sentiment
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'compound': vader_scores['compound'],
            'pos': vader_scores['pos'],
            'neu': vader_scores['neu'],
            'neg': vader_scores['neg']
        }
    
    def get_sentiment_features(self, symbol):
        """
        Get aggregated sentiment features for a symbol
        
        Args:
            symbol (str): Financial symbol
            
        Returns:
            dict: Aggregated sentiment features
        """
        news_items = self.get_yahoo_finance_news(symbol)
        
        if not news_items:
            # Return neutral sentiment if no news found
            return {
                'avg_polarity': 0,
                'avg_subjectivity': 0,
                'avg_compound': 0,
                'avg_positive': 0,
                'avg_negative': 0,
                'news_count': 0
            }
        
        sentiments = []
        for item in news_items:
            # Combine title and description for sentiment analysis
            text = f"{item['title']} {item['description']}"
            sentiment = self.analyze_sentiment(text)
            sentiments.append(sentiment)
        
        # Calculate averages
        if sentiments:
            return {
                'avg_polarity': sum([s['polarity'] for s in sentiments]) / len(sentiments),
                'avg_subjectivity': sum([s['subjectivity'] for s in sentiments]) / len(sentiments),
                'avg_compound': sum([s['compound'] for s in sentiments]) / len(sentiments),
                'avg_positive': sum([s['pos'] for s in sentiments]) / len(sentiments),
                'avg_negative': sum([s['neg'] for s in sentiments]) / len(sentiments),
                'news_count': len(sentiments)
            }
        else:
            return {
                'avg_polarity': 0,
                'avg_subjectivity': 0,
                'avg_compound': 0,
                'avg_positive': 0,
                'avg_negative': 0,
                'news_count': 0
            }

class NewsFeatureEnhancer:
    def __init__(self, features_dir="../../data/features", output_dir="../../data/enhanced"):
        """Initialize news feature enhancer"""
        self.features_dir = features_dir
        self.output_dir = output_dir
        self.analyzer = NewsAnalyzer()
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def add_news_features_to_dataset(self, feature_file, output_file):
        """
        Add news sentiment features to existing feature dataset
        
        Args:
            feature_file (str): Path to features CSV file
            output_file (str): Path for enhanced output file
            
        Returns:
            dict: Sentiment features that were added
        """
        # Extract symbol from filename
        symbol = os.path.basename(feature_file).replace('_features.csv', '')
        
        # Load existing features
        df = pd.read_csv(feature_file)
        
        print(f"Fetching news sentiment for {symbol}...")
        sentiment_features = self.analyzer.get_sentiment_features(symbol)
        
        # Add sentiment features to all rows (assuming current sentiment applies to recent data)
        for key, value in sentiment_features.items():
            df[f'news_{key}'] = value
        
        # Save enhanced dataset
        df.to_csv(output_file, index=False)
        print(f"Saved enhanced dataset to {output_file}")
        
        return sentiment_features
    
    def enhance_all_datasets(self):
        """Enhance all feature datasets with news sentiment"""
        from glob import glob
        
        feature_files = glob(os.path.join(self.features_dir, '*_features.csv'))
        
        if not feature_files:
            print(f"⚠️ No feature files found in {self.features_dir}")
            return 0, 0
        
        print(f"📰 Enhancing {len(feature_files)} datasets with news sentiment...")
        print(f"📁 Input directory: {self.features_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        
        enhanced_files = []
        successful_enhancements = 0
        failed_enhancements = 0
        
        for file in feature_files:
            asset = os.path.basename(file).replace('_features.csv', '')
            enhanced_file = os.path.join(self.output_dir, f'{asset}_enhanced_features.csv')
            
            try:
                sentiment_features = self.add_news_features_to_dataset(file, enhanced_file)
                enhanced_files.append(enhanced_file)
                print(f"✅ Enhanced {asset} (News count: {sentiment_features['news_count']})")
                successful_enhancements += 1
                
                # Add small delay to avoid overwhelming news sources
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Failed to enhance {asset}: {e}")
                failed_enhancements += 1
        
        print(f"\n📰 News Enhancement Summary:")
        print(f"✅ Successful: {successful_enhancements}")
        print(f"❌ Failed: {failed_enhancements}")
        print(f"📁 Files saved in: {os.path.abspath(self.output_dir)}")
        
        return successful_enhancements, failed_enhancements

if __name__ == "__main__":
    # Test with a single symbol
    analyzer = NewsAnalyzer()
    sentiment = analyzer.get_sentiment_features('AAPL')
    print("AAPL News Sentiment:", sentiment)
    
    # Enhance all datasets
    enhancer = NewsFeatureEnhancer()
    enhancer.enhance_all_datasets()
