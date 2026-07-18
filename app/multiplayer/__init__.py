from flask import Blueprint

mp_bp = Blueprint('multiplayer', __name__)

from app.multiplayer import routes
