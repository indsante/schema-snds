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

# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# **Change current directory**

import os
import sys
ROOT_PATH = os.path.dirname(os.getcwd())
os.chdir(ROOT_PATH)
sys.path.append(ROOT_PATH)

# **Generic notebook import**

import pandas as pd
pd.options.display.max_rows = 30
pd.options.display.max_columns = 100
pd.options.display.max_colwidth = 100

from src.reformat_snds_dico import *
from tableschema import validate

df = read_snds_vars('../SNDS-portail/Dictionnaire/app/app_data/snds_vars.csv')
df.head(2)

df = add_type_and_length_columns(df)
df = convert_to_table_schema_type(df)
df.head(2)

write_all_schema(df, 'data/table_schema')




