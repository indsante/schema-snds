"""
L'objectif de ces fonctions est de recréer les données nécessaire à l'application dico-snds,
à partir des données stockées dans Table-Schema

"""

import logging
import os
from collections import defaultdict
from os.path import join as pjoin
from shutil import copyfile
from typing import Union, List

import pandas as pd
from tableschema import Schema, Table

from src.constants import DICO_SNDS_DIR, NO_NOMENCLATURE, DATE_CREATED, DATE_DELETED, DATE_MISSING, \
    NOMENCLATURE, TYPE_ORACLE, NOMENCLATURES_DIR
from src.utils import get_all_schema, get_all_nomenclatures_csv_schema_path, get_used_nomenclatures

DICO_EDGES_CSV = "snds_links.csv"
DICO_NODES_CSV = "snds_nodes.csv"
DICO_TABLES_CSV = "snds_tables.csv"
DICO_VARIABLES_CSV = "snds_vars.csv"
DICO_NOMENCLATURES_CSV = "snds_nomenclatures.csv"
DICO_CSV_FILES = [DICO_TABLES_CSV, DICO_VARIABLES_CSV, DICO_NOMENCLATURES_CSV, DICO_EDGES_CSV, DICO_NODES_CSV]

DICO_VARIABLE = 'var'
SCHEMA_PRODUIT = 'produit'
TITRE = "titre"

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
    "DAMIR": 11,
    "EGB": 12
}

pd.options.display.max_columns = 100

DATE_CREATION = 'creation'
DATE_SUPRESSION = 'suppression'
DATES_MANQUANTES = 'dates_manquantes'


def generate_dico_snds(work_dir, products):
    logging.info("Convert schemas to dico-snds app data")
    os.makedirs(pjoin(work_dir, DICO_SNDS_DIR), exist_ok=True)
    table_schema_to_snds_variables(work_dir, products)
    table_schema_to_snds_tables(work_dir, products)
    table_schema_to_snds_graph(work_dir, products)
    table_schema_to_snds_nomenclatures(work_dir, products)
    cp_nomenclatures(work_dir, products)


def cp_nomenclatures(work_dir, products):
    used_nomenclatures = get_used_nomenclatures(work_dir, products)

    rooted_nomenclatures_dir = pjoin(work_dir, NOMENCLATURES_DIR)
    rooted_nomenclatures_dico_snds_dir = pjoin(work_dir, DICO_SNDS_DIR, NOMENCLATURES_DIR)
    logging.info(" - copy the csv in {} subdirectories into {}".format(
        rooted_nomenclatures_dir,
        rooted_nomenclatures_dico_snds_dir
    ))
    os.makedirs(rooted_nomenclatures_dico_snds_dir, exist_ok=True)
    for root, dirs, files in os.walk(rooted_nomenclatures_dir):
        for file in files:
            if file.endswith('.csv') and file[:-4] in used_nomenclatures:
                source_file_path = pjoin(root, file)
                target_file_path = pjoin(rooted_nomenclatures_dico_snds_dir, file)
                copyfile(source_file_path, target_file_path)


def table_schema_to_snds_nomenclatures(work_dir, products):
    used_nomenclatures = get_used_nomenclatures(work_dir, products)

    logging.info(" - create a table with all nomenclatures title's : {}".format(DICO_NOMENCLATURES_CSV))
    nomenclature_dict = defaultdict(set)
    for schema in get_all_schema(work_dir, products):
        # table_name = schema.descriptor.get('name')
        for field in schema.fields:
            descriptor = field.descriptor
            variable_name = descriptor.get('name')
            nomenclature = str(descriptor.get(NOMENCLATURE, ''))
            if nomenclature:
                nomenclature_dict[nomenclature].add(variable_name)

    nomenclature_list = []
    for csv_path, schema_path in get_all_nomenclatures_csv_schema_path(pjoin(work_dir, NOMENCLATURES_DIR)):
        schema = Schema(schema_path)
        nomenclature = schema.descriptor['name']
        if nomenclature not in used_nomenclatures:
            continue

        table = Table(csv_path, schema=schema_path)
        n_rows = 0
        for row in table.iter():
            n_rows += 1

        variables_liees = ', '.join(sorted(list(nomenclature_dict[nomenclature])))
        if not variables_liees:
            variables_liees = 'Aucune variable liée'
        nomenclature_list.append({
            NOMENCLATURE: nomenclature,
            TITRE: schema.descriptor.get('title', 'Titre manquant'),
            # 'description': schema.descriptor.get('description', ''),
            'variables_liees': variables_liees,
            'nombre_lignes': n_rows
        })
    df = pd.DataFrame(nomenclature_list, columns=[NOMENCLATURE, TITRE, 'variables_liees', 'nombre_lignes'])
    df = df.sort_values([NOMENCLATURE])
    snds_nomenclature_path = pjoin(work_dir, DICO_SNDS_DIR, DICO_NOMENCLATURES_CSV)
    df.to_csv(snds_nomenclature_path, index=False)


def table_schema_to_snds_variables(work_dir, products):
    # dico_produit = "produit"
    logging.info(" - convert schemas to {}".format(DICO_VARIABLES_CSV))
    variables_list = []
    for schema in get_all_schema(work_dir, products):
        for field in schema.fields:
            descriptor = field.descriptor
            length = descriptor.get('length', '')
            length = ' ({})'.format(length) if length else ''
            format_variable = descriptor[TYPE_ORACLE] + length
            nomenclature = str(descriptor.get(NOMENCLATURE, '')).split(':')[0]
            nomenclature = nomenclature if (nomenclature.strip() != 'nan') else NO_NOMENCLATURE

            variables_list.append({
                # dico_produit: schema.descriptor[SCHEMA_PRODUIT],
                'table': schema.descriptor['name'],
                DICO_VARIABLE: descriptor['name'],
                'format': format_variable,
                'description': descriptor['description'],
                NOMENCLATURE: nomenclature,
                DATE_CREATION: str(descriptor.get(DATE_CREATED, '')),
                DATE_SUPRESSION: str(descriptor.get(DATE_DELETED, '')),
                DATES_MANQUANTES: ', '.join(descriptor.get(DATE_MISSING, ''))
            })
    df = pd.DataFrame(variables_list,
                      columns=[
                          # dico_produit,
                          'table', DICO_VARIABLE, 'format', 'description', NOMENCLATURE, DATE_CREATION,
                          DATE_SUPRESSION, DATES_MANQUANTES])
    df = df.sort_values([
        # dico_produit,
        'table',
        # DICO_VARIABLE
    ],
        kind="mergesort"  # Do not loose original variables order while sorting
    )
    snds_variable_path = pjoin(work_dir, DICO_SNDS_DIR, DICO_VARIABLES_CSV)
    print(snds_variable_path)
    df.to_csv(snds_variable_path, index=False)


def table_schema_to_snds_tables(work_dir, products):
    logging.info(" - convert schemas to {}".format(DICO_TABLES_CSV))
    dico_produit = "Produit"
    dico_table = "Table"
    dico_libelle = 'Libelle'

    table_list = []
    for schema in get_all_schema(work_dir, products):
        logging.debug("   - convert schema {}".format(schema.descriptor['name']))
        table_list.append({
            dico_produit: schema.descriptor[SCHEMA_PRODUIT],
            dico_table: schema.descriptor['name'],
            dico_libelle: schema.descriptor['title'],
            DATE_CREATION: schema.descriptor['history'][DATE_CREATED],
            DATE_SUPRESSION: schema.descriptor['history'][DATE_DELETED],
            DATES_MANQUANTES: ', '.join(schema.descriptor['history'][DATE_MISSING])

        })
    df = pd.DataFrame(table_list, columns=[dico_produit, dico_table, dico_libelle, DATE_CREATION, DATE_SUPRESSION,
                                           DATES_MANQUANTES])
    df = df.sort_values([dico_produit, dico_table, dico_libelle])
    snds_table_path = pjoin(work_dir, DICO_SNDS_DIR, DICO_TABLES_CSV)
    df.to_csv(snds_table_path, index=False)


def table_schema_to_snds_graph(work_dir, products):
    logging.info(" - convert schemas to {} and {}".format(DICO_NODES_CSV, DICO_EDGES_CSV))

    node_dict = dict()
    schemas = [schema for schema in
               get_all_schema(work_dir, products) if schema.descriptor["produit"] not in ["DAMIR", "EGB"]]
    for i, schema in enumerate(schemas):
        descriptor = schema.descriptor
        table_name = descriptor['name']
        node_dict[table_name] = {
            'name': table_name,
            'description': descriptor['title'],
            'group': PRODUIT_TO_GROUP[descriptor[SCHEMA_PRODUIT]],
            'index': i,
            'nb_vars': 1,
        }

    edge_list = []
    for schema in schemas:
        descriptor = schema.descriptor
        for foreign_key in descriptor.get("foreignKeys", []):
            try:
                target = node_dict[foreign_key['reference']['resource']]['index']
            except KeyError as e:
                logging.error("Missing foreign table", e)
                raise e

            edge_list.append({
                'source': node_dict[descriptor['name']]['index'],
                'target': target,
                'joint_var': create_join_str(foreign_key['fields'], foreign_key['reference']['fields'],
                                             foreign_key.get('description', None)),

            })
    df_nodes = pd.DataFrame(list(node_dict.values()), columns=['name', 'description', 'group', 'index', 'nb_vars'])
    df_nodes = df_nodes.sort_values(['index'])
    snds_nodes_path = pjoin(work_dir, DICO_SNDS_DIR, DICO_NODES_CSV)
    df_nodes.to_csv(snds_nodes_path, index=False)

    df_edges = pd.DataFrame(edge_list, columns=['source', 'target', 'joint_var'])
    df_edges = (df_edges
                .groupby(['source', 'target'])['joint_var']
                .apply(lambda s: ' | '.join(s))
                .reset_index()
                .sort_values(['source', 'target'])
                )
    snds_edges_path = pjoin(work_dir, DICO_SNDS_DIR, DICO_EDGES_CSV)
    df_edges.to_csv(snds_edges_path, index=False)


def create_join_str(source_fields: Union[str, List[str]], referenced_fields: Union[str, List[str]],
                    description: str = None) -> str:
    if isinstance(source_fields, str):
        source_fields = [source_fields]
    if isinstance(referenced_fields, str):
        referenced_fields = [referenced_fields]

    sep = ' + '
    if set(source_fields) == set(referenced_fields):
        result = sep.join(source_fields)
    else:
        result = '{} => {}'.format(sep.join(source_fields), sep.join(referenced_fields))
    if description:
        result += ' | ' + description
    return result
