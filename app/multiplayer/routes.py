from flask import render_template
from flask_login import login_required, current_user

from app.multiplayer import mp_bp

@mp_bp.route('/')
@login_required
def lobby():
    return render_template('multiplayer/lobby.html')
