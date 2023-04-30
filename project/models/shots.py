from project import db

class Shot(db.Model):
    __tablename__ = 'shots'
    shot_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    shot_number = db.Column(db.Integer)
    period = db.Column(db.Integer)
    game_clock = db.Column(db.String(8))
    shot_clock = db.Column(db.Float)
    dribbles = db.Column(db.Integer)
    touch_time = db.Column(db.Float)
    shot_dist = db.Column(db.Float)
    pts_type = db.Column(db.Integer)
    shot_result = db.Column(db.String(7))
    close_def_dist = db.Column(db.Float)
    fgm = db.Column(db.Integer)
    pts = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
    player_name = db.Column(db.String(50))
    defenders = db.relationship('Defender', backref='shot', lazy=True)


    
    