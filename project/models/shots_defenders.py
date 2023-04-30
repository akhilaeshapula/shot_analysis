from project import db

class ShotDefender(db.Model):
    __tablename__ = 'shots_defenders'
    shot_id = db.Column(db.Integer, db.ForeignKey('shots.shot_id'), primary_key=True)
    defender_id = db.Column(db.Integer, db.ForeignKey('defenders.defender_id'), primary_key=True)
    closest_defender_player_id = db.Column(db.Integer)