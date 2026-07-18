from flask import request
from flask_socketio import emit, join_room
from flask_login import current_user
from app import socketio

waiting_players = []
active_rooms = {}

CHOICES = ['rock', 'paper', 'scissors']

def determine_round_winner(choice1, choice2):
    if choice1 == choice2:
        return 'draw'
    beats = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    if beats[choice1] == choice2:
        return 'player1'
    return 'player2'


@socketio.on('connect')
def handle_connect():
    print('Client connected:', request.sid)


@socketio.on('disconnect')
def handle_disconnect():
    global waiting_players
    sid = request.sid
    waiting_players = [p for p in waiting_players if p['sid'] != sid]

    for room_id, room in list(active_rooms.items()):
        if sid in room['players']:
            other_sids = [s for s in room['players'] if s != sid]
            if other_sids:
                emit('opponent_left', {}, room=other_sids[0])
            del active_rooms[room_id]


@socketio.on('find_match')
def handle_find_match():
    if not current_user.is_authenticated:
        emit('match_error', {'message': 'Not logged in'})
        return

    sid = request.sid

    if waiting_players:
        opponent = waiting_players.pop(0)
        room_id = f"room_{opponent['sid']}_{sid}"

        join_room(room_id, sid=opponent['sid'])
        join_room(room_id, sid=sid)

        active_rooms[room_id] = {
            'players': {
                opponent['sid']: {'user_id': opponent['user_id'], 'username': opponent['username'], 'choice': None},
                sid: {'user_id': current_user.id, 'username': current_user.username, 'choice': None}
            }
        }

        emit('match_found', {'room': room_id, 'opponent': current_user.username}, room=opponent['sid'])
        emit('match_found', {'room': room_id, 'opponent': opponent['username']}, room=sid)
    else:
        waiting_players.append({'sid': sid, 'user_id': current_user.id, 'username': current_user.username})
        emit('waiting_for_opponent')


@socketio.on('cancel_find')
def handle_cancel_find():
    global waiting_players
    waiting_players = [p for p in waiting_players if p['sid'] != request.sid]


@socketio.on('submit_choice')
def handle_submit_choice(data):
    room_id = data.get('room')
    choice = data.get('choice')
    sid = request.sid

    if room_id not in active_rooms or choice not in CHOICES:
        return

    room = active_rooms[room_id]
    if sid not in room['players']:
        return

    room['players'][sid]['choice'] = choice
    emit('opponent_ready', {}, room=room_id, include_self=False)

    choices_made = [p['choice'] for p in room['players'].values()]
    if all(choices_made):
        sids = list(room['players'].keys())
        p1_sid, p2_sid = sids[0], sids[1]
        p1 = room['players'][p1_sid]
        p2 = room['players'][p2_sid]

        outcome = determine_round_winner(p1['choice'], p2['choice'])
        if outcome == 'draw':
            p1_result, p2_result = 'draw', 'draw'
        elif outcome == 'player1':
            p1_result, p2_result = 'win', 'loss'
        else:
            p1_result, p2_result = 'loss', 'win'

        emit('round_result', {
            'your_choice': p1['choice'],
            'opponent_choice': p2['choice'],
            'result': p1_result,
            'opponent_username': p2['username']
        }, room=p1_sid)

        emit('round_result', {
            'your_choice': p2['choice'],
            'opponent_choice': p1['choice'],
            'result': p2_result,
            'opponent_username': p1['username']
        }, room=p2_sid)

        room['players'][p1_sid]['choice'] = None
        room['players'][p2_sid]['choice'] = None
