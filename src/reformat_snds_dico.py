import logging
import os
import re
from collections import defaultdict
from typing import Tuple

import pandas as pd
from tableschema import Schema

from src.constants import STRING, NUMBER, DATE, DATETIME, ANY, DICO_SNDS_PATH, MAIN_SCHEMA_DIR

FORMAT_SOURCE = 'format_source'
PRODUIT = 'produit'


def read_snds_vars() -> pd.DataFrame:
    snds_vars_path = os.path.join(DICO_SNDS_PATH, 'snds_vars.csv')
    return (pd
            .read_csv(snds_vars_path)
            .rename(columns={'var': 'variable',
                             'format': FORMAT_SOURCE
                             })
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
    df_type_and_length = (df[FORMAT_SOURCE]
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


def read_snds_table_lib() -> pd.DataFrame:
    snds_vars_path = os.path.join(DICO_SNDS_PATH, 'SNDS_tables_lib.csv')
    df = (pd
          .read_csv(snds_vars_path, sep=';', dtype=str)
          .rename(columns={'Unnamed: 0': 'table_id',
                           'Produit': PRODUIT,
                           'Libelle': 'libelle_table',
                           'Champ': 'champ_table'
                           })
          )
    df[PRODUIT] = df[PRODUIT].str.replace('DCIR/DCIRS', 'DCIR_DCIRS')
    return df


def merge_vars_table(df_vars, df_table_lib):
    logging.warning("Les tables {} sont présentes dans les 'variables' et pas dans les 'tables', "
                    "et réciproquement pour {}"
                    .format(set(df_vars.table) - set(df_table_lib.Table), set(df_table_lib.Table) - set(df_vars.table))
                    )

    logging.info("Nombre de lignes avant jointure : variables {}, tables {} ".format(len(df_vars), len(df_table_lib)))
    df = (df_vars
          .merge(df_table_lib, how='inner', left_on='table', right_on='Table', validate='many_to_one')
          .drop(columns='Table')
          )
    logging.info("Nombre de lignes après jointure : {}".format(len(df)))

    return df


def get_dico_snds_variables() -> pd.DataFrame:
    logging.info("Reformat and combine informations from dico-snds files 'snds_vars.csv' and 'SNDS_tables_lib.csv'")
    df_vars = read_snds_vars()
    df_vars = add_type_and_length_columns(df_vars)
    df_vars = convert_to_table_schema_type(df_vars)
    df_table_lib = read_snds_table_lib()
    df = merge_vars_table(df_vars, df_table_lib)
    return df


def write_all_schema(df: pd.DataFrame) -> None:
    logging.info("Write all raw tableschema from 'snds-dico'")
    for i, ((produit, table_name), df_table) in enumerate(df.groupby([PRODUIT, 'table'])):
        schema = get_table_schema(df_table, table_name)
        path = os.path.join(MAIN_SCHEMA_DIR, produit, table_name + '.json')
        schema.save(path, ensure_ascii=False)


def get_table_schema(df_table: pd.DataFrame, table_name: str) -> Schema:
    fields = list()
    for i, row in df_table.iterrows():
        fields.append({
            'name': row['variable'],
            'description': row['description'],
            'type': row['type']
        })
    descriptor = {'fields': fields, 'title': table_name}
    return Schema(descriptor, strict=True)


def dico_snds_to_table_schema():
    df = get_dico_snds_variables()
    logging.info("Write reformated snds-dico information")
    df.to_csv('data/variables.csv', index=False)
    write_all_schema(df)
