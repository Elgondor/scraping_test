import subprocess
import os
import json
from var_env import VAR_ENV

class ScraperService:
    def __init__(self):
        self.file_path = 'src/infra/data/combined_scraped_data.json'
    
    def run_spider(self):
        try:
            subprocess.run(["python", "run_scraper.py"])
        except Exception as e:
            return {'error': e}

    def get_scraped_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                # print(data)
            return data
        else:
            return None
