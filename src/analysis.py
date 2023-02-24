import numpy as np
import pandas as pd
import logging
from helper_functions import calculate_groupby_ts
logging.basicConfig(filename='../logger.log', format='%(asctime)s %(levelname)s:%(name)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

#Equation I've been tinkering with
#plt.hist(((crowder_df['TS'] - crowder_df['TS'].mean()) * (crowder_df['FGA'] + crowder_df['FTA'] / 2) + (crowder_df['TS'].mean() * (crowder_df['FGA'].mean() + crowder_df['FTA'].mean() / 2))), bins = np.arange(-1, 12, 1))

#TODO: CHECK ALL GROUP BYS

#Average TS for SF in 2022 Playoffs according to statmuse
SF_AVG_TS = .567
#Average TS for PF in 2022 Playoffs according to statmuse
PF_AVG_TS = .585

TS_NEEDED_COLUMNS = ['PTS', 'FGA', 'FTA']

ROUND_MAP = {
    'EC1' : 'FIRST ROUND',
    'WC1' : 'FIRST ROUND',
    'ECS' : 'CONFERENCE SEMIFINALS',
    'WCS' : 'CONFERENCE SEMIFINALS',
    'ECF' : 'CONFERENCE FINALS',
    'WCF' : 'CONFERENCE FINALS',
    'FIN' : 'FINALS',
}

def get_ts_by_year(df):
    '''
    Calculates the true shooting percentage for each year in the playoffs

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    
    Returns:
        ts_by_year : pd.DataFrame, the dataframe containing the true shooting percentage for the playoffs in each year
    '''
    ts_by_year = df[['Year'] + TS_NEEDED_COLUMNS].groupby('Year').apply(lambda x: calculate_groupby_ts(x))
    ts_by_year = pd.DataFrame(ts_by_year)
    ts_by_year.columns = ['TS']
    return ts_by_year

def get_ts_by_series(df):
    '''
    Calculates the true shooting percentage for each series in the playoffs

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()

    Returns:
        ts_by_series : pd.DataFrame, the dataframe containing the true shooting percentage for each playoff series
    '''
    #TODO: IS THIS RIGHT?
    ts_by_series = df[['Year', 'Opp', 'Series'] + TS_NEEDED_COLUMNS].groupby(['Year', 'Series', 'Opp']).apply(lambda x: calculate_groupby_ts(x))
    ts_by_series = pd.DataFrame(ts_by_series)
    ts_by_series.columns = ['TS']
    return ts_by_series

def get_ts_by_game(df):
    '''
    Calculate the true shooting percentage for each game (1 - 7) in the playoffs

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    
    Returns:
        ts_by_game : pd.DataFrame, the dataframe containing the true shooting percentage for each playoff game
    '''
    ts_by_game = df[['G#'] + TS_NEEDED_COLUMNS].groupby('G#').apply(lambda x: calculate_groupby_ts(x))
    ts_by_game = pd.DataFrame(ts_by_game)
    ts_by_game.columns = ['TS']
    return ts_by_game
    

def get_ts_by_series_and_game(df):
    '''
    Calculates the true shooting percentage mean for each game in each series in the playoffs

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()

    Returns:
        ts_by_series_and_game : pd.DataFrame, the dataframe containing the true shooting percentage for each playoff game by series
    '''
    #THIS WAY RIGHT PROBABLY
    ts_by_series_and_game = df[['Series', 'G#'] + TS_NEEDED_COLUMNS].groupby(['Series', 'G#']).apply(lambda x: calculate_groupby_ts(x)).unstack() 
    return ts_by_series_and_game

def get_ts_by_year_and_round(df):
    '''
    Calculates the true shooting percentage mean for each series in each year in the playoffs

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()

    Returns:
        ts_by_series_and_year : pd.DataFrame, the dataframe containing the true shooting percentage for each playoff series and year
    '''
    df_copy = df.copy()
    df_copy['Round'] = df_copy['Series'].map(ROUND_MAP)
    #Make the series column categorical and ordered
    ROUND_ORDER = ['FIRST ROUND', 'CONFERENCE SEMIFINALS', 'CONFERENCE FINALS', 'FINALS']
    df_copy['Round'] = pd.Categorical(df_copy['Round'], categories=ROUND_ORDER, ordered=True)
    ts_by_series_and_year = df_copy[['Round', 'Year'] + TS_NEEDED_COLUMNS].groupby(['Year', 'Round']).apply(lambda x: calculate_groupby_ts(x)).unstack() 
    return ts_by_series_and_year

def get_ts_by_home_away(df):
    '''
    Calculates the true shooting percentage for home vs away games

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    
    Returns:
        ts_by_home_away : pd.DataFrame, the dataframe containing the true shooting percentage for home vs away games
    '''
    ts_by_home_away = df[['Home/Away'] + TS_NEEDED_COLUMNS].groupby('Home/Away').apply(lambda x: calculate_groupby_ts(x))
    ts_by_home_away = pd.DataFrame(ts_by_home_away)
    ts_by_home_away.columns = ['TS']
    return ts_by_home_away

def get_streaks(df):
    '''
    Gets information about the streaks a player has shooting (above/below average TS for position)

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()

    Returns:
        streaks_df : pd.DataFrame, the dataframe containing the streaks
    '''
    return df


def get_hot_streaks(df):
    '''
    Gets information about the hot streaks a player has shooting (above average TS for position)
    
    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    
    Returns:
        hot_streaks_df : pd.DataFrame, the dataframe containing the hot streaks
    '''
    hot_streaks = []
    curr_streak_length = 0
    curr_year = df['Year'].min()
    start_date = ''
    end_date = ''
    for index, row in df.iterrows():
        if row['TS'] >= SF_AVG_TS:
            if curr_streak_length == 0:
                start_date = row['Date']
                start_game = row['Series'] + ' Game ' + str(row['G#'])
            if row['Year'] == curr_year:
                curr_streak_length += 1
                end_date = row['Date']
                end_game = row['Series'] + ' Game ' + str(row['G#'])
            else:
                if curr_streak_length > 0:
                    hot_streaks.append({'Streak Length (Games)' : curr_streak_length, 'Start Date' : start_date, 'End Date' : end_date, 'First Game' : start_game, 'Last Game' : end_game})
                    curr_streak_length = 1
                    curr_year = row['Year']
        else:
            if curr_streak_length > 0:
                hot_streaks.append({'Streak Length (Games)' : curr_streak_length, 'Start Date' : start_date, 'End Date' : end_date, 'First Game' : start_game, 'Last Game' : end_game})
                curr_streak_length = 0
            curr_year = row['Year']
    hot_streaks_df = pd.DataFrame(hot_streaks)
    return hot_streaks_df

def get_cold_streaks(df):
    '''
    Gets information about the cold streaks a player has shooting (above average TS for position)
    
    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    
    Returns:
        cold_streaks_df : pd.DataFrame, the dataframe containing the cold streaks
    '''
    cold_streaks = []
    curr_streak_length = 0
    curr_year = df['Year'].min()
    start_date = ''
    end_date = ''
    for index, row in df.iterrows():
        if row['TS'] < SF_AVG_TS:
            if curr_streak_length == 0:
                start_date = row['Date']
                start_game = row['Series'] + ' Game ' + str(row['G#'])
            if row['Year'] == curr_year:
                curr_streak_length += 1
                end_date = row['Date']
                end_game = row['Series'] + ' Game ' + str(row['G#'])
            else:
                if curr_streak_length > 0:
                    cold_streaks.append({'Streak Length (Games)' : curr_streak_length, 'Start Date' : start_date, 'End Date' : end_date, 'First Game' : start_game, 'Last Game' : end_game})
                    curr_streak_length = 1
                    curr_year = row['Year']
        else:
            if curr_streak_length > 0:
                cold_streaks.append({'Streak Length (Games)' : curr_streak_length, 'Start Date' : start_date, 'End Date' : end_date, 'First Game' : start_game, 'Last Game' : end_game})
                curr_streak_length = 0
            curr_year = row['Year']
    cold_streaks_df = pd.DataFrame(cold_streaks)
    return cold_streaks_df