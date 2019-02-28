import logging
import os
from typing import Union, List

from tableschema import Schema

from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR, DCIR_DCIRS_SCHEMA_DIR, BENEFICIARY_SCHEMA_DIR, \
    DECES_SCHEMA_DIR

DCIRS_CENTRAL_TABLE = 'NS_PRS_F'
DCIRS_JOIN_KEY = ['CLE_DCI_JNT']

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
BENEFICIARY_DCIR_EXCLUDED_TABLES = 'DA_PRA_R.json'

BENEFICIARY_CENTRAL_TABLE_DCIRS = 'IR_IBA_R'
BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY = ['BEN_IDT_ANO']
BENEFICIARY_DCIRS_EXCLUDED_TABLES = [
    'DA_PRA_R.json',
    'IR_IMB_R.json',
]

DECES_JOIN_KEY = ['BEN_IDT_ANO']


def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit()


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


def add_dcirs_keys() -> None:
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


def add_dcir_keys() -> None:
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


def update_descriptor_field(schema: Schema, field_name: str, update_dict: dict) -> bool:
    fields = schema.descriptor['fields']
    for field in fields:
        if field['name'] == field_name:
            field.update(update_dict)
            schema.commit()
            return True
    return False


def add_beneficiary_central_table_DCIR_keys() -> None:
    """
    Ajout des liens entre la table réferentiel beneficiaire du DCIR (IR_BEN_R) et les tables associées beneficiaires

    Toutes les tables DCIR_DCIRS sont des tables associées aux bénéficiaires sauf la table DA_PRA_R qui concerne
    les Professionnels de Santé.
    """
    logging.info("Ajout des liens entre la table réferentiel beneficiaire du DCIR IR_BEN_R et "
                 "ses tables associés beneficiaires dans le table schema")
    path_beneficiary_dcir = os.path.join(BENEFICIARY_SCHEMA_DIR, BENEFICIARY_CENTRAL_TABLE_DCIR + '.json')
    schema_beneficiary_dcir = Schema(path_beneficiary_dcir)
    update_descriptor_field(schema_beneficiary_dcir, 'BEN_IDT_ANO', {"constraints": {"unique": True}})
    add_primary_key(schema_beneficiary_dcir, BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY)
    add_foreign_key(schema_beneficiary_dcir, BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY, BENEFICIARY_CENTRAL_TABLE_DCIRS,
                    BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY)
    schema_beneficiary_dcir.save(path_beneficiary_dcir, ensure_ascii=False)
    add_associated_beneficiary_tables_foreign_keys(BENEFICIARY_CENTRAL_TABLE_DCIR,
                                                   BENEFICIARY_DCIR_EXCLUDED_TABLES,
                                                   BENEFICIARY_CENTRAL_TABLE_DCIR_JOIN_KEY
                                                   )
    add_deces_foreign_keys_with_beneficiary(BENEFICIARY_CENTRAL_TABLE_DCIR)


def add_beneficiary_central_table_DCIRS_keys() -> None:
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
    add_associated_beneficiary_tables_foreign_keys(BENEFICIARY_CENTRAL_TABLE_DCIRS,
                                                   BENEFICIARY_DCIRS_EXCLUDED_TABLES,
                                                   BENEFICIARY_CENTRAL_TABLE_DCIRS_JOIN_KEY
                                                   )
    add_deces_foreign_keys_with_beneficiary(BENEFICIARY_CENTRAL_TABLE_DCIRS)


def add_associated_beneficiary_tables_foreign_keys(beneficiary_central_table: str,
                                                   dcirs_dcir_excluded_tables: Union[str, List[str]],
                                                   beneficiary_central_table_join_key: Union[str, List[str]]) -> None:
    """
    Ajout des clefs étrangères entre les tables associées bénéficaires et une des tables réferentiel beneficiaire

    Les tables référentiel bénéficiaires sont le DCIR (IR_BEN_R) ou DCIRS (IR_IBA_R).
    Utilisation de la clef de jointure propre à chacune des tables référentiels beneficiaires.
    Exclusion de tables à ne pas considérer dans le dossier DCIR/DCIRS pour des raisons expliquées le cas échéant
    """
    for tableschema_filename in os.listdir(DCIR_DCIRS_SCHEMA_DIR):
        path = os.path.join(DCIR_DCIRS_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename not in dcirs_dcir_excluded_tables:
            add_foreign_key(schema, beneficiary_central_table_join_key, beneficiary_central_table,
                            beneficiary_central_table_join_key)
        schema.save(path, ensure_ascii=False)


def add_deces_foreign_keys_with_beneficiary(beneficiary_central_table: str) -> None:
    """
    Ajout des liens entre une des tables beneficiaires et les tables dates et causes de décés.

    Une seule clef de jointure possible pour l'ensemble des tables bénéficiaires
    """
    for tableschema_filename in os.listdir(DECES_SCHEMA_DIR):
        path = os.path.join(DECES_SCHEMA_DIR, tableschema_filename)
        schema = Schema(path)
        add_foreign_key(schema, DECES_JOIN_KEY, beneficiary_central_table, DECES_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
