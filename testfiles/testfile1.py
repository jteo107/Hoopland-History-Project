import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from v1 import Session, sznfile, playerEntry
import pandas as pd

session = Session()

def upload_files(file):
    if not file:
        return "File upload error", 400
    name = os.path.basename(file)
    newfile = name[4:7]
    year_file = sznfile(year=newfile)
    session.add(year_file)
    session.flush()
    df = pd.read_csv(file)

    df = df.replace('-', 0)
    df = df.fillna(0)

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



if __name__ == "__main__":
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2018_season_stats.csv')
    player = session.query(playerEntry).filter_by(name = 'A.J. Vaquero').first()
    print(f"Player found: {player.name}, Team: {player.team}, Points: {player.pts}")
