from flask import Flask
from app.web.views import main
from var_env import VAR_ENV
from app.web.extensions import db
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# db = None

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    app.config['SQLALCHEMY_DATABASE_URI'] = VAR_ENV['SQLALCHEMY_DATABASE_URI']
    app.config['SECRET_KEY'] = VAR_ENV['JWT_SECRET_KEY']

    print(app.config['SQLALCHEMY_DATABASE_URI'] )
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=3000, debug=True)
