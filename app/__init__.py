from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, cors_allowed_origins='*')

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    from app.auth import auth_bp
    from app.game import game_bp
    from app.api import api_bp
    from app.multiplayer import mp_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(mp_bp, url_prefix='/multiplayer')

    from app.multiplayer import socket_events

    return app
