'''Initializes the Flask application and the database'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os
load_dotenv()
db = SQLAlchemy()
# Constants for databases
DB_NAME = "test"
secret_key = "secret"
login_manager = LoginManager()

def create_app()->Flask:
    '''Initialize Flask application and return app object'''
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SECRET_KEY"] = secret_key
    # initialize the database
    from .models import User, Message
    db.init_app(app)
    create_database(app)
    # initialize the login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from .views import views
    app.register_blueprint(views)
    from .auth import auth
    app.register_blueprint(auth)
    return app

def create_database(app: Flask):
    '''Create database if it does not exist'''
    db_path = os.path.join('instance', 'test.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            # Verify tables exist
        print("Database created")
    else:
        print("Database exists")