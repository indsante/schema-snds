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

# +
import json
import pandas as pd
import re
import os 
import logging


import sys
sys.path.append('../')
#from src.constants import SCHEMAS_DIR
from src.utils import get_all_schema
from tableschema import Schema

from typing import List
# -

path2schemas = '../schemas/'
path2test_schemas = '../tests/schemas/'
path2tables_history = 'tables_history.csv'
path2variables_history = 'variables_history.csv'

DEFAULT_CREATED = ''
DEFAULT_DELETED = ''
DEFAULT_MISSINGS = []

# +
def add_tables_history(
    schemas_dir: str, 
    tables_history_filename: str,
    save: bool = True) -> List[Schema]:
    """
    Add tables history to schemas 
    """
    new_schemas = []
    schemas = get_all_schema(schemas_dir=schemas_dir)
    tables_history_df = pd.read_csv(tables_history_filename)
    ## harmonize the unkown year part in the table names (XX for kwikly != aa_nn for the schema)
    tables_history_df['var'] = tables_history_df['var'].apply(lambda x: re.sub('XX', 'aa_nn', x))
    for schema in schemas:
        table_name = schema.descriptor['name']
        logging.info("Ajout de l'historique pour la table '{}'".format(table_name))
        table_produit = schema.descriptor['produit']
        table_history = tables_history_df.loc[tables_history_df['var'] == table_name, :]
        if len(table_history) == 0:
            table_history_dic = {
            'dateCreated': DEFAULT_CREATED, 
            'dateDeleted': DEFAULT_DELETED,
            'dateMissing': DEFAULT_MISSINGS}
        else:
            if pd.isna(table_history['missings'].values[0]):
                dateMissing = DEFAULT_MISSINGS
            else:
                dateMissing = str(table_history['missings'].values[0]).split('_')
            table_history_dic = {
                'dateCreated': str(table_history['created'].values[0]), 
                'dateDeleted': str(table_history['deleted'].values[0]),
                'dateMissing': dateMissing}
        schema.descriptor['history'] = table_history_dic
        schema.commit()
        if save:
            if re.search('PMSI', table_produit) is not None:
                save_path = os.path.join(schemas_dir, 'PMSI', table_produit, table_name)+'.json'
            else:
                save_path = os.path.join(schemas_dir, table_produit, table_name)+'.json'
            schema.save(save_path, ensure_ascii=False)
        new_schemas.append(schema)
    return new_schemas

def add_variables_history(
    schemas_dir: str, 
    variables_history_filename: str,
    save: bool = True,
    verbose=False) -> List[Schema]:
    """
    Add variables history to schemas 
    """
    new_schemas = []
    schemas = get_all_schema(schemas_dir=schemas_dir)
    variables_history_df = pd.read_csv(variables_history_filename)
    ## harmonize the unkown year part in the table names (XX for kwikly != aa_nn for the schema)
    variables_history_df['table'] = variables_history_df['table'].apply(lambda x: re.sub('XX', 'aa_nn', x))
    for schema in schemas:
        table_name = schema.descriptor['name']
        table_produit = schema.descriptor['produit']
        table_history = variables_history_df.loc[variables_history_df['table'] == table_name, :]
        logging.info("-----\n Ajout de l'historique pour la table '{}'".format(table_name))
        for var_name in schema.field_names:
            if verbose:
                logging.info("Ajout de l'historique pour la variable '{}'".format(var_name))
            var_history = table_history.loc[table_history['var'] == var_name, :]
            if len(var_history) == 0:
                var_history_dic = {
                    'dateCreated': DEFAULT_CREATED, 
                    'dateDeleted': DEFAULT_DELETED,
                    'dateMissing': DEFAULT_MISSINGS}
            else:
                if pd.isna(var_history['missings'].values[0]):
                    dateMissing = DEFAULT_MISSINGS
                else:
                    dateMissing = str(var_history['missings'].values[0]).split('_')
                var_history_dic = {
                    'dateCreated': str(var_history['created'].values[0]), 
                    'dateDeleted': str(var_history['deleted'].values[0]),
                    'dateMissing': dateMissing}
            schema.update_field(var_name, var_history_dic)
        schema.commit()
        new_schemas.append(schema)
        if save:
            if re.search('PMSI', table_produit) is not None:
                save_path = os.path.join(schemas_dir, 'PMSI', table_produit, table_name)+'.json'
            else:
                save_path = os.path.join(schemas_dir, table_produit, table_name)+'.json'
            schema.save(save_path, ensure_ascii=False)
    return new_schemas


def rm_tables_fields(
    schemas_dir: str, 
    fields_to_rm: List[str],
    save: bool = True,
    verbose: bool = False) -> List[Schema]:
    """
    Remove some fields from the schemas
    """
    new_schemas = []
    schemas = get_all_schema(schemas_dir=schemas_dir)
    for schema in schemas:
        table_name = schema.descriptor['name']
        if verbose:
            logging.info("Suppresion des champs {} pour la table '{}'".format(fields_to_rm, table_name))
        table_produit = schema.descriptor['produit']
        
        for f in fields_to_rm:
            schema.descriptor.pop(f, 0)
        schema.commit()
        if save:
            if re.search('PMSI', table_produit) is not None:
                save_path = os.path.join(schemas_dir, 'PMSI', table_produit, table_name)+'.json'
            else:
                save_path = os.path.join(schemas_dir, table_produit, table_name)+'.json'
            schema.save(save_path, ensure_ascii=False)
        new_schemas.append(schema)
    return new_schemas

def rm_variables_fields(
    schemas_dir: str, 
    fields_to_rm: List[str],
    save: bool = True,
    verbose=False) -> List[Schema]:
    """
    Remove some fields from the schema
    """
    new_schemas = []
    schemas = get_all_schema(schemas_dir=schemas_dir)
    
    for schema in schemas:
        table_name = schema.descriptor['name']
        table_produit = schema.descriptor['produit']
        if verbose:
            logging.info("-----\n Suppresion des champs {} pour la table '{}'".format(fields_to_rm, table_name))
        for i, var_name in enumerate(schema.field_names):
            #if verbose:
            #    logging.info("Suppression des champs pour la variable '{}'".format(var_name))
            for f in fields_to_rm:
                schema.descriptor['fields'][i].pop(f, 0)
        schema.commit()
        new_schemas.append(schema)
        if save:
            if re.search('PMSI', table_produit) is not None:
                save_path = os.path.join(schemas_dir, 'PMSI', table_produit, table_name)+'.json'
            else:
                save_path = os.path.join(schemas_dir, table_produit, table_name)+'.json'
            schema.save(save_path, ensure_ascii=False)
    return new_schemas
# -

# # src schemas history addition

table_schemas = add_tables_history(path2schemas, 'tables_history.csv', save=True)
var_history = add_variables_history(path2schemas, 'variables_history.csv', save=True)

# # test schemas history addition

table_schemas = add_tables_history(path2test_schemas, 'tables_history.csv', save=True)
var_history = add_variables_history(path2test_schemas, 'variables_history.csv', save=True)

# ## Remove fields from schemas

table_schemas = rm_tables_fields(path2schemas, ['history'], save=True)
variables_history = rm_variables_fields(path2schemas, ['dateDeleted', 'dateCreated', 'dateMissing'])

# ## Remove fields from test schemas

table_schemas = rm_tables_fields(path2test_schemas, ['history'], save=True)
variables_history = rm_variables_fields(path2test_schemas, ['dateDeleted', 'dateCreated', 'dateMissing'])


