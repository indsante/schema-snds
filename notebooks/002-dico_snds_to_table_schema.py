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

from src.build_tableschema.add_keys import add_dcirs_keys
from src.byproducts.convert import table_schema_to_markdown
from src.byproducts.relational_diagram import generate_postgresql_tables_within_docker, \
    generate_relational_diagram_from_host
from src.build_tableschema.reformat_snds_dico import build_tableschema_from_dico_snds
from src.utils import is_running_in_docker

build_tableschema_from_dico_snds()
add_dcirs_keys()
table_schema_to_markdown()


if is_running_in_docker():
    generate_postgresql_tables_within_docker()
else:
    generate_relational_diagram_from_host()




