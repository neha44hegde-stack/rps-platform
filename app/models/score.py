from app import db

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_games = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref=db.backref('score', uselist=False))

    @property
    def win_percentage(self):
        if self.total_games == 0:
            return 0.0
        return round((self.wins / self.total_games) * 100, 2)

    def __repr__(self):
        return f'<Score user={self.user_id} wins={self.wins}>'
