import requests
import pandas as pd 
from datetime import datetime
import logging
from typing import Optional, Dict
import time 
import yaml
import os
from dotenv import load_env 

load_dotenv()

class AlphaVantageExtractor:
    def __init__(self, config_path: str = 'config/config.yaml')
    with open(config_path, 'r') as file: 
        self.config = yaml.safe_load(file)
    
    self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    self.base_url = self.config['alpha_vantage']['base_url']
    self.rate_limit = self.config['alpha_vantage']['rate_limit']
    self.logger = logging.getLogger(__name__)
    self.last_call_time = 0 

    def _rate_limit_handler(self): 
        # Handles API rate Limiting 
        current_time = time.time()
        time_passed = current_time - self.last_call_time
        if time_passed < (60 / self.rate_limit):
            time.sleep((60 / self.rate_limit) - time_passed)
        self.last_call_time = time.time()