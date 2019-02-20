import os
from tableschema import Schema
from typing import Union, List
import logging
from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR, DCIR_DCIRS_SCHEMA_DIR, BENEFICIARY_SCHEMA_DIR

DCIRS_CENTRAL_TABLE = 'NS_PRS_F'
DCIRS_JOIN_KEY = 'CLE_DCI_JNT'

DCIR_CENTRAL_TABLE = 'ER_PRS_F'
DCIR_JOIN_KEY = [
    'DCT_ORD_NUM',
    'FLX_DIS_DTD',
    'FLX_EMT_NUM',
    'FLX_EMT_ORD',
    'FLX_EMT_TYP',
    'FLX_TRT_DTD',
    'ORG_CLE_NUM',
    'PRS_ORD_NUM',
    'REM_TYP_AFF',
]

BENEFICIARY_CENTRAL_TABLE_DCIR = 'IR_BEN_R'
BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY = [
    'BEN_NIR_PSA',
    'BEN_RNG_GEM',
]

BENEFICIARY_CENTRAL_TABLE_DCIRS = 'IR_IBA_R'
BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY = 'BEN_IDT_ANO'


def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit(strict=True)


def add_foreign_key(schema: Schema, fields: Union[str, List[str]], referenced_table: str,
                    referenced_fields: Union[str, List[str]]) -> None:
    if 'foreignKeys' not in schema.descriptor:
        schema.descriptor['foreignKeys'] = list()

    foreign_key_descriptor = {
        'fields': fields,
        'reference': {
            'resource': referenced_table,
            'fields': referenced_fields
        }
    }

    schema.descriptor['foreignKeys'].append(foreign_key_descriptor)
    schema.commit(strict=True)


def add_dcirs_keys_to_table_schema() -> None:
    """ Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées
    """
    logging.info("Ajout des liens entre la table centrale prestation du DCIRS et ses tables associées"
                 " dans le table schema")
    for tableschema_filename in os.listdir(DCIRS_SCHMEMA_DIR):
        path = os.path.join(DCIRS_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIRS_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIRS_JOIN_KEY)
        else:
            add_foreign_key(schema, DCIRS_JOIN_KEY, DCIRS_CENTRAL_TABLE, DCIRS_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_dcir_keys_to_table_schema() -> None:
    """ Ajout des liens entre la table centrale prestation du DCIR et ses tables associées
    """
    logging.info("Ajout des liens entre la table centrale prestation du DCIR et ses tables associées"
                 " dans le table schema")
    for tableschema_filename in os.listdir(DCIR_SCHMEMA_DIR):
        path = os.path.join(DCIR_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIR_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIR_JOIN_KEY)
        else:
            add_foreign_key(schema, DCIR_JOIN_KEY, DCIR_CENTRAL_TABLE, DCIR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_beneficiary_central_table_DCIR_keys_with_associated_beneficiary_tables_to_table_schema() -> None:
    """
    Ajout des liens entre la table réferentiel beneficiaire du DCIR (IR_BEN_R) et les tables associées beneficiaires

    Toutes les tables DCIR_DCIRS sont des tables associées aux bénéficiaires sauf la table DA_PRA_R qui concerne
    les Professionnels de Santé.
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIR IR_BEN_R et "
                 "ses tables associés beneficiaires dans le table schema")
    path_beneficiary_dcir = os.path.join(BENEFICIARY_SCHEMA_DIR, BENEFICIARY_CENTRAL_TABLE_DCIR + '.json')
    schema_beneficiary_dcir = Schema(path_beneficiary_dcir)
    add_primary_key(schema_beneficiary_dcir, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
    schema_beneficiary_dcir.save(path_beneficiary_dcir, ensure_ascii=False)
    for tableschema_filename in os.listdir(DCIR_DCIRS_SCHEMA_DIR):
        path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename != 'DA_PRA_R.json':
            add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIR,
                            BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_beneficiary_central_table_DCIRS_keys_with_associated_beneficiary_tables_to_table_schema() -> None:
    """
    Ajout des liens entre la table réferentiel beneficiaire du DCIRS (IR_IBA_R) et les tables associées beneficiaires

    Toutes les tables DCIR_DCIRS sont des tables associées aux bénéficiaires sauf la table DA_PRA_R qui concerne
    les Professionnels de Santé.
    La table IR_IMB_R (Référentiel médicalisé - historique des exonérations) ne peut pas être reliée au DCIRS car elle
    n'a pas la clé de jointure (BEN_IDT_ANO)
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIRS IR_IBA_R et ses tables associés "
                 "beneficiaires dans le table schema")
    path_beneficiary_dcirs = os.path.join(BENEFICIARY_SCHEMA_DIR, BENEFICIARY_CENTRAL_TABLE_DCIRS + '.json')
    schema_beneficiary_dcirs = Schema(path_beneficiary_dcirs)
    add_primary_key(schema_beneficiary_dcirs, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
    schema_beneficiary_dcirs.save(path_beneficiary_dcirs, ensure_ascii=False)
    for tableschema_filename in os.listdir(DCIR_DCIRS_SCHEMA_DIR):
        path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename not in ['DA_PRA_R.json', 'IR_IMB_R.json']:
            add_foreign_key(schema, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIRS,
                            BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
