import pandas as pd
import numpy as np

def calculate_true_shooting(row):
    '''
    Helper function to calculate the true shooting percentage

    Arguments:
        row : pd.Series, the row of the dataframe
    Returns:
        ts : float, the true shooting percentage
    '''
    try:
        return row['PTS'] / (2 * (row['FGA'] + .44 * row['FTA']))
    except Exception as e:
        return 1

def calculate_groupby_ts(df):
    '''
    Helper function to calculate the true shooting percentage in groupby's

    Arguments: 
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
    Returns:
        ts : float, the true shooting percentage
    '''
    try:
        return df['PTS'].sum() / (2 * (df['FGA'].sum() + .44 * df['FTA'].sum()))
    except Exception as e:
        return 1