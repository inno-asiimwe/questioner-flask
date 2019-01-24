from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config



db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    from models import user

    db.init_app(app)

    # register blueprints
    from resources.users import auth_api
    
    app.register_blueprint(auth_api, url_prefix='/api/v1/users')

    return app
