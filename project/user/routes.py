from flask import Blueprint,render_template,redirect, url_for,flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from project.models.User import User
from project import db
from flask_login import login_user, login_required, logout_user
from threading import Thread
from project.models.shots import Shot
from project.models.Players import Player
from project.models.data import Data
from project.models.Games import Game
from project.models.defenders import Defender
from project.models.shots_defenders import ShotDefender 
import plotly.graph_objs as go
import pandas as pd
from io import BytesIO
import base64

admin = Blueprint('admin', __name__)

@admin.route('/login')
def login():
    return render_template('login.html')

@admin.route('/signup')
def signup():
    return render_template('signup.html')

@admin.route('/signup', methods=['GET','POST'])
def signup_post():
    if "post":
        email = request.form.get('email')
        print(email)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
       
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if password!=confirm_password:
            flash('Password does not match')
            return redirect(url_for('admin.signup'))
        
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('admin.signup'))
 
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, first_name=firstname,last_name=lastname, password=generate_password_hash(password, method='sha256'))



        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin.login'))
    else:
        return render_template('signup.html')

    
@admin.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    # role = request.form.get('roles')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('admin.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    return redirect(url_for('admin.profile'))  



@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/profile', methods=['GET'])
def profile():
    players_records = Player.query.all()
    print(players_records[0].player_name)
    return render_template('profile.html', packages = players_records) 

@admin.route('/player/<string:token>')
@login_required
def player(token):
    player_name_token = token
    print(player_name_token)
    # str_cmd = "select * from  where player_id="+player_id+";"
    str_cmd = "select * from data as d where d.player_name = '"+player_name_token+"' ORDER BY d.shot_id ASC;"
    # str_cmd = "select * from data where player_id = '"+player_name+"' ;"
    data = db.engine.execute(str_cmd).fetchall()
    # data = Data.query.filter_by(player_name = player_name_token).first()
    # print(data)
    if data == None:
        return redirect(url_for('admin.profile')) 
    else:
        return render_template('player.html', shot_record = data)

@admin.route('/shotEdit/<string:token>',methods = ['GET'])
@login_required
def shotEdit(token):
    str_cmd= " select * from data where shot_id="+token+";"
    records_shot = db.engine.execute(str_cmd).fetchall()
    print(records_shot[0])
    return render_template('editForm.html',records_shot=records_shot[0])

@admin.route('/shotEdit',methods=['POST'])
@login_required
def shotEditSave():
    records_shots = request.form.get('token')
    str_cmd= " select * from data where shot_id="+records_shots+";"
    data = db.engine.execute(str_cmd).fetchall()
    data = data[0]
    update_details = Data.query.filter_by(shot_id = data.shot_id ).first()
    shot_number = request.form.get('shot_number')
    period = request.form.get('period')
    shot_dist = request.form.get('shot_dist')
    shot_res = request.form.get('shot_res')
    pts_type = request.form.get('pts_type')
    print(data)
    pts = request.form.get('pts')
    if shot_number:
        update_details.shot_number = shot_number
    if period:
        update_details.period = period
    if shot_dist:
        update_details.shot_dist = shot_dist
    if shot_res:
        update_details.shot_result = shot_res
    if pts_type:
        update_details.pts_type = pts_type
    if pts:
        update_details.pts = pts
    db.session.commit()
    
    update_details2 = Shot.query.filter_by(shot_id = data.shot_id ).first()
    shot_number = request.form.get('shot_number')
    period = request.form.get('period')
    shot_dist = request.form.get('shot_dist')
    shot_res = request.form.get('shot_res')
    pts_type = request.form.get('pts_type')
    print(data)
    pts = request.form.get('pts')
    if shot_number:
        update_details2.shot_number = shot_number
    if period:
        update_details2.period = period
    if shot_dist:
        update_details2.shot_dist = shot_dist
    if shot_res:
        update_details2.shot_result = shot_res
    if pts_type:
        update_details2.pts_type = pts_type
    if pts:
        update_details2.pts = pts
    

    # print("Updated values:")
    # print("Shot number:", update_details.shot_number)
    # print("Period:", update_details.period)
    # print("Shot dist:", update_details.shot_dist)
    # print("Shot result:", update_details.shot_result)
    # print("PTS type:", update_details.pts_type)
    # print("PTS:", update_details.pts)
    db.session.commit()
    return redirect(url_for('admin.player',token= data.player_name))  


@admin.route('/shotDelete/<string:token>',methods = ['GET'])
@login_required
def shotDelete(token):
    str_cmd= " select * from data where shot_id="+token+";"
    data = db.engine.execute(str_cmd).fetchall()
    data = data[0]
    player_name = data.player_name
    str_cmd2= "delete from data as d where d.shot_id="+token+";"
    db.engine.execute(str_cmd2)
    db.session.commit()
    return redirect(url_for('admin.player',token= player_name))

@admin.route('/createPlayer')
@login_required
def createPlayer():
    return render_template('createPlayer.html')

@admin.route('/createPlayer', methods=['POST'])
@login_required
def createPlayerPost():
    player_name = request.form.get('player_name')
    shot_number = request.form.get('shot_number')
    period = request.form.get('period')
    shot_dist = request.form.get('shot_dist')
    shot_res = request.form.get('shot_res')
    pts_type = request.form.get('pts_type')
    pts = request.form.get('pts')
    game_id = request.form.get('game_id')
    closest_defender = request.form.get('closest_defender')
    data = Data(player_name=player_name, shot_number=shot_number, period=period, shot_dist=shot_dist,shot_result=shot_res, pts_type=pts_type, pts=pts, closest_defender=closest_defender)
    db.session.add(data)
    db.session.commit()
    player_query = Player.query.filter_by(player_name = data.player_name ).first()
    if player_query == None:
        player_data = Player(player_name=player_name)
        db.session.add(player_data)
        db.session.commit()
    shot_record = Shot(player_name=player_name, shot_number=shot_number, period=period, shot_dist=shot_dist,shot_result=shot_res, pts_type=pts_type, pts=pts)
    # print(shot_record.player_name, "###############shot_record.player_name")
    db.session.add(shot_record)
    db.session.commit()
    game_record= Game(game_id = game_id)
    db.session.add(game_record)
    db.session.commit()
    closest_defender_record = Defender(closest_defender=closest_defender)
    db.session.add(closest_defender_record)
    db.session.commit()
    return redirect(url_for('admin.player', token = player_name))

@admin.route('/visualize', methods=['GET','POST'])
@login_required
def visualize():
   players = Player.query.all()
   print(players[0].player_name)
   if request.method == 'POST':
        player_name = request.form['player_name']
        player_data = Data.query.filter_by(player_name=player_name).all()
        df = pd.DataFrame([(p.shot_result) for p in player_data], columns=['shot_result'])
        success_rate = df['shot_result'].value_counts(normalize=True) * 100
        made = success_rate.made
        missed = success_rate.missed
        print(type(made))
        print(type(missed))
        return render_template('visualisation.html', made= made, missed =missed, players= players)
   return render_template('visualisation.html', players= players)


    
    









