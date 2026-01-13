import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


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

    return (player1, player2)

def get_full_szn_stats(szn_year):
    yearfile = session.query(sznfile).filter_by(year=szn_year).first()
    if not yearfile:
        print("Season not found")
        return None
    players = session.query(playerEntry).filter_by(szn_file_id = yearfile.id).all()
    if not players:
        print("No players found for this season")
        return None
    data = []
    for p in players:
        data.append({
            'Name': p.name,
            'Team': p.team,
            'Position': p.position,
            'Year': p.year,
            'GP': p.gp,
            'GS': p.gs,
            'MIN': p.min,
            'PTS': p.pts,
            'FGM': p.fgm,
            'FGA': p.fga,
            'FG%': p.fg_pct,
            '3PM': p.threepm,
            '3PA': p.threepa,
            '3P%': p.threepct,
            'FTM': p.ftm,
            'FTA': p.fta,
            'FT%': p.ftpct,
            'REB': p.reb,
            'OREB': p.oreb,
            'AST': p.ast,
            'STL': p.stl,
            'BLK': p.blk,
            'PF': p.pf,
            'TO': p.tov,
            '+/-': p.plus_minus,
            'DD': p.dd,
            'TD': p.td,
            'POTG': p.potg,
            'PER': p.per,
            'TS%': p.ts,
            'EFG%': p.efg
        })
    df = pd.DataFrame(data)
    print(df)
    return df

def season_plot_design(dataframe,additional_criteria,plot_type, x, y, num_clusters):
    positions = []
    teams = []
    rookie_only = False
    if(additional_criteria['Position'] != None):
        for pos in additional_criteria['Position']:
            if pos not in positions:
                positions.append(pos)
    if(additional_criteria['Team'] != None):
        for team in additional_criteria['Team']:
            if team not in teams:
                teams.append(team)
    if(additional_criteria['Rookie'] == True):
        rookie_only = True
    if(plot_type == 'kmeans'):
        kmeans_season_plot(dataframe, positions,rookie_only,num_clusters)
    else:
        pca_plot(dataframe, positions, teams, rookie_only, x, y)

def kmeans_season_plot(dataframe, positions, rookie_only,num_clusters):
    df = dataframe.copy()
    df = df[(df['GP'] > 0) & (df['MIN'] > 0)]
    if(len(positions) > 0):
        df = df[df['Position'].isin(positions)]
    if(rookie_only):
        df = df[df['Year'] == 'R']
    if(df.empty):
        return None
    key_stats = [
        'GP',
        'GS',
        'MIN',
        'PTS',
        'FGM',
        'FGA',
        '3PM',
        '3PA',
        'FTM',
        'FTA',
        'REB',
        'OREB',
        'AST',
        'STL',
        'BLK',
        'PF',
        'TO',
        '+/-',
        'PER',
        'TS%',
        'EFG%'
    ]
    numeric_df = df[key_stats]
    numeric_df = numeric_df.loc[:, numeric_df.std() > 0]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    k = num_clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    df['Cluster'] = clusters
    for i in sorted(df['Cluster'].unique()):
        print(f"Cluster {i}:")
        members = df[df['Cluster'] == i]['Name'].tolist()
        print(members)
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)
    
    df['PCA1'] = pca_data[:, 0]
    df['PCA2'] = pca_data[:, 1]

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Cluster', palette='Set2')
    
    for i, row in df.iterrows():
        plt.text(row['PCA1']+0.02, row['PCA2']+0.02, row['Name'], fontsize=9)
    
    plt.title('K-Means Clustering of Players')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend(title='Cluster')
    plt.show()



    
    

def pca_plot(dataframe, positions, teams, rookie_only, x, y):
    pass






    
