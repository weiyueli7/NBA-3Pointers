import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def viz_average_salary(df):

    os.makedirs('results/figures', exist_ok=True)

    seasonal_salary_mean = df.groupby('Season')['salary'].mean() * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    seasonal_salary_mean.plot(kind='line', ax=ax, color='b', marker='o', linestyle='-', linewidth=2, markersize=8)

    ax.set_xticks(range(2000, 2023, 1))
    ax.set_xticklabels(range(2000, 2023, 1), rotation=45)

    ax.set_title("Average Salary in Thousands of USD by Season", fontsize=16)
    ax.set_xlabel('Season', fontsize=14)
    ax.set_ylabel('Salary in Thousands in 2023 Dollars', fontsize=14)

    ax.grid(True, linestyle='--', alpha=0.6)

    ax.legend(['Average Salary'], loc='upper left', fontsize=12)

    plt.tight_layout()

    plt.savefig(f'results/figures/average_salary.png')

    # plt.show()


def viz_three_point_evolution(df):


    os.makedirs('results/figures', exist_ok=True)

    all_sea = df.groupby('Season').sum()


    fig, ax = plt.subplots(figsize=(10, 6))

    (all_sea['3PA'] / all_sea['FGA']).plot(kind='line', ax=ax, color='g', marker='s', linestyle='-', linewidth=2, markersize=8)

    ax.set_xticks(range(2000, 2023, 1))
    ax.set_xticklabels(range(2000, 2023, 1), rotation=45)

    ax.set_title("Ratio of Three-Point Attempts by Season", fontsize=16)
    ax.set_xlabel('Season', fontsize=14)
    ax.set_ylabel('Three-Point Attempts Ratio', fontsize=14)

    ax.grid(True, linestyle='--', alpha=0.6)

    ax.legend(['Average 3PA'], loc='upper left', fontsize=12)
    plt.tight_layout()

    plt.savefig(f'results/figures/three_point_evolution.png')

    # plt.show()

def viz_salary_cap():

    os.makedirs('results/figures', exist_ok=True)

    salary_caps = pd.read_csv('data/salary_cap/salary_cap.csv')

    salary_caps['Salary Cap'] = salary_caps['Salary Cap'].str.replace(',', '').str.strip('$').astype(int)
    salary_caps['Salary Cap in 2022 Dollars'] = salary_caps['Salary Cap in 2022 Dollars'].str.replace(',', '').str.strip('$').astype(int)
    salary_caps['Year'] = salary_caps['Year'].apply(lambda x: x.split('-')[0]).astype(int)

    df = pd.read_csv('data/salary_cap/MEHOINUSA672N.csv')
    df['Year'] = pd.to_datetime(df['DATE']).dt.year
    df['Annual Household Income in 2022 Dollars'] = df['MEHOINUSA672N']


    plt.figure(figsize=(15, 8))

    plt.plot(salary_caps["Year"], salary_caps["Salary Cap"] / 1_000_000, label="Salary Cap", color="blue", marker='o')
    plt.plot(salary_caps["Year"], salary_caps["Salary Cap in 2022 Dollars"] / 1_000_000, label="Salary Cap in 2022 Dollars", color="green", marker='x')

    plt.plot(df["Year"], df["Annual Household Income in 2022 Dollars"] / 1_000_000, label="Annual Household Income in 2022 Dollars", color="red", marker='^')

    last_year = df["Year"].iloc[-1]
    last_salary_cap = salary_caps["Salary Cap in 2022 Dollars"].iloc[-1] / 1_000_000
    last_household_income = df["Annual Household Income in 2022 Dollars"].iloc[-1] / 1_000_000

    first_year = df["Year"].iloc[0]
    first_salary_cap = salary_caps["Salary Cap in 2022 Dollars"].iloc[0] / 1_000_000
    first_household_income = df["Annual Household Income in 2022 Dollars"].iloc[0] / 1_000_000

    plt.text(last_year - 0.5, last_salary_cap - 10, f"{last_salary_cap:,}", color="green", ha='left', fontdict={'size': 12})
    plt.text(last_year - 0.5, last_household_income + 5, f"{last_household_income:,}", color="red", ha='left', fontdict={'size': 12})

    plt.text(first_year - 0.5, first_salary_cap + 5, f"{first_salary_cap:,}", color="green", ha='left', fontdict={'size': 12})
    plt.text(first_year - 0.5, first_household_income -5, f"{first_household_income:,}", color="red", ha='left', fontdict={'size': 12})



    plt.title("Trend of NBA Salary Cap for Each Team Over the Years", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Amount in Millions of USD", fontsize=14)
    plt.xticks(salary_caps["Year"], rotation=45)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'results/figures/salary_cap.png')

    # plt.show()