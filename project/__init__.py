from flask import Flask, request,url_for,redirect,session,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
import csv

# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'root'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/test5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test5_nf8w_user:tfTTxGDSpa9Dstks7XpGmjlOskBL2xIx@dpg-ch7dnk82qv26p1cebqr0-a/test5_nf8w'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    from project.models.User import User



    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    from project.common.main import main
    app.register_blueprint(main)
    # blueprint for auth routes in our app
    from project.user.routes import admin
    app.register_blueprint(admin)

    from project.models.User import User
    from project.models.Games import Game
    from project.models.shots import Shot
    from project.models.Players import Player
    from project.models.shots_defenders import ShotDefender
    from project.models.defenders import Defender
    from project.models.data import Data
    with app.app_context():
        db.create_all()
        db.session.commit()



#     @app.before_first_request
#     def do_something_only_once():
#         with open('project/shots_filtered_1.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             next(csv_reader) # Skip first row
#             inserted_defenders = set()
#             inserted_players = set()
#             inserted_games = set()
#             for row in csv_reader:
#                 # insert into 'defenders' table
#                 closest_defender_player_id = row[15]
#                 closest_defender = row[14]
#                 if closest_defender not in inserted_defenders:
#                     defender = Defender(closest_defender=closest_defender)
#                     db.session.add(defender)
#                     db.session.flush()  # to get the defender_id generated by the database
#                     inserted_defenders.add(closest_defender)
#                 defender = Defender.query.filter_by(closest_defender=closest_defender).first()
#                 defender_id = defender.defender_id

#                 # insert into 'players' table
#                 player_id = row[20]
#                 player_name = row[19]
#                 if player_id not in inserted_players:
#                     player = Player(player_id=player_id, player_name=player_name)
#                     db.session.add(player)
#                     inserted_players.add(player_id)
#                 player = Player.query.filter_by(player_id=player_id).first()
#                 player_id = player.player_id

#                 # insert into 'games' table
#                 game_id = row[0]
#                 if game_id not in inserted_games:
#                     matchup = row[1]
#                     location = row[2]
#                     w = row[3]
#                     final_margin = row[4]
#                     game = Game(game_id=game_id, matchup=matchup, location=location, w=w, final_margin=final_margin)
#                     db.session.add(game)
#                     inserted_games.add(game_id)

#                 # insert into 'shots' table
#                 shot_number = row[5]
#                 period = row[6]
#                 game_clock = row[7]
#                 shot_clock = row[8]
#                 dribbles = row[9]
#                 touch_time = row[10]
#                 shot_dist = row[11]
#                 pts_type = row[12]
#                 shot_result = row[13]
#                 close_def_dist = row[16]
#                 fgm = row[17]
#                 pts = row[18]
#                 game = Game.query.filter_by(game_id=game_id).first()
#                 shot = Shot(shot_number=shot_number, period=period, game_clock=game_clock,
#                             shot_clock=shot_clock, dribbles=dribbles, touch_time=touch_time, shot_dist=shot_dist,
#                             pts_type=pts_type, shot_result=shot_result, close_def_dist=close_def_dist, fgm=fgm, pts=pts,
#                             player_id=player_id, game_id=game_id)
#                 db.session.add(shot)
#                 db.session.commit()

#                 #insert into 'data' table
#                 player_name = row[19]
#                 shot_number = row[5]
#                 period = row[6]
#                 shot_dist = row[11]
#                 shot_result = row[13]
#                 pts_type = row[12]
#                 pts = row[18]
#                 closest_defender = row[14]
#                 data = Data(player_name= player_name, shot_number=shot_number,period=period,shot_dist=shot_dist, shot_result=shot_result, pts_type=pts_type,pts=pts,closest_defender=closest_defender)
#                 db.session.add(data)
#                 db.session.commit()

#                 # insert into 'shot_defenders' table
#                 shot_defender = ShotDefender.query.filter_by(shot_id=shot.shot_id, defender_id=defender_id).first()
#                 if not shot_defender:
#                     shot_defender = ShotDefender(shot_id=shot.shot_id, defender_id=defender_id, closest_defender_player_id=closest_defender_player_id)
#                     db.session.add(shot_defender)
#                     db.session.commit()



    return app
