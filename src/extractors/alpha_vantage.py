import requests
import pandas as pd
from datetime import datetime
import logging
from typing import Optional, Dict
import time
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageExtractor:
    def __init__(self, config_path: str = 'config/config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = self.config['alpha_vantage']['base_url']
        self.rate_limit = self.config['alpha_vantage']['rate_limit']
        self.logger = logging.getLogger(__name__)
        self.last_call_time = 0

    def _rate_limit_handler(self):
        """Handles API rate limiting"""
        current_time = time.time()
        time_passed = current_time - self.last_call_time
        if time_passed < (60 / self.rate_limit):
            time.sleep((60 / self.rate_limit) - time_passed)
        self.last_call_time = time.time()

    def fetch_daily_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Fetches daily stock data for a given symbol
        """
        try:
            self._rate_limit_handler()
            
            params: Dict = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": "full"
            }
            
            self.logger.info(f"Fetching data for symbol: {symbol}")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if "Time Series (Daily)" not in data:
                self.logger.error(f"No data returned for symbol {symbol}")
                return None
                
            # Convert JSON to DataFrame
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
            
            # Clean column names
            df.columns = [col.split('. ')[1].lower() for col in df.columns]
            
            # Convert index to datetime
            df.index = pd.to_datetime(df.index)
            
            # Reset index to make date a column
            df.reset_index(inplace=True)
            df.rename(columns={"index": "date"}, inplace=True)
            
            # Add symbol column
            df['symbol'] = symbol
            
            # Save raw data
            self._save_raw_data(df, symbol)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def _save_raw_data(self, df: pd.DataFrame, symbol: str):
        """Saves raw data to CSV"""
        filename = f"data/raw/{symbol}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        self.logger.info(f"Raw data saved to {filename}")

    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """
        Fetches company overview for a given symbol
        """
        try:
            self._rate_limit_handler()
            
            params = {
                "function": "OVERVIEW",
                "symbol": symbol,
                "apikey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error fetching company info for {symbol}: {str(e)}")
            return None