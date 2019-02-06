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

from src.add_keys import add_dcirs_keys_to_table_schema
from src.convert import table_schema_to_markdown, table_schema_to_sql_within_docker, table_schema_to_relational_diagram_from_host
from src.reformat_snds_dico import dico_snds_to_table_schema
from src.utils import is_running_in_docker

dico_snds_to_table_schema()
add_dcirs_keys_to_table_schema()
table_schema_to_markdown()


if is_running_in_docker():
    table_schema_to_sql_within_docker()
else:
    table_schema_to_relational_diagram_from_host()




