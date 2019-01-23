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

# # Préparation du dico-snds

df = (pd
      .read_csv('../SNDS-portail/Dictionnaire/app/app_data/snds_vars.csv')
      .rename(columns={
          'var': 'column',
          'description': 'column_comment'
      })
     )
df.head(2)

# +
import re
pattern = '(.*)\((.*)\)'
def extract_type_and_length(type_str):
    if pd.isna(type_str):
        return [None, None]
    
    match = re.match(pattern, type_str)
    if match:
        return [match[1], match[2]]
    else:
        return [type_str, None]

def add_type_and_lenght_columns(df):
    df_type_and_length = (df['format']
                          .map(extract_type_and_length)
                          .apply(pd.Series)
                          .rename(columns={0: 'datatype', 1: 'length'})
                          )
    return (pd.concat([df, df_type_and_length], axis=1)
            .drop(columns=['format'])
           )

df = add_type_and_lenght_columns(df)
df.head(2)

# +
NUMERIC = 'Numeric'
STRING = 'String'
DATE = 'Date'
DATETIME = 'DateTime'

def add_generic_type(df):
    map_to_generic_type = {
        'numérique': NUMERIC,
        'number': NUMERIC,
        'num': NUMERIC,
        'caractère': STRING,
        'alphanumérique': STRING,
        'varchar2': STRING,
        'char': STRING,
        'raw': STRING,
        'car': STRING,
        'date': DATE,
        'datetime': DATETIME,
        None: 'undefined',
    }

    df.datatype = (df.datatype
                   .str.lower()
                   .str.strip()
                  )
    df['generic_type'] = (df.datatype
                          .str.lower()
                          .str.strip()
                          .map(map_to_generic_type)
                         )
    
    is_na = df.generic_type.isna()
    if is_na.any():
        raise Exception('Some types are not mapped {}'.format(df[is_na].datatype.unique()))

    return df.drop(columns=['datatype'])

df = add_generic_type(df)
df.head(2)
# -

df.to_csv("data/dico_snds.csv", index=False)

# +
from sqlalchemy import MetaData, Table, Column, types, create_engine
NUMERIC = 'Numeric'
STRING = 'String'
DATE = 'Date'
DATETIME = 'DateTime'

map_to_sqlalchemy_type = {
    NUMERIC: types.Numeric,
    STRING: types.String,
    DATE: types.Date,
    DATETIME: types.DateTime,
}
df['sqlalchemy_type'] = df.generic_type.map(map_to_sqlalchemy_type)
def convert_rows_to_columns_list(df):
    columns = list()
    for index, row in df.iterrows():
        column = Column(name=row['column'], 
                        type_=row['sqlalchemy_type'],
                        comment=row['column_comment'],
                       )
        columns.append(column)
    return columns

convert_rows_to_columns_list(df.head(3))
# + {}
from sqlalchemy import MetaData, Table, Column, types, create_engine

connection = create_engine('postgresql://postgres@localhost:5432/postgres')
connection = create_engine('sqlite:///notebooks/ignore/db.sql')

metadata = MetaData(bind=connection)

for i, (table, df_table) in enumerate(df.dropna(subset=['sqlalchemy_type']).groupby('table')):
    if i >= 2: 
        break
    columns = convert_rows_to_columns_list(df_table)
    Table(table, metadata, *columns)

metadata.create_all(connection, checkfirst=True)
# -
# https://docs.sqlalchemy.org/en/latest/faq/metadata_schema.html#how-can-i-get-the-create-table-drop-table-output-as-a-string
from sqlalchemy.schema import CreateTable
for t in metadata.tables.values():
    print(CreateTable(t))


