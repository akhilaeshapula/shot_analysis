from project import db

class Player(db.Model):
    __tablename__ = 'players'
    player_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50))
    shots = db.relationship('Shot', backref='player', lazy=True)
