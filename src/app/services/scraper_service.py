import subprocess
import os
import json

class ScraperService:
    def __init__(self):
        self.file_path = 'src/infra/data/scraped_data.json'
    
    def run_spider(self):
        subprocess.run(["python", "run_scraper.py"])

    def get_scraped_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            return None
