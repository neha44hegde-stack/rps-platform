from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    from app.auth import auth_bp
    from app.game import game_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
