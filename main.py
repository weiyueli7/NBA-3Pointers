import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from tqdm import tqdm
import time
import json

from data import *
from model import *
from eda import *




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--get_data', default=False, type=bool)
    parser.add_argument('--salary_source', default='hoopshype', type=str, choices=['hoopshype', 'espn'])
    
    args = parser.parse_args()

    if args.get_data:
        if args.salary_source == 'hoopshype':
            get_hoopshype_salary()
        elif args.salary_source == 'espn':
            get_espn_salary()
        else:
            raise ValueError('Invalid salary source')
        get_player_statistics()

    # Load data
    
    # Load player statistics
    players = pd.DataFrame()
    for year in tqdm(range(2000, 2023)):
        cur_year = process_year(year)
        players = pd.concat([players, cur_year], ignore_index=True, axis=0)

    # Load salaries
    salaries = pd.DataFrame()

    if args.salary_source == 'hoopshype':
        salary_func = process_hoopshype_salary
    elif args.salary_source == 'espn':
        salary_func = process_espn_salary



    for year in tqdm(range(2000, 2023)):
        cur_year = salary_func(year)
        salaries = pd.concat([salaries, cur_year], ignore_index=True, axis=0)

    # Merge salaries and player statistics
    df = merge_and_encoding(players, salaries)


    # Feature engineering

    df = feature_engineering(df)

    print("Summary Statistics for all players: \n")
    ss = df[['3PPerMP', 'PTSPerMP', 'TRBPerMP', 'ASTPerMP', 'PFPerMP', 'STLPerMP']].describe().to_latex()
    print(ss)
    os.makedirs('results/summary_statistics', exist_ok=True)
    with open(f'results/summary_statistics/summary_statistics.tex', 'w') as f:
        f.write(ss)

    # Visualizations

    viz_average_salary(df)
    viz_three_point_evolution(df)
    viz_salary_cap()


    # Run Models
    
    for model in [f"model_{i+1}" for i in range(6)]:
        with open(f"model_configs/{model}.json", 'r') as file:
                config_dict = json.load(file)
        independent_vars = config_dict['independent_vars']
        dependent_var = config_dict['dependent_var']
        print("----------------------------------\n")
        print(f"Running {model}\n\n")
        print("Independent Variables: ", independent_vars, "\n")
        print("Dependent Variable: ", dependent_var, "\n")
        print("----------------------------------\n\n")
        OLS(df, independent_vars, dependent_var, model)
        print("----------------------------------\n\n")
    


if __name__ == '__main__':
    main()
