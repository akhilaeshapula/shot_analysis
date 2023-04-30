from project import db

class Defender(db.Model):
    __tablename__ = 'defenders'
    defender_id = db.Column(db.Integer, primary_key=True)
    closest_defender = db.Column(db.String(50))
    closest_defender_player_id = db.Column(db.Integer)
    close_def_dist = db.Column(db.Float)
    shot_id = db.Column(db.Integer, db.ForeignKey('shots.shot_id'))