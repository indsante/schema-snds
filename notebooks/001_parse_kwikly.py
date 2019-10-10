# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import re
import os

# # Variables history

# +
url2kwikly = 'https://documentation-snds.health-data-hub.fr/files/Cnam/2019-05-09_Cnam_KWIKLY-Katalogue-Sniiram-SNDS-v1.3_MPL-2.0.xlsm'

raw_excel = pd.ExcelFile(url2kwikly)
table_names = raw_excel.sheet_names
undesired_tables = [
    'Accueil', 'DCIR', 'PMSI', 'CAUSES DE DECES',
    'id_potentiel_médicales_DCIR',
    'id_potentiel_médicales_PMSI',
    'id_potentiel_médicales_CDD',
    'IR_BEN_R', 'IR_IMB_R', 'IR_PHA_R'
    ]
table_names = [t for t in table_names if t not in undesired_tables]
tables = {tab_name: pd.read_excel(raw_excel, sheet_name=tab_name, header=3) for tab_name in table_names}
# -

def create_histrory(x, years):
    var_history = []
    for c in years:
        if x[c] == 'X' and c != '*':
            var_history.append(int(c))
    if '*' in years and x['*'] == 'X':
        var_history += [int(y) for y in np.arange(2013, 2020)]
    var_history.sort()
    return var_history

# +
variables_history = {}
for table, df in tables.items():
    # exception management
    if 'Nom variable' not in df.columns:
        df.rename(columns={
            'Nom de la variable': 'Nom variable', 
            'Variable': 'Nom variable', 
            'Nom Variable': 'Nom variable',
            'Code variable': 'Nom variable',
            'Nomvariable': 'Nom variable'}, inplace=True)
    #print(table)
    variables_history[table] = pd.DataFrame()
    years = [c for c in df.columns if re.search('^20', str(c)) is not None]
    if '*' in df.columns:
        years.append('*')
    variables_history[table]['history'] = df.apply(lambda x: create_histrory(x, years), axis=1)
    variables_history[table]['var'] = df['Nom variable']
    variables_history[table]['table'] = table
    variables_history[table] = variables_history[table].loc[:, ['table', 'var', 'history']]

    
all_variables_history_df = pd.concat(variables_history.values(), axis=0)
# filter out residual garbage lines from excel
all_variables_history_df = all_variables_history_df.loc[~(all_variables_history_df['history'].apply(len) == 0), :]

# +
def compute_start(x):
    return min(x)

def compute_end(x):
    return max(x)

def compute_missings(x):
    missings = [str(y) for y in np.arange(min(x), max(x) + 1) if y not in x]
    if len(missings) > 0:
        return '_'.join(missings)
    else:
        return np.NAN
# -

all_variables_history_df['created'] = all_variables_history_df['history'].apply(compute_start)
all_variables_history_df['deleted'] = all_variables_history_df['history'].apply(compute_end)
all_variables_history_df['missings'] = all_variables_history_df['history'].apply(compute_missings)
all_variables_history_df.head()

print('Missing years for:')
missings_years = all_variables_history_df.loc[~all_variables_history_df['missings'].isna(), :]
print(len(missings_years))
missings_years

# ## Saving parsed variables history

all_variables_history_df.drop('history', axis=1).to_csv('variables_history.csv', header=True, index=False)

# # Tables history

raw_excel = pd.ExcelFile(url2kwikly)
table_names = raw_excel.sheet_names
desired_tables = ['PMSI', 'CAUSES DE DECES']
table_names = [t for t in table_names if t in desired_tables]
raw_tables_history = {tab_name: pd.read_excel(raw_excel, sheet_name=tab_name, header=7) for tab_name in table_names}

# +
tables_history = {}
for table, df in raw_tables_history.items():
    #print(table)
    tables_history[table] = pd.DataFrame()
    years = [c for c in df.columns if re.search('^20', str(c)) is not None]
    tables_history[table]['var'] = df['Table']
    tables_history[table]['history'] = df.apply(lambda x: create_histrory(x, years), axis=1)

all_tables_history_df = pd.concat(tables_history.values(), axis=0)
# filter out residual garbage lines from excel
all_tables_history_df = all_tables_history_df.loc[~(all_tables_history_df['history'].apply(len) == 0), :]
# -

all_tables_history_df['created'] = all_tables_history_df['history'].apply(compute_start)
all_tables_history_df['deleted'] = all_tables_history_df['history'].apply(compute_end)
all_tables_history_df['missings'] = all_tables_history_df['history'].apply(compute_missings)
all_tables_history_df.head()

print('Missing years for:')
missings_years = all_tables_history_df.loc[~all_tables_history_df['missings'].isna(), :]
print(len(missings_years))
missings_years

# ## Saving parsed tables history

all_tables_history_df.drop('history', axis=1).to_csv('tables_history.csv', header=True, index=False)


