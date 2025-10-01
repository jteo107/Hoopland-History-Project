import os
from flask import Flask, request, jsonify, url_for, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import json
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config('SQLALCHEMY_DATABASE_URI', 'sqlite:///sznfiles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class playerEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

db.create_all()

class sznfile(db.model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(3), nullable=False)
    players = db.relationship('playerEntry', backref='sznfile', lazy=True)


@app_route('/')
def homepage:
    return render_template('index.html')


@app_route('/upload', methods=['POST'])
def upload_files():
    file = request.files['file']
    if not file:
        return "File upload error", 400
    file = file.filename
    newfile = filename[4:7]
    yearfile = sznfile(year=newfile)
    db.session.add(year_file)
    db.session.flush()
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        player_entry = playerEntry(
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
        year_file['players'].append(player_entry)
        db.session.add(player_entry)
    db.session.commit()
    return "Successful upload"

@app.route('/files', methods=['GET'])
def getFiles(szn_year,player_name):




if name == 'main':
    app.run(debug=True)






