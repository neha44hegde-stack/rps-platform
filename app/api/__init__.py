from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)

api = Api(
    api_bp,
    version='1.0',
    title='RPS Platform API',
    description='REST API for the AI-Powered Rock Paper Scissors Platform',
    doc='/docs'
)

from app.api import routes
