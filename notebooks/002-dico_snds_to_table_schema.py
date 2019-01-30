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

from src.add_keys import add_dcirs_key_to_schemas
from src.convert import convert_schemas_to_markdown, create_sql_schema_from_docker, create_relational_diagram_from_host
from src.reformat_snds_dico import snds_dico_to_schemas
from src.utils import is_running_in_docker

snds_dico_to_schemas()
add_dcirs_key_to_schemas()
convert_schemas_to_markdown()


if is_running_in_docker():
    create_sql_schema_from_docker()
else:
    create_relational_diagram_from_host()




