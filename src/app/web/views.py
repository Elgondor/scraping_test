import json
import uuid
from flask import Blueprint, jsonify, request, make_response, render_template
from  werkzeug.security import generate_password_hash, check_password_hash
from app.services.scraper_service import ScraperService
# from src.app.web.authentication import token_required
from .authentication import token_required
# from .authentication import token_required
# import sys
# sys.path.append(".")
from .extensions import db
from .models import *
from datetime import datetime, timedelta
import jwt 

import csv

from .email import EmailUtils

from sqlalchemy import func
from var_env import VAR_ENV

main = Blueprint('main', __name__)
scraper_service = ScraperService()

@main.route('/scrape', methods=['GET'])
@token_required
def scrape():
    try:
        scraper_service.run_spider()
        return jsonify({'message': 'Scraping started'})
    except Exception as e:
        mail = EmailUtils()
        error = json.dumps({"error": e.args})
        mail.send_email(
                to='shokkamax2@gmail.com',
                subject="Scrapper encountered an error",
                html_content=error
            )
        return jsonify({'error': e.args})


@main.route('/report_generation', methods=['GET'])
@token_required
def report_generation():
    try:
        scraped_data_list = scraper_service.get_scraped_data()
        keys = scraped_data_list[0].keys()
        path = VAR_ENV['FILE_PATH_DATA'] + 'csv/combined_scraped_data.csv'
        with open(path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(scraped_data_list)
        return jsonify({'message': 'Already converted into CSV', 
                        'file_path': path})
    except Exception as e:
        return jsonify({'error': e.args})


@main.route('/')
def index():
    scraped_data_list = scraper_service.get_scraped_data()
    return render_template('table.html', data_list = scraped_data_list)



@main.route('/load_bulk_scraped_data', methods=['GET'])
@token_required
def load_bulk_scraped_data():
    try: 
        public_register_data_bulk = []
        scraped_data_list = scraper_service.get_scraped_data()
        for data_item in scraped_data_list:
            public_register_data_bulk.append(PublicRegisterModel(registrant = data_item['registrant'], 
                                                                public_register_status = data_item['status'],
                                                                public_register_class = data_item['class'],
                                                                practice_location = data_item['practice_location']))
        
        db.session.bulk_save_objects(public_register_data_bulk)
        db.session.flush()
        db.session.commit()
        return jsonify({'message': 'Scraped data inserted in DB'})
    except Exception as e:
        return jsonify({'error': e.args})
    finally:
        db.session.close()

@main.route('/get_public_register_data/<int:page>', methods=['GET'])
@token_required
def get_public_register_data(page = 1):
    res = []
    per_page = 10
    try:
        total_pages = PublicRegisterModel.query.count()
        total_pages = total_pages / per_page
        public_register_list = PublicRegisterModel.query.paginate(page = page, per_page = per_page, error_out=False)
        for public_register_item in public_register_list:
            res.append(
                {
                    'id': public_register_item.id,
                    'registrant': public_register_item.registrant,
                    'public_register_status': public_register_item.public_register_status,
                    'public_register_class': public_register_item.public_register_class,
                    'practice_location': public_register_item.practice_location,
                }
            )
        return jsonify({'data': res,
                        'page': page,
                        'per_page': per_page,
                        'total_number_pages': total_pages})    
    except Exception as e:
        return jsonify({'error': e.args})


@main.route('/login', methods =['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    print(email)
    print(password)
    if email == '' or password == '':
        return make_response(
            'Could not verify', 401,
            {'authorization' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query.filter_by(email = email).first()
    print(user)
    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    if check_password_hash(user.password, password):
        print(VAR_ENV['JWT_SECRET_KEY'])
        token = jwt.encode({
            'uuid': user.uuid.urn,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, VAR_ENV['JWT_SECRET_KEY'])
        return make_response(json.dumps({'token' : token}), 201)
    
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )


@main.route('/signup', methods =['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
  
    # checking for existing user
    user = User.query.filter_by(email = email).first()
    if not user:
        user = User(
            uuid = str(uuid.uuid4()),
            email = email,
            password = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)