"""
L'objectif de ces fonctions est de recréer les données nécessaire à l'application dico-snds,
à partir des données stockées dans Table-Schema

"""

import logging
import os
from typing import Union, List

import pandas as pd

from src.constants import APP_DICO_SNDS_PATH
from src.utils import get_all_schema

EDGES_CSV = "snds_links.csv"
NODES_CSV = "snds_nodes.csv"
TABLES_CSV = "SNDS_tables_lib.csv"
SNDS_VARIABLES_CSV = "snds_vars.csv"

DICO_VARIABLE = 'var'
SCHEMA_PRODUIT = 'produit'

PRODUIT_TO_GROUP = {
    "BENEFICIAIRE": 1,
    "DCIR_DCIRS": 2,
    "DCIRS": 3,
    "DCIR": 4,
    "Causes de décès": 5,
    "CARTOGRAPHIE_PATHOLOGIES": 6,
    "PMSI MCO": 7,
    "PMSI HAD": 8,
    "PMSI SSR": 9,
    "PMSI RIM-P": 10,
}

pd.options.display.max_columns = 100


def table_schema_to_app_dico():
    logging.info("Convert schemas to dico-snds app data")
    os.makedirs(APP_DICO_SNDS_PATH, exist_ok=True)
    table_schema_to_snds_tables()
    table_schema_to_snds_variables()
    table_schema_to_snds_graph()


def table_schema_to_snds_variables():
    dico_produit = "produit"
    logging.info("Convert schemas to {}".format(SNDS_VARIABLES_CSV))
    variables_list = []
    for schema in get_all_schema():
        for field in schema.fields:
            descriptor = field.descriptor
            length = descriptor.get('length', '')
            length = ' ({})'.format(length) if length else ''
            variables_list.append({
                # dico_produit: schema.descriptor[SCHEMA_PRODUIT],
                'table': schema.descriptor['name'],
                DICO_VARIABLE: descriptor['name'],
                'format': descriptor['type'] + length,
                'description': descriptor['description'],
                'nomenclature': descriptor.get('nomenclature', ''),
            })
    df = pd.DataFrame(variables_list,
                      columns=[
                          # dico_produit,
                          'table', DICO_VARIABLE, 'format', 'description', 'nomenclature'])
    df = df.sort_values([
        # dico_produit,
        'table', DICO_VARIABLE])
    snds_variable_path = os.path.join(APP_DICO_SNDS_PATH, SNDS_VARIABLES_CSV)
    df.to_csv(snds_variable_path, index=False, sep=';')


def table_schema_to_snds_tables():
    logging.info("Convert schemas to {}".format(TABLES_CSV))
    dico_produit = "Produit"
    dico_table = "Table"
    dico_libelle = 'Libelle'
    table_list = []
    for schema in get_all_schema():
        table_list.append({
            dico_produit: schema.descriptor[SCHEMA_PRODUIT],
            dico_table: schema.descriptor['name'],
            dico_libelle: schema.descriptor['title'],

        })
    df = pd.DataFrame(table_list, columns=[dico_produit, dico_table, dico_libelle])
    df = df.sort_values([dico_produit, dico_table, dico_libelle])
    snds_table_path = os.path.join(APP_DICO_SNDS_PATH, TABLES_CSV)
    df.to_csv(snds_table_path, index=True, sep=';')


def table_schema_to_snds_graph():
    logging.info("Convert schemas to {} and {}".format(NODES_CSV, EDGES_CSV))
    node_dict = dict()
    edge_list = []
    for i, schema in enumerate(get_all_schema()):
        descriptor = schema.descriptor
        table_name = descriptor['name']
        node_dict[table_name] = {
            'name': table_name,
            'description': descriptor['title'],
            'group': PRODUIT_TO_GROUP[descriptor[SCHEMA_PRODUIT]],
            'index': i,
            'nb_vars': 1,
        }
    for schema in get_all_schema():
        descriptor = schema.descriptor
        for foreign_key in descriptor.get("foreignKeys", []):
            edge_list.append({
                'source': node_dict[descriptor['name']]['index'],
                'target': node_dict[foreign_key['reference']['resource']]['index'],
                'group': 1,
                'joint_var': create_join_str(foreign_key['fields'], foreign_key['reference']['fields']),

            })
    df_nodes = pd.DataFrame(list(node_dict.values()), columns=['name', 'description', 'group', 'index', 'nb_vars'])
    df_nodes = df_nodes.sort_values(['index'])
    snds_nodes_path = os.path.join(APP_DICO_SNDS_PATH, NODES_CSV)
    df_nodes.to_csv(snds_nodes_path, index=False)

    df_edges = pd.DataFrame(edge_list, columns=['source', 'target', 'group', 'joint_var'])
    df_edges = df_edges.sort_values(['source', 'target'])
    snds_edges_path = os.path.join(APP_DICO_SNDS_PATH, EDGES_CSV)
    df_edges.to_csv(snds_edges_path, index=False)


def create_join_str(source_fields: Union[str, List[str]], referenced_fields: Union[str, List[str]]) -> str:
    if isinstance(source_fields, str):
        source_fields = [source_fields]
    if isinstance(referenced_fields, str):
        referenced_fields = [referenced_fields]

    sep = ' + '
    if set(source_fields) == set(referenced_fields):
        return sep.join(source_fields)
    else:
        return '{} => {}'.format(sep.join(source_fields), sep.join(referenced_fields))


if __name__ == '__main__':
    table_schema_to_app_dico()
