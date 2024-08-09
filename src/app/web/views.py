from flask import Blueprint, jsonify
from app.services.scraper_service import ScraperService

# import sys
# sys.path.append(".")
from .extensions import db
from .models import User

main = Blueprint('main', __name__)
scraper_service = ScraperService()

@main.route('/scrape', methods=['GET'])
def scrape():
    scraper_service.run_spider()
    return jsonify({'message': 'Scraping started'})

@main.route('/testing_get', methods=['GET'])
def testing_get():
    user = User.query.all()
    print(user)
    # scraper_service.run_spider()
    return jsonify({'message': 'Nice test'})