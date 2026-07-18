from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import current_user, login_required
from app import db
from app.api import api
from app.game.ai import get_ai_choice
from app.game.routes import determine_winner, CHOICES
from app.models import Game, Score, User

ns_game = Namespace('game', description='Gameplay operations')
ns_leaderboard = Namespace('leaderboard', description='Leaderboard operations')

api.add_namespace(ns_game, path='/game')
api.add_namespace(ns_leaderboard, path='/leaderboard')

play_input = ns_game.model('PlayInput', {
    'choice': fields.String(required=True, description='rock, paper, or scissors', enum=CHOICES)
})

play_output = ns_game.model('PlayOutput', {
    'player_choice': fields.String,
    'computer_choice': fields.String,
    'result': fields.String,
    'predicted_move': fields.String,
    'method': fields.String
})

history_item = ns_game.model('HistoryItem', {
    'id': fields.Integer,
    'player_choice': fields.String,
    'computer_choice': fields.String,
    'result': fields.String,
    'played_at': fields.String
})

leaderboard_item = ns_leaderboard.model('LeaderboardItem', {
    'username': fields.String,
    'total_games': fields.Integer,
    'wins': fields.Integer,
    'win_percentage': fields.Float,
    'best_streak': fields.Integer
})


@ns_game.route('/play')
class Play(Resource):
    @ns_game.expect(play_input)
    @ns_game.marshal_with(play_output)
    @login_required
    def post(self):
        data = request.get_json()
        player_choice = data.get('choice')

        if player_choice not in CHOICES:
            ns_game.abort(400, 'Invalid choice. Must be rock, paper, or scissors.')

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
            score = Score(user_id=current_user.id, total_games=0, wins=0, losses=0,
                          draws=0, current_streak=0, best_streak=0)
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

        return {
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result,
            'predicted_move': predicted_move,
            'method': method
        }


@ns_game.route('/history')
class History(Resource):
    @ns_game.marshal_list_with(history_item)
    @login_required
    def get(self):
        games = Game.query.filter_by(user_id=current_user.id).order_by(Game.played_at.desc()).limit(50).all()
        return [{
            'id': g.id,
            'player_choice': g.player_choice,
            'computer_choice': g.computer_choice,
            'result': g.result,
            'played_at': g.played_at.isoformat()
        } for g in games]


@ns_leaderboard.route('')
class Leaderboard(Resource):
    @ns_leaderboard.marshal_list_with(leaderboard_item)
    @login_required
    def get(self):
        scores = Score.query.filter(Score.total_games > 0).order_by(Score.wins.desc()).all()
        return [{
            'username': s.user.username,
            'total_games': s.total_games,
            'wins': s.wins,
            'win_percentage': s.win_percentage,
            'best_streak': s.best_streak
        } for s in scores]
