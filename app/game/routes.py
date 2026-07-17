from app.game import game_bp

@game_bp.route('/')
def index():
    return "game placeholder"
