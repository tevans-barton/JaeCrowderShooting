import numpy as np
import pandas as pd
import logging
import re
from helper_functions import calculate_true_shooting
logging.basicConfig(filename='../logger.log', format='%(asctime)s %(levelname)s:%(name)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

INACTIVE_DESIGNATIONS = ['Did Not Play', 'Inactive', 'Injured Reserve', 'Did Not Dress', 'Player Suspended']

def get_player_gamelog(filename):
    '''
    Reads in a csv file and returns a cleaned dataframe
    
    Arguments:
        filename : str, The path to the csv file

    Returns:
        df_cleaned : pd.DataFrame, the cleaned dataframe
    '''
    df = pd.read_csv(filename)
    df_cleaned = __clean_gamelog(df)
    return df_cleaned

def __clean_gamelog(gamelog_df):
    '''
    Helper function to clean the gamelog dataframe

    Arguments:
        gamelog_df : pd.DataFrame, the gamelog dataframe
    
    Returns:
        player_gamelog_df : pd.DataFrame, the cleaned gamelog dataframe
    '''
    player_gamelog_df = gamelog_df.copy()
    #Get rid of unused rank column
    player_gamelog_df = player_gamelog_df.drop('Rk', axis = 1)
    #Rename incorrectly labeled date column
    player_gamelog_df = player_gamelog_df.rename(columns=lambda x: re.sub('[0-9]{4} Playoffs','Date',x))
    #Rename and reformat home/away column
    player_gamelog_df = player_gamelog_df.rename(columns=lambda x: re.sub('Unnamed: 5','Home/Away',x))
    player_gamelog_df['Home/Away'] = player_gamelog_df['Home/Away'].replace('@', 'Away').fillna('Home')
    #Rename and reformat result column
    player_gamelog_df = player_gamelog_df.rename(columns=lambda x: re.sub('Unnamed: 8','Result',x))
    #Drop rows where the header is repeated
    player_gamelog_df = player_gamelog_df[player_gamelog_df['Date'] != 'Date'].reset_index(drop = True)
    #Remove games where player was inactive using inactive designations list
    player_gamelog_df = player_gamelog_df.replace(INACTIVE_DESIGNATIONS, np.nan)
    #Drop rows where the player did not play any minutes
    player_gamelog_df = player_gamelog_df[player_gamelog_df['MP'].notnull()].reset_index(drop = True)


    #Split the result column into a win/loss column and a point differential column
    result_column = player_gamelog_df['Result']
    player_gamelog_df['Result'] = result_column.str.extract(r'(W|L)')
    player_gamelog_df['Point Differential'] = result_column.str.extract(r'\(([\-\+]\d+)\)')
    #Convert numeric columns to numeric type
    player_gamelog_df = player_gamelog_df.apply(lambda x : pd.to_numeric(x, errors='ignore'))
    #Make Date column a datetime object
    player_gamelog_df['Date'] = pd.to_datetime(player_gamelog_df['Date']).dt.date
    #Create a year column
    player_gamelog_df['Year'] = pd.to_datetime(player_gamelog_df['Date']).dt.year
    
    #Make the series column categorical and ordered
    SERIES_ORDER = ['EC1', 'WC1', 'ECS', 'WCS', 'ECF', 'WCF', 'FIN']
    player_gamelog_df['Series'] = pd.Categorical(player_gamelog_df['Series'], categories=SERIES_ORDER, ordered=True)
    
    player_gamelog_df['TS'] = player_gamelog_df.apply(lambda x : calculate_true_shooting(x), axis = 1)

    #Reorder columns
    FIRST_HALF_COLUMNS = ['Date', 'Year', 'G', 'Series', 'Tm', 'Home/Away', 'Opp', 'G#', 'Result', 'Point Differential']
    player_gamelog_df = player_gamelog_df[FIRST_HALF_COLUMNS + [x for x in player_gamelog_df.columns if x not in FIRST_HALF_COLUMNS]]
    return player_gamelog_df