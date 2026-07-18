from app.game.ai import get_ai_choice, CHOICES

def test_ai_returns_valid_choice_with_no_history(app, db):
    with app.app_context():
        choice, predicted, method = get_ai_choice(user_id=9999)
        assert choice in CHOICES
        assert method.startswith('random')
