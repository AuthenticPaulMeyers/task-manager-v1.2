from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


# initialise the database
db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY']='KEEPA'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///task.db'

    db.init_app(app)
    CORS(app)
    csrf.init_app(app)
    login_manager.init_app(app)

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