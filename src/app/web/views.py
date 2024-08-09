from flask import Blueprint, jsonify
from app.services.scraper_service import ScraperService

main = Blueprint('main', __name__)
scraper_service = ScraperService()

@main.route('/scrape', methods=['GET'])
def scrape():
    scraper_service.run_spider()
    return jsonify({'message': 'Scraping started'})
