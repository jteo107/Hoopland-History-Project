import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dbhandler import Session, sznfile, playerEntry, upload_files
from optionhandler import get_player_szn_stats, compare_player_szn_stats, get_full_szn_stats, season_plot_design
import pandas as pd

session = Session()


if __name__ == "__main__":
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2006_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2007_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2008_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2009_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2010_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2011_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2012_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2013_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2014_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2015_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2016_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2017_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2018_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2019_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2020_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2021_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2022_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2023_season_stats.csv')
    upload_files('/Users/Johann/hoophistoryproject/datafiles/HLA_2024_season_stats.csv')

    ##crit = {'Position': ('PG','GF'), 'Team': None, 'Rookie': False}
    ##season_plot_design(get_full_szn_stats('2020'),crit,'kmeans',0,0,20)
    compare_player_szn_stats('Niko Metrovic',2018,'Taog Gib',2009)

    
    
