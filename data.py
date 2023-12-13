import os
import time
import pandas as pd
import numpy as np
from tqdm import tqdm



def get_espn_salary():
    os.makedirs('data/espn_salaries', exist_ok=True)
    for year in tqdm(range(2000, 2023)):
        cur_s = pd.DataFrame()
        for page in tqdm(range(1, 16)):
            cur_page_s = None
            for trial in range(3):
                if cur_page_s is not None:
                    continue
                try:
                    time.sleep(5)
                    cur_page_s = pd.read_html(
                        f'https://www.espn.com/nba/salaries/_/year/{year+1}/page/{page}'
                        )[0]
                    cur_s = pd.concat([cur_s, cur_page_s])
                except:
                    pass
                if trial == 2:
                    print(f'Failed to get {year+1} page {page}')
        cur_s.to_csv(f'data/espn_salaries/salary_{year}.csv', index=False)


def get_hoopshype_salary():
    os.makedirs('data/hoopshype_salaries', exist_ok=True)
    # for year in tqdm(range(2000, 2023)):
    for year in tqdm(range(2014, 2015)):
        for trials in range(3):
            try:
                time.sleep(3)
                cur_s = pd.read_html(
                    f"https://hoopshype.com/salaries/players/{year}-{year+1}/"
                    )[0]
            except:
                pass
            if trials == 2 and cur_s.shape[0]<100:
                print(f'Failed to get {year}')
        cur_s.to_csv(f'data/hoopshype_salaries/salary_{year}.csv', index=False)

def get_player_statistics():
    os.makedirs('data/player_statistics', exist_ok=True)

    for year in tqdm(range(2000, 2023)):

        for trials in range(3):
            try:
                time.sleep(3)
                cur_s = pd.read_html(
                    f"https://www.basketball-reference.com/leagues/NBA_{year+1}_totals.html"
                    )[0]
            except:
                pass
            if trials == 2 and cur_s.shape[0]<100:
                print(f'Failed to get {year}')
        cur_s.to_csv(f'data/player_statistics/player_{year}.csv', index=False)


def process_year(year):

    # load data
    data = pd.read_csv(f'data/player_statistics/player_{year}.csv')

    # get rid of unnecessary rows
    data = data[(data['Player'] != 'Player') & (data['Pos'] != 'Pos')]

    # set season
    
    data['Season'] = year
    data['Trend'] = year - 2000

    first_column = data.pop('Season')
    data.insert(0, 'Season', first_column) 

    # convert data types to float
    convert_dict = {col: float for col in ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
        '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
        'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        }
    data = data.astype(
        convert_dict
        
    )

    # subtract points made from 3 from total points
    data['PTS'] = data['PTS'] - 3* data['3P']

    # drop duplicated rows for players who played for multiple teams, keep the last team they played for
    data = data.sort_values(by='G', ascending=False)
    data = data.drop_duplicates(subset='Player')
    data.reset_index(drop=True, inplace=True)



    game_played_thredhold = data.groupby('Tm').max()['G'].to_dict()

    # drop players who played less than 1/4 of the player who played the most games for that team
    for team in game_played_thredhold:
        data = data[~((data['Tm'] == team) & (data['G'] < game_played_thredhold[team]/4))]


    return data


def process_espn_salary(sea):
    sal = pd.read_csv(f'data/espn_salaries/salary_{sea}.csv', skiprows=[0] )
    sal = sal[(sal['NAME']!= 'NAME') & (sal['TEAM'] != 'TEAM')]
    sal['salary'] = sal['SALARY'].str.replace('$', '').str.replace(',', '').astype(float) / 100_000
    sal['name'] = sal['NAME'].str.split(',').str[0]
    sal['position'] = sal['NAME'].str.split(',').str[1]
    sal['season'] = sea
    sal = sal[['name', 'position', 'salary', 'season']]
    return sal

def process_hoopshype_salary(sea):
    cur_year = pd.read_csv(f'data/hoopshype_salaries/salary_{sea}.csv')
    cur_year['name'] = cur_year['Player']
    cur_year['season'] = sea
    if sea == 2023:
        cur_year['salary'] = cur_year[f'{sea}/{str(sea+1)[-2:]}'].str.strip("$").str.replace(',', '').astype(float) / 1_000
    else:
        cur_year['salary'] = cur_year[f'{sea}/{str(sea+1)[-2:]}(*)'].str.strip("$").str.replace(',', '').astype(float) / 1_000
    cur_year['position'] = ''
    cur_year = cur_year[['name', 'position', 'salary', 'season']]
    return cur_year
    
def merge_and_encoding(players, salaries):
    df = players.merge(salaries, left_on=['Player', 'Season'], right_on=['name', 'season'])
    seasons = pd.get_dummies(df['Season'], drop_first=True, prefix="season")
    teams = pd.get_dummies(df['Tm'], drop_first=True, prefix="team")
    positions = pd.get_dummies(df['Pos'], drop_first=False, prefix="position")
    df = pd.concat([df, seasons, teams, positions], axis=1)
    return df


def feature_engineering(df):

    df = df.sort_values(by=['Player', 'Season'])

    # Group by 'Player' and then shift the 'salary' column by 1 to get the previous year's salary
    df['last_year_salary'] = df.groupby('Player')['salary'].shift(1)

    df['next_year_salary'] = df.groupby('Player')['salary'].shift(-1)


    # Replace the NaN values for players who did not play last year
    df['last_year_salary'] = df['last_year_salary'].replace({np.nan: None}).astype(float)
    df['next_year_salary'] = df['next_year_salary'].replace({np.nan: None}).astype(float)

    df['3PPerMP'] = df['3P'] / df['MP']
    df['PTSPerMP'] = df['PTS'] / df['MP']
    df['TRBPerMP'] = df['TRB'] / df['MP']
    df['ASTPerMP'] = df['AST'] / df['MP']
    df['PFPerMP'] = df['PF'] / df['MP']
    df['STLPerMP'] = df['STL'] / df['MP']


    df = df[~((df['Player']=='Damion James') & (df['Season']==2013))]


    # interaction terms
    for year in range(2001, 2023):
        df[f'3PPerMPxseason_{year}'] = df.loc[:, '3PPerMP'] * df.loc[:, f'season_{year}']

    for position in ['PF', 'PG', 'SF', 'SG']:
        df[f'3PPerMPxPosition_{position}xTrend'] = df.loc[:, '3PPerMP'] * df.loc[:, f'position_{position}'] * df.loc[:, 'Trend']

    df['3PPerMPxTrend'] = df['3PPerMP'] * df['Trend']

    return df
