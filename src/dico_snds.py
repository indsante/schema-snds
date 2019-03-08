"""
L'objectif de ces fonctions est de recréer les données nécessaire à l'application dico-snds,
à partir des données stockées dans Table-Schema

"""

import logging
import os

import pandas as pd

from src.constants import APP_DICO_SNDS_PATH
from src.utils import get_all_schema

pd.options.display.max_columns = 100


def table_schema_to_app_dico():
    logging.info("Convert schemas to dico-snds app data")
    os.makedirs(APP_DICO_SNDS_PATH, exist_ok=True)
    table_schema_to_snds_tables()
    table_schema_to_snds_variables()
    table_schema_to_snds_graph()


def table_schema_to_snds_variables():
    logging.info("Convert schemas to snds_variables.csv")
    variables_list = []
    for schema in get_all_schema():
        for field in schema.fields:
            descriptor = field.descriptor
            length = descriptor.get('length', '')
            length = ' ({})'.format(length) if length else ''
            variables_list.append({
                'produit': schema.descriptor['produit'],
                'table': schema.descriptor['name'],
                'var': descriptor['name'],
                'format': descriptor['type'] + length,
                'description': descriptor['description'],
                'nomenclature': descriptor.get('nomenclature', ''),
            })
    df = pd.DataFrame(variables_list, columns=['produit', 'table', 'var', 'format', 'description', 'nomenclature'])
    df = df.sort_values(['produit', 'table', 'var'])
    snds_variable_path = os.path.join(APP_DICO_SNDS_PATH, 'snds_variables.csv')
    df.to_csv(snds_variable_path, index=False)


def table_schema_to_snds_tables():
    pass


def table_schema_to_snds_graph():
    pass


if __name__ == '__main__':
    table_schema_to_app_dico()
