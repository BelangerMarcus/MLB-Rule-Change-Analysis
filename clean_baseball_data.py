import pandas as pd
import datetime               
import numpy as np
import warnings

df_all_dirty = pd.read_csv(r"C:\Users\mbela\Downloads\.....")
# display(df_all_dirty.head())
df_slider_dirty = pd.read_csv(r"C:\Users\mbela\Downloads\.....")
# display(df_slider_dirty.head())
df_4seam_dirty = pd.read_csv(r"C:\Users\mbela\Downloads\Projects\.....")
# display(df_4seam_dirty.head())

################################################################################################################################################################################

### CLEAN (LEAGUE-WIDE) and (TEAM) PITCH DATA

def clean_pitch(df, pitch_type=None, team=None):
    stats = ['pitches','total_pitches','pitch_percent','ba','iso','babip','slg','woba','hits','abs','spin_rate','velocity','sv_ratio','whiffs','swings','takes','WHIFF','swstr']
    league_headers = ['game_date','period','pitches','total_pitches','pitch_percent','ba','iso','babip','slg','woba','hits','abs','spin_rate','velocity','sv_ratio','whiffs','swings','takes','WHIFF','swstr']
    team_headers = ['game_date','period','team_name','pitches','total_pitches','pitch_percent','ba','iso','babip','slg','woba','hits','abs','spin_rate','velocity','sv_ratio','whiffs','swings','takes','WHIFF','swstr']
    
    warnings.filterwarnings("ignore")                                                 # generally bad practice, but in this case--> not a problem
    df['game_date'] = pd.to_datetime(df['game_date'])                                 # convert game_date to datetime 
    df = df.sort_values('game_date')                                                  # sort by game_date
    df.rename(columns={'spin/velo':'sv_ratio'}, inplace=True)                         # change column name
    df['sv_ratio'] = pd.to_numeric(df['sv_ratio'], errors='coerce')                   # convert sv_ratio to float64
    df['WHIFF'] = pd.to_numeric(df['WHIFF'], errors='coerce')                         # convert WHIFF to float64
    df_clean=df.dropna()                                                              # drop Nan 
    if team == None:
        df_clean=df_clean.groupby('game_date',as_index=False)[stats].mean()           # create daily, league-wide stats. If team != None then we will create a dataframe with team performances --> allows us to compare teams
    conditions = [                                                                    # adds column with 'periods', makes it easier to do hypothesis tests later
        (df_clean['game_date'] <= '2021-06-03'),                                    
        (df_clean['game_date'] > '2021-06-03') & (df_clean['game_date'] <= '2021-06-20'), 
        (df_clean['game_date'] > '2021-06-20')]
    values = ['before', 'transition', 'after']
    df_clean['period'] = np.select(conditions, values)
    if team == None:
        df_clean=df_clean.reindex(columns=league_headers)                             # creates column headers without 'team_name'
    else:
        df_clean=df_clean.reindex(columns=team_headers)                               # creates column headers with 'team_name'
    if pitch_type != None:                                                            # changes 'pitches' to more informative title if we are looking at a specific type of pitch
        df_clean.rename(columns={'pitches': pitch_type}, inplace=True)
    df_clean.set_index('game_date',inplace=True)                                      # sets game_date as index
    df_clean['period'] = df_clean['period'].astype('category')                        # changes period to category, makes it easier to work with later
    pd.set_option('display.max_rows', None)                                           
    pd.set_option('display.max_columns', None)
#     df_clean.info()
    return df_clean
    
################################################################################################################################################################################

### CREATE .csv's FOR ANALYSIS PAGE ### 

### (LEAGUE-WIDE STATS)
df_league_all = clean_pitch(df_all_dirty)
df_league_slider = clean_pitch(df_slider_dirty, 'slider')
df_league_4seam = clean_pitch(df_4seam_dirty, '4seamFB')

## test:
# display(df_league_all)
# display(df_league_slider)
# display(df_league_4seam)

## transfer to other page
df_league_all.to_csv('league_all.csv')
df_league_slider.to_csv('league_slider.csv')
df_league_4seam.to_csv('league_4seam.csv')


### (TEAM STATS)
df_team_all = clean_pitch(df_all_dirty, team = 1)
df_team_slider = clean_pitch(df_slider_dirty, 'slider', 1)
df_team_4seam = clean_pitch(df_4seam_dirty, '4seamFB', 1)

## test:
# display(df_team_all)
# display(df_team_slider)
# display(df_team_4seam)

## transfer to other page
df_team_all.to_csv('team_all.csv')
df_team_slider.to_csv('team_slider.csv')
df_team_4seam.to_csv('team_4seam.csv')
