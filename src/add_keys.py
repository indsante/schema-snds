import os
from tableschema import Schema
from typing import Union, List
import logging
from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR

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
    logging.info("Add primary and foreign key inside DCIRS table schemas")
    for tableschema_filename in os.listdir(DCIRS_SCHMEMA_DIR):
        path = os.path.join(DCIRS_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIRS_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIRS_JOIN_KEY)
        else:
            add_foreign_key(schema, DCIRS_JOIN_KEY, DCIRS_CENTRAL_TABLE, DCIRS_JOIN_KEY)
        schema.save(path, ensure_ascii=False)


def add_dcir_keys_to_table_schema() -> None:
    logging.info("Add primary and foreign key inside DCIR table schemas")
    for tableschema_filename in os.listdir(DCIR_SCHMEMA_DIR):
        path = os.path.join(DCIR_SCHMEMA_DIR, tableschema_filename)
        schema = Schema(path)
        if tableschema_filename == DCIR_CENTRAL_TABLE + '.json':
            add_primary_key(schema, DCIR_JOIN_KEY)
        else:
            add_foreign_key(schema, DCIR_JOIN_KEY, DCIR_CENTRAL_TABLE, DCIR_JOIN_KEY)
        schema.save(path, ensure_ascii=False)
