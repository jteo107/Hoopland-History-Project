import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dbhandler import Session, sznfile, playerEntry, upload_files, player
import pandas as pd

session = Session()

##specific season stat get method##
def get_player_szn_stats(player_name, season_year):
    yearfile = session.query(sznfile).filter_by(year=season_year).first()
    if not yearfile:
        print("Season not found")
        return None
    ##filters by player name and the season year file id##
    player = session.query(playerEntry).filter_by(name=player_name, szn_file_id = yearfile.id).first()
    if not player:
        print("Player not found")
        return None
    print(f"Player found: {player.name}, Team: {player.team}, Year: {season_year},Points: {player.pts}, Rebounds: {player.reb}, Assists: {player.ast}")
    return player

def compare_player_szn_stats(player1_name, player1_year, player2_name, player2_year):
    player1 = get_player_szn_stats(player1_name, player1_year)
    player2 = get_player_szn_stats(player2_name, player2_year)
    if not player1 or not player2:
        print("One or both players not found")
        return None
    print(f"{player1.name} ({player1_year} Season) vs {player2.name} ({player2_year} Season)")
    print(f"Points: {player1.pts} vs {player2.pts}")
    print(f"Rebounds: {player1.reb} vs {player2.reb}")
    print(f"Assists: {player1.ast} vs {player2.ast}")
    print(f"Steals: {player1.stl} vs {player2.stl}")
    print(f"Blocks: {player1.blk} vs {player2.blk}")
    print(f"PER: {player1.per} vs {player2.per}")
    print(f"TS%: {player1.ts} vs {player2.ts}")
    print(f"EFG%: {player1.efg} vs {player2.efg}")
    print(f"Games Played: {player1.gp} vs {player2.gp}")
    print(f"Games Started: {player1.gs} vs {player2.gs}")
    print(f"Minutes: {player1.min} vs {player2.min}")
    print(f"FGM: {player1.fgm} vs {player2.fgm}")
    print(f"FGA: {player1.fga} vs {player2.fga}")
    print(f"FG%: {player1.fg_pct} vs {player2.fg_pct}")
    print(f"3PM: {player1.threepm} vs {player2.threepm}")
    print(f"3PA: {player1.threepa} vs {player2.threepa}")
    print(f"3P%: {player1.threepct} vs {player2.threepct}")
    print(f"FTM: {player1.ftm} vs {player2.ftm}")
    print(f"FTA: {player1.fta} vs {player2.fta}")
    print(f"FT%: {player1.ftpct} vs {player2.ftpct}")
    print(f"Offensive Rebounds: {player1.oreb} vs {player2.oreb}")
    print(f"Personal Fouls: {player1.pf} vs {player2.pf}")
    print(f"Turnovers: {player1.tov} vs {player2.tov}")
    print(f"+/-: {player1.plus_minus} vs {player2.plus_minus}")
    print(f"Double-Doubles: {player1.dd} vs {player2.dd}")
    print(f"Triple-Doubles: {player1.td} vs {player2.td}")
    print(f"Player of the Game: {player1.potg} vs {player2.potg}")
    

    
