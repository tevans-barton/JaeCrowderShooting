import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import analysis
plt.style.use('ggplot')

#Equation I've been tinkering with
#plt.hist(((crowder_df['TS'] - crowder_df['TS'].mean()) * (crowder_df['FGA'] + crowder_df['FTA'] / 2) + (crowder_df['TS'].mean() * (crowder_df['FGA'].mean() + crowder_df['FTA'].mean() / 2))), bins = np.arange(-1, 12, 1))

#If the visualizations folder doesn't exist, create it
if not os.path.exists('../visualizations'):
    os.makedirs('../visualizations')


#Average TS for SF in 2022 Playoffs according to statmuse
SF_AVG_TS = .567
#Average TS for PF in 2022 Playoffs according to statmuse
PF_AVG_TS = .585

#Buck's Logos Official Colors
BUCKS_GREEN = '#00471B'
BUCKS_BLUE = '#0077c0'
BUCKS_CREAM = '#EEE1C6'

TEAM_COLORS_FOR_BAR_PLOTS = {
    'DAL' : '#002B5E',
    'BOS' : '#007A33',
    'UTA' : '#F9A01B',
    'MIA' : '#98002E',
    'PHO' : '#E56020',
    'MIL' : BUCKS_GREEN,
}


def plot_ts_by_year(df, player_name, download = False):
    '''
    Plots the true shooting percentage from year to year

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False
    
    Returns:
        None
    '''
    plt.figure(figsize=(12,8))
    #Plot the player's TS
    df_to_plot = analysis.get_ts_by_year(df)
    teams_in_order = list(df.drop_duplicates(subset = ['Year', 'Tm']).sort_values('Year')['Tm'])
    colors = [TEAM_COLORS_FOR_BAR_PLOTS[x] if x in TEAM_COLORS_FOR_BAR_PLOTS.keys() else 'Gray' for x in teams_in_order]
    plt.bar(df_to_plot.index, df_to_plot['TS'], color=colors, label=player_name)
    plt.xlabel('Year', fontsize = 15)
    plt.xticks(df_to_plot.index.unique())
    plt.ylabel('True Shooting Percentage', fontsize= 15)
    plt.title('{p} Playoff True Shooting by Year'.format(p = player_name), fontsize = 20)
    if download:
        plt.savefig('../visualizations/{p}_ts_by_year.png'.format(p = player_name.replace(' ', '')))
    plt.show()

def plot_ts_vs_time(df, player_name, download = False):
    '''
    Plots the true shooting percentage for a player over the 
    course of their playoff career, comparing it to the average for the position
    
    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False
    
    Returns:
        None
    '''
    plt.figure(figsize=(12,8))
    #Plot the player's TS
    plt.plot(df['TS'], color=BUCKS_GREEN, label=player_name)
    #Plot the average TS for the position
    plt.plot([SF_AVG_TS] * len(df), linestyle='dashed', color=BUCKS_BLUE, label='Small Forward 2022 Playoff Average')
    plt.xlabel('Game', fontsize = 15)
    plt.ylabel('True Shooting Percentage', fontsize= 15)
    plt.title('{p} Playoff True Shooting'.format(p = player_name), fontsize = 20)
    plt.legend(fontsize = 14)
    if download:
        plt.savefig('../visualizations/{p}_ts_vs_time.png'.format(p = player_name.replace(' ', '')))
    plt.show()

def plot_ts_histogram(df, player_name, download = False):
    '''
    Plots the distribution of true shooting percentage for a player in their playoff career

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False
    
    Returns:
        None
    '''
    plt.figure(figsize=(12,8))
    #Plot the player's TS distribution
    plt.hist(df['TS'], color=BUCKS_GREEN, bins = np.arange(0, 1.3, .1), label='_nolegend_')
    #Plot the average TS for the position with a red dot
    plt.plot(SF_AVG_TS, 0.05, marker='o', markersize=15, color=BUCKS_BLUE, markeredgecolor=BUCKS_CREAM, label='Small Forward 2022 Playoff Average')
    plt.legend(fontsize = 14)
    plt.xlabel('True Shooting Percentage', fontsize = 15)
    plt.ylabel('Count', fontsize= 15)
    plt.title('{p} Playoff True Shooting'.format(p = player_name), fontsize = 20)
    if download:
        plt.savefig('../visualizations/{p}_ts_histogram.png'.format(p = player_name.replace(' ', '')))
    plt.show()

def plot_ts_by_game(df, player_name, download = False):
    '''
    Plots the true shooting percentage for a player depending on game in the series

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False

    Returns:
        None
    '''
    plt.figure(figsize=(12,8))
    #Plot the player's TS
    df_to_plot = analysis.get_ts_by_game(df)
    plt.bar(df_to_plot.index, df_to_plot['TS'], color=BUCKS_GREEN, label=player_name)
    plt.xlabel('Game in Series', fontsize = 15)
    plt.xticks(df_to_plot.index.unique())
    plt.ylabel('True Shooting Percentage', fontsize= 15)
    plt.title('{p} Playoff True Shooting by Game in Series'.format(p = player_name), fontsize = 20)
    if download:
        plt.savefig('../visualizations/{p}_ts_by_game.png'.format(p = player_name.replace(' ', '')))
    plt.show()

def plot_year_series_heatmap(df, player_name, download = False):
    '''
    Plots a heatmap of the true shooting percentage for a player in each series in each year

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False

    Returns:
        None
    '''
    df_to_plot = analysis.get_ts_by_year_and_round(df)
    plt.figure(figsize=(12,8))
    #Plot the heatmap
    map = sns.diverging_palette(10, 133, as_cmap=True)
    map.set_bad(color = '#36454F')
    #map = sns.light_palette(BUCKS_GREEN)
    ax = sns.heatmap(df_to_plot, cmap=map, annot=True, fmt='.3f', cbar=False, center=SF_AVG_TS)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xlabel('Series', fontsize = 15, loc='center')
    plt.ylabel('Year', fontsize= 15)
    plt.yticks(rotation=0)
    plt.title('{p} Playoff True Shooting by Year and Round'.format(p = player_name), fontsize = 20)
    if download:
        plt.savefig('../visualizations/{p}_ts_by_year_round_heatmap.png'.format(p = player_name.replace(' ', '')))
    plt.show()

def plot_game_series_heatmap(df, player_name, download = False):
    '''
    Plots a heatmap of the true shooting percentage for a player in each game of each playoff series

    Arguments:
        df : pd.DataFrame, the dataframe containing the gamelogs. Expects dataframe of the form returned by etl.get_gamelogs()
        player_name : str, the name of the player
        download : bool, whether or not to save the plot to the visualizations folder, defaults to False
    
    Returns:
        None
    '''
    df_to_plot = analysis.get_ts_by_series_and_game(df)
    plt.figure(figsize=(12,8))
    #Plot the heatmap
    map = sns.diverging_palette(10, 133, as_cmap=True)
    #map = sns.light_palette(BUCKS_GREEN)
    ax = sns.heatmap(df_to_plot, cmap=map, annot=True, fmt='.3f', cbar=False, center=SF_AVG_TS)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xlabel('Game', fontsize = 15, loc='center')
    plt.ylabel('Series', fontsize= 15)
    plt.yticks(rotation=0)
    plt.title('{p} Playoff True Shooting by Series and Game'.format(p = player_name), fontsize = 20)
    if download:
        plt.savefig('../visualizations/{p}_ts_by_game_series_heatmap.png'.format(p = player_name.replace(' ', '')))
    plt.show()
