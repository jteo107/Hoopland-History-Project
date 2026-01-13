import os
from flask import Flask, request, jsonify, url_for, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import json
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI', 'sqlite:///hooplandhistory.db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class playerEntry(db.Model):
    __tablename__ = 'playerEntries'
    id = db.Column(db.Integer, primary_key=True)
    szn_file_id = db.Column(db.Integer, db.ForeignKey('szn_files.id'), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(3), nullable=False)
    year = db.Column(db.String(3), nullable=False)
    gp = db.Column(db.Integer, nullable=False)
    gs = db.Column(db.Integer, nullable=False)
    min = db.Column(db.Float, nullable=False)
    pts = db.Column(db.Float, nullable=False)
    fgm = db.Column(db.Float, nullable=False)
    fga = db.Column(db.Float, nullable=False)
    fg_pct = db.Column(db.Float, nullable=False)
    threepm = db.Column(db.Float, nullable=False)
    threepa = db.Column(db.Float, nullable=False)
    threepct = db.Column(db.Float, nullable=False)
    ftm = db.Column(db.Float, nullable=False)
    fta = db.Column(db.Float, nullable=False)
    ftpct = db.Column(db.Float, nullable=False)
    reb = db.Column(db.Float, nullable=False)
    oreb = db.Column(db.Float, nullable=False)
    ast = db.Column(db.Float, nullable=False)
    stl = db.Column(db.Float, nullable=False)
    blk = db.Column(db.Float, nullable=False)
    pf = db.Column(db.Float, nullable=False)
    tov = db.Column(db.Float, nullable=False)
    plus_minus = db.Column(db.Float, nullable=False)
    dd = db.Column(db.Integer, nullable=False)
    td = db.Column(db.Integer, nullable=False)
    potg = db.Column(db.Integer, nullable=False)
    per = db.Column(db.Float, nullable=False)
    ts = db.Column(db.Float, nullable=False)
    plus_minus = db.Column(db.Float, nullable=False)
    efg = db.Column(db.Float, nullable=False)


class sznfile(db.Model):
    __tablename__ = 'szn_files'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(3), nullable=False)
    players = db.relationship('playerEntry', backref='sznfile', lazy=True)




@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    file = request.files['file']
    if not file:
        return "File upload error", 400
    name = file.filename
    newfile = name[4:7]
    yearfile = sznfile(year=newfile)
    db.session.add(year_file)
    db.session.flush()
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        player_entry = playerEntry(
            szn_file_id=year_file.id,
            name=row['name'],
            team=row['team'],
            position=row['position'],
            year=row['year'],
            gp=row['gp'],
            gs=row['gs'],
            min=row['min'],
            pts=row['pts'],
            fgm=row['fgm'],
            fga=row['fga'],
            fg_pct=row['fg_pct'],
            threepm=row['threepm'],
            threepa=row['threepa'],
            threepct=row['threepct'],
            ftm=row['ftm'],
            fta=row['fta'],
            ftpct=row['ftpct'],
            reb=row['reb'],
            oreb=row['oreb'],
            ast=row['ast'],
            stl=row['stl'],
            blk=row['blk'],
            pf=row['pf'],
            tov=row['tov'],
            plus_minus=row['plus_minus'],
            dd=row['dd'],
            td=row['td'],
            potg=row['potg'],
            per=row['per'],
            ts=row['ts'],
            efg=row['efg']
        )
        db.session.add(player_entry)
    db.session.commit()
    return "Successful upload"

def main_menu():
    choice = request.form.get('choice')
    match choice:
        case "Individual Season":
            option = get_individual_season()
            individual_season_menu()
        case "Individual Player":
            option = get_individual_player()
            individual_player_menu()
        case "Team Season":
            option = get_team_season()
            team_season_menu()
        case "Get Players List":
            option = get_players_list()
            mult_players_menu()
        case "Get All Players":
            option = get_all_players()
            all_players_menu()
        case _:
            option = "Invalid choice"
    return option

def get_individual_season():
    year = request.form.get('year')
    results = sznfile.query.filter_by(year=year).all()
    return results
    
def get_individual_player():
    name = request.form.get('name')
    name = name.title()
    player = sznfile.query.filter_by(name=name).all()
    return player

def get_team_season():
    name = request.form.get('team')
    year = request.form.get('year')
    name = name.upper()
    team = sznfile.query.filter_by(team=name, year=year).all()
    return team

def get_players_list():
    rawnames = request.form.get('players')
    players = []
    for name in rawnames.split(','):
        name = name.title().strip()
        players.append(name)
    player_entries = sznfile.query.filter(sznfile.name.in_(players)).all()
    return player_entries
    
def get_all_players():
    player_list = sznfile.quey.all()
    return player_list

def individual_player_menu():
    choice = request.form.get('choice')
    match choice:
        case "Get Career Stats":
            option = get_career_stats()
        case "Get Season Stats":
            year = request.form.get('year')
            option = get_player_season_stats(year)
        case "Get Career Advanced Stats" : 
            option = get_career_advanced_stats()
        case _:
            option = "Invalid choice"
    return option

def get_career_stats():
    name = request.form.get('name')
    name = name.title()
    player = sznfile.query.filter_by(name=name).all()
    return player
    
def get_player_season_stats(year):
    name = request.form.get('name')
    name = name.title()
    results = sznfile.query.filter_by(name=name, year=year).all()
    return results






if __name__ == 'main':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






