import os
from tableschema import Schema
from typing import Union, List
import logging


def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit(strict=True)


def add_foreign_key(schema: Schema, fields, referenced_table, referenced_fields) -> None:
    if 'foreignKeys' not in schema.descriptor:
        schema.descriptor['foreignKeys'] = list()

    foreign_key_descriptor = {
        'fields': fields,
        'reference': {
            'resource': referenced_table,
            'fields': referenced_fields}
    }

    schema.descriptor['foreignKeys'].append(foreign_key_descriptor)
    schema.commit(strict=True)


def add_dcirs_keys(dcirs_directory: str) -> None:
    logging.info("Add primary and foreign key inside DCIRS table schemas")
    for tableschema in os.listdir(dcirs_directory):
        path = os.path.join(dcirs_directory, tableschema)
        schema = Schema(path)
        if tableschema == 'NS_PRS_F.json':
            add_primary_key(schema, 'CLE_DCI_JNT')
        else:
            add_foreign_key(schema, 'CLE_DCI_JNT', 'NS_PRS_F', 'CLE_DCI_JNT')
        schema.save(path, ensure_ascii=False)
