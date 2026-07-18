import random
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.game import game_bp
from app.game.ai import get_ai_choice
from app.models import Game, Score, User

CHOICES = ['rock', 'paper', 'scissors']

def determine_winner(player, computer):
    if player == computer:
        return 'draw'
    beats = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    if beats[player] == computer:
        return 'win'
    return 'loss'

@game_bp.route('/')
@login_required
def index():
    return render_template('game/index.html')

@game_bp.route('/play', methods=['POST'])
@login_required
def play():
    player_choice = request.form.get('choice')
    if player_choice not in CHOICES:
        return redirect(url_for('game.index'))

    computer_choice, predicted_move, method = get_ai_choice(current_user.id)
    result = determine_winner(player_choice, computer_choice)

    game = Game(
        user_id=current_user.id,
        player_choice=player_choice,
        computer_choice=computer_choice,
        result=result
    )
    db.session.add(game)

    score = Score.query.filter_by(user_id=current_user.id).first()
    if not score:
        score = Score(
            user_id=current_user.id,
            total_games=0,
            wins=0,
            losses=0,
            draws=0,
            current_streak=0,
            best_streak=0
        )
        db.session.add(score)

    score.total_games += 1
    if result == 'win':
        score.wins += 1
        score.current_streak += 1
        score.best_streak = max(score.best_streak, score.current_streak)
    elif result == 'loss':
        score.losses += 1
        score.current_streak = 0
    else:
        score.draws += 1
        score.current_streak = 0

    db.session.commit()

    return render_template('game/result.html',
                            player_choice=player_choice,
                            computer_choice=computer_choice,
                            result=result,
                            predicted_move=predicted_move,
                            method=method)

@game_bp.route('/history')
@login_required
def history():
    games = Game.query.filter_by(user_id=current_user.id).order_by(Game.played_at.desc()).all()
    return render_template('game/history.html', games=games)

@game_bp.route('/leaderboard')
@login_required
def leaderboard():
    scores = Score.query.filter(Score.total_games > 0).order_by(Score.wins.desc()).all()
    return render_template('game/leaderboard.html', scores=scores)

@game_bp.route('/dashboard')
@login_required
def dashboard():
    score = Score.query.filter_by(user_id=current_user.id).first()
    games = Game.query.filter_by(user_id=current_user.id).order_by(Game.played_at.asc()).all()

    move_counts = {'rock': 0, 'paper': 0, 'scissors': 0}
    for g in games:
        move_counts[g.player_choice] += 1

    running_win_rate = []
    wins_so_far = 0
    for i, g in enumerate(games, start=1):
        if g.result == 'win':
            wins_so_far += 1
        running_win_rate.append(round((wins_so_far / i) * 100, 1))

    return render_template('game/dashboard.html',
                            score=score,
                            move_counts=move_counts,
                            running_win_rate=running_win_rate,
                            game_numbers=list(range(1, len(games) + 1)))
