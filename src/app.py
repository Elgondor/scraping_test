from flask import Flask
# from app.web.models import *
from app.web.views import main

from app.web.extensions import db

# db = None

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baeldung:baeldung@localhost:5432/baeldung'
    
    print(app.config['SQLALCHEMY_DATABASE_URI'] )
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=3000, debug=True)
