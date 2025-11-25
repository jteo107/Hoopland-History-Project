from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "sqlite:///hooplandhistory.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

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


class sznfile(Base):
    __tablename__ = 'szn_files'
    id = Column(Integer, primary_key=True)
    year = Column(String(3), nullable=False)
    players = relationship('playerEntry', backref='sznfile', lazy=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    session = Session()
    new_season = sznfile(year="2023")
    session.add(new_season)
    session.commit()
    print(f"New Season added with id: {new_season.id}")
    years = session.query(sznfile).all()
    print(f"Total year files in database: {len(years)}")
    session.close()

