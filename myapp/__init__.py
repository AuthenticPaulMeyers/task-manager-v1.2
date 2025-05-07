from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
import os

# initialise mail
mail = Mail()
# initialise the database
db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY']='KEEPA'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///task.db'
    # configure email server
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Set in .env or Render
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    db.init_app(app)
    CORS(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # register models 
    from . import models
    from .tasks import task
    from .auth import auth
    from .models import User


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(auth)
    app.register_blueprint(task)

    return app