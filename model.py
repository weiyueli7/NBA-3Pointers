import os
import pandas as pd
import numpy as np
import statsmodels.api as sm


def OLS(df, independent_vars, dependent_var, name):

    new_df = df.copy()
    if dependent_var == 'next_year_salary':
        new_df = new_df.dropna(subset=['next_year_salary'])

    X = new_df[independent_vars]  # Independent variables
    y = new_df[dependent_var]  # Dependent variable

    # Adding a constant term for the intercept
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit(cov_type='HC1')

    print(model.summary())

    os.makedirs('results/models', exist_ok=True)

    with open(f'results/models/{name}.tex', 'w') as f:
        f.write(model.summary().as_latex())
