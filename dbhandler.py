from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
import pandas as pd

DATABASE_URL = "sqlite:///hooplandhistory.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

##class declaration for SQL player entry table##
class playerEntry(Base):
    __tablename__ = 'playerEntries'
    id = Column(Integer, primary_key=True)
    szn_file_id = Column(Integer, ForeignKey('szn_files.id'), nullable=False)

    name = Column(String(150), nullable=False)
    team = Column(String(100), nullable=False)
    position = Column(String(3), nullable=False)
    year = Column(String(3), nullable=False)
    gp = Column(Integer, nullable=False)
    gs = Column(Integer, nullable=False)
    min = Column(Float, nullable=False)
    pts = Column(Float, nullable=False)
    fgm = Column(Float, nullable=False)
    fga = Column(Float, nullable=False)
    fg_pct = Column(Float, nullable=False)
    threepm = Column(Float, nullable=False)
    threepa = Column(Float, nullable=False)
    threepct = Column(Float, nullable=False)
    ftm = Column(Float, nullable=False)
    fta = Column(Float, nullable=False)
    ftpct = Column(Float, nullable=False)
    reb = Column(Float, nullable=False)
    oreb = Column(Float, nullable=False)
    ast = Column(Float, nullable=False)
    stl = Column(Float, nullable=False)
    blk = Column(Float, nullable=False)
    pf = Column(Float, nullable=False)
    tov = Column(Float, nullable=False)
    plus_minus = Column(Float, nullable=False)
    dd = Column(Integer, nullable=False)
    td = Column(Integer, nullable=False)
    potg = Column(Integer, nullable=False)
    per = Column(Float, nullable=False)
    ts = Column(Float, nullable=False)
    efg = Column(Float, nullable=False)

##class declaration for the season file table## 
class sznfile(Base):
    __tablename__ = 'szn_files'
    id = Column(Integer, primary_key=True)
    year = Column(String(3), nullable=False)
    ##relationship to playerEntry table##
    players = relationship('playerEntry', backref='sznfile', lazy=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

##upload file method##
def upload_files(file):
    if not file:
        return "File upload error", 400
    session = Session()
    ##temporary file name handling before real upload method gets figured out
    name = os.path.basename(file)
    ##slices out the year from the file name##
    newfile = name[4:8]
    year_file = sznfile(year=newfile)
    session.add(year_file)
    session.flush()
    df = pd.read_csv(file)

    df = df.replace('-', 0)
    df = df.fillna(0)
    ##uses pandas to read the csv file and iterate through each row to add to the database##
    for _, row in df.iterrows():
        player_entry = playerEntry(
            szn_file_id=year_file.id,
            name=row['Player Name'],
            team=row['Team'],
            position=row['Position'],
            year=row['Year'],
            gp=row['GP'],
            gs=row['GP'],
            min=row['MIN'],
            pts=row['PTS'],
            fgm=row['FGM'],
            fga=row['FGA'],
            fg_pct=row['FG%'],
            threepm=row['3PM'],
            threepa=row['3PA'],
            threepct=row['3P%'],
            ftm=row['FTM'],
            fta=row['FTA'],
            ftpct=row['FT%'],
            reb=row['REB'],
            oreb=row['OREB'],
            ast=row['AST'],
            stl=row['STL'],
            blk=row['BLK'],
            pf=row['PF'],
            tov=row['TO'],
            plus_minus=row['+/-'],
            dd=row['DD'],
            td=row['TD'],
            potg=row['POTG'],
            per=row['PER'],
            ts=row['TS%'],
            efg=row['EFG%']
        )
        session.add(player_entry)
    session.commit()
    return "Successful upload"

##player object class for further analysis##
class player:
    def __init__(self,name, team, position, year, gp, gs, min, pts, fgm, fga, fg_pct, threepm, threepa, threepct, ftm, fta, ftpct, reb, oreb, ast, stl, blk, pf, tov, plus_minus, dd, td, potg, per, ts, efg):
        self.name = name
        self.team = team
        self.position = position
        self.year = year
        self.gp = gp
        self.gs = gs
        self.min = min
        self.pts = pts
        self.fgm = fgm
        self.fga = fga
        self.fg_pct = fg_pct
        self.threepm = threepm
        self.threepa = threepa
        self.threepct = threepct
        self.ftm = ftm
        self.fta = fta
        self.ftpct = ftpct
        self.reb = reb
        self.oreb = oreb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.pf = pf
        self.tov = tov
        self.plus_minus = plus_minus
        self.dd = dd
        self.td = td
        self.potg = potg
        self.per = per
        self.ts = ts
        self.efg = efg
    def get_stats(self):
        return vars(self)


    



if __name__ == "__main__":
    session = Session()
    new_season = sznfile(year="2023")
    session.add(new_season)
    session.commit()
    print(f"New Season added with id: {new_season.id}")
    years = session.query(sznfile).all()
    print(f"Total year files in database: {len(years)}")
    session.close()

