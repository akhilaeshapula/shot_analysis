from project import db

class Data(db.Model):
    __tablename__ = 'data'
    shot_id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(50))
    shot_number = db.Column(db.Integer)
    period = db.Column(db.Integer)
    shot_dist = db.Column(db.Float)
    shot_result = db.Column(db.String(10))
    pts_type = db.Column(db.Integer)
    pts = db.Column(db.Integer)
    closest_defender = db.Column(db.String(50))