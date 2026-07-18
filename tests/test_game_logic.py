from app.game.routes import determine_winner

def test_rock_beats_scissors():
    assert determine_winner('rock', 'scissors') == 'win'

def test_scissors_beats_paper():
    assert determine_winner('scissors', 'paper') == 'win'

def test_paper_beats_rock():
    assert determine_winner('paper', 'rock') == 'win'

def test_rock_loses_to_paper():
    assert determine_winner('rock', 'paper') == 'loss'

def test_draw_when_same_choice():
    assert determine_winner('rock', 'rock') == 'draw'
    assert determine_winner('paper', 'paper') == 'draw'
    assert determine_winner('scissors', 'scissors') == 'draw'
