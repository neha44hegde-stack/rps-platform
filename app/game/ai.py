import random
from collections import Counter
from app.models import Game

CHOICES = ['rock', 'paper', 'scissors']
COUNTERS = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}

MIN_HISTORY_FOR_PREDICTION = 5
HISTORY_WINDOW = 30
SEQUENCE_LENGTH = 2

def predict_from_sequence(player_moves):
    if len(player_moves) <= SEQUENCE_LENGTH:
        return None, None

    current_sequence = tuple(player_moves[-SEQUENCE_LENGTH:])
    next_move_counts = Counter()

    for i in range(len(player_moves) - SEQUENCE_LENGTH):
        window = tuple(player_moves[i:i + SEQUENCE_LENGTH])
        if window == current_sequence:
            next_index = i + SEQUENCE_LENGTH
            if next_index < len(player_moves):
                next_move_counts[player_moves[next_index]] += 1

    if not next_move_counts:
        return None, None

    return next_move_counts.most_common(1)[0][0], 'sequence'

def predict_from_frequency(player_moves):
    move_counts = Counter(player_moves)
    return move_counts.most_common(1)[0][0], 'frequency'

def get_ai_choice(user_id):
    recent_games = (Game.query
                     .filter_by(user_id=user_id)
                     .order_by(Game.played_at.desc())
                     .limit(HISTORY_WINDOW)
                     .all())

    if len(recent_games) < MIN_HISTORY_FOR_PREDICTION:
        return random.choice(CHOICES), None, 'random (not enough history yet)'

    recent_games.reverse()
    player_moves = [g.player_choice for g in recent_games]

    predicted_move, method = predict_from_sequence(player_moves)

    if predicted_move is None:
        predicted_move, method = predict_from_frequency(player_moves)

    return COUNTERS[predicted_move], predicted_move, method
