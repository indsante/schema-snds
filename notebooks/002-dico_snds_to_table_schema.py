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

dico_snds_path = '../dico-snds'

# +
df_vars = read_snds_vars(dico_snds_path)
df_vars = add_type_and_length_columns(df_vars)
df_vars = convert_to_table_schema_type(df_vars)

df_table_lib = read_snds_table_lib(dico_snds_path)

df = merge_vars_table(df_vars, df_table_lib)
df.head(2)
# -

write_all_schema(df, 'data/tableschema')
df.to_csv('data/variables.csv', index=False)


