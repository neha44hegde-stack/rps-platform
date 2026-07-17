from app.auth import auth_bp

@auth_bp.route('/login')
def login():
    return "login placeholder"
