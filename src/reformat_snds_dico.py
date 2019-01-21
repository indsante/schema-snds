import pandas as pd
import re


def extract_type_and_length(type_str):
    pattern = '(.*)\((.*)\)'
    if pd.isna(type_str):
        return [None, None]

    match = re.match(pattern, type_str)
    if match:
        return [match[1], match[2]]
    else:
        return [type_str, None]


def add_type_and_length_columns(df):
    df_type_and_length = (df['format']
                          .str.lower()
                          .map(extract_type_and_length)
                          .apply(pd.Series)
                          .rename(columns={0: 'type', 1: 'length'})
                          )
    return pd.concat([df, df_type_and_length], axis=1)


NUMERIC = 'Numeric'
STRING = 'String'
DATE = 'Date'
DATETIME = 'DateTime'

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
}

if __name__ == '__main__':
    df = pd.read_csv('../../SNDS-portail/Dictionnaire/app/app_data/snds_vars.csv')
    df = add_type_and_length_columns(df)
    df['generic_type'] = df['type'].map(map_to_generic_type)
    df.rename(columns={})
