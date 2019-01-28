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

# +
from table_schema_to_markdown import convert_source

from src.reformat_snds_dico import get_dico_snds_variables, write_all_schema
from src.add_keys import add_dcirs_keys
from src.convert import convert_schemas_to_markdown, create_schemas_in_sql_storage
# -

dico_snds_path = '../dico-snds'
tableschema_dir = 'data/tableschema'
df = get_dico_snds_variables(dico_snds_path)
df.to_csv('data/variables.csv', index=False)
write_all_schema(df, 'data/tableschema')


dcirs_dir = 'data/tableschema/dcirs'
add_dcirs_keys(dcirs_dir)


convert_schemas_to_markdown(tableschema_dir)



# +
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres@localhost:5432/postgres')
engine = create_engine('sqlite:///notebooks/ignore/db.sql')

create_schemas_in_sql_storage(dcirs_dir, engine)
# -



