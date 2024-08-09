import os
import sys
import json
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.infra.adapters.public_register_spider import PublicRegisterSpider

def combine_json_files(base_dir='src/infra/data'):
    combined_data = []
    for filename in os.listdir(base_dir):
        if filename.startswith('scraped_data_') and filename.endswith('.json'):
            with open(os.path.join(base_dir, filename), 'r') as file:
                data = json.load(file)
                combined_data.extend(data)
    combined_filename = os.path.join(base_dir, 'combined_scraped_data.json')
    with open(combined_filename, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(PublicRegisterSpider)
    process.start()

    # Combine JSON files after scraping
    combine_json_files()

if __name__ == "__main__":
    run()
