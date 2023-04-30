from project import db

class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    matchup = db.Column(db.String(100))
    location = db.Column(db.String(100))
    w = db.Column(db.String(1))
    final_margin = db.Column(db.Integer)
    shots = db.relationship('Shot', backref='game', lazy=True)