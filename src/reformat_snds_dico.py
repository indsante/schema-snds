import os
import re
from collections import defaultdict
from typing import Tuple

import pandas as pd
from tableschema import Schema

from src.table_schema_types import STRING, NUMBER, DATE, DATETIME, ANY


def read_snds_vars(dico_snds_path):
    snds_vars_path = os.path.join(dico_snds_path, 'app', 'app_data', 'snds_vars.csv')
    return (pd
            .read_csv(snds_vars_path)
            .rename(columns={'var': 'name'})
            )


def extract_type_and_length(type_str: str) -> Tuple[str, str]:
    pattern = '(.*)\((.*)\)'
    if pd.isna(type_str):
        return [None, None]

    match = re.match(pattern, type_str)
    if match:
        return [match[1], match[2]]
    else:
        return [type_str, None]


def add_type_and_length_columns(df: pd.DataFrame) -> pd.DataFrame:
    df_type_and_length = (df['format']
                          .str.lower()
                          .map(extract_type_and_length)
                          .apply(pd.Series)
                          .rename(columns={0: 'type', 1: 'length'})
                          )
    return pd.concat([df, df_type_and_length], axis=1)


def convert_to_table_schema_type(df: pd.DataFrame) -> pd.DataFrame:
    map_types_snds_to_table_schema = defaultdict(lambda: ANY, {
        'numérique': NUMBER,
        'number': NUMBER,
        'num': NUMBER,
        'caractère': STRING,
        'alphanumérique': STRING,
        'varchar2': STRING,
        'char': STRING,
        'raw': STRING,
        'car': STRING,
        'date': DATE,
        'datetime': DATETIME,
    })
    df['type'] = (df['type']
                  .str.lower()
                  .str.strip()
                  .map(map_types_snds_to_table_schema)
                  )
    return df


def get_table_schema(df_table: pd.DataFrame) -> Schema:
    fields = list()
    columns = ['name', 'description', 'type']
    for index, row in df_table[columns].iterrows():
        fields.append(row.to_dict())
    descriptor = {'fields': fields}
    return Schema(descriptor, strict=True)


def write_all_schema(df: pd.DataFrame, directory) -> None:
    for i, (table, df_table) in enumerate(df.groupby('table')):
        schema = get_table_schema(df_table)
        path = os.path.join(directory, table + '.json')
        schema.save(path, ensure_ascii=False)


if __name__ == '__main__':
    print(os.getcwd())
    df_vars = read_snds_vars('../../dico-snds')
    df_vars = add_type_and_length_columns(df_vars)
    df_vars = convert_to_table_schema_type(df_vars)
    write_all_schema(df_vars, '../data/tableschema')
