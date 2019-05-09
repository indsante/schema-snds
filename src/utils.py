import logging
import os
import shutil
from typing import List, Union

from tableschema import Schema

from src.constants import DATA_DIR, TABLESCHEMA_DIR, TABLESCHEMA


def reset_data_directory():
    logging.info("Reset data directory")
    for folder in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder)
        if folder == TABLESCHEMA:
            continue
        if not os.path.isdir(folder_path):
            logging.warning("'{}' is not a folder. We do not delete it in data directory.".format(folder_path))
            continue
        logging.info("Delete folder '{}'".format(folder_path))
        shutil.rmtree(folder_path, ignore_errors=True)


def get_all_schema() -> List[Schema]:
    return [Schema(schema_path) for schema_path in get_all_schema_path()]


def get_all_schema_path() -> List[str]:
    for root, dirs, files in os.walk(TABLESCHEMA_DIR):
        dirs.sort()
        for file in sorted(files):
            schema_path = os.path.join(root, file)
            yield schema_path


def is_running_in_docker():
    proc_cgroup_file = os.path.join('/', 'proc', 'self', 'cgroup')
    if not os.path.exists(proc_cgroup_file):
        return False

    with open(proc_cgroup_file, 'r') as f:
        for line in f.readlines():
            t = line.split('/')
            if len(t) < 2:
                continue
            if t[1] == 'docker':
                return True

    return False


# Not used currently
def add_primary_key(schema: Schema, primary_key: Union[str, List[str]]) -> None:
    schema.descriptor['primaryKey'] = primary_key
    schema.commit()


def add_foreign_key(schema: Schema, fields: Union[str, List[str]], referenced_table: str,
                    referenced_fields: Union[str, List[str]], description: str = None) -> None:
    if 'foreignKeys' not in schema.descriptor:
        schema.descriptor['foreignKeys'] = list()

    foreign_key_descriptor = {
        'fields': fields,
        'reference': {
            'resource': referenced_table,
            'fields': referenced_fields
        },
    }
    if description:
        foreign_key_descriptor['description'] = description
    schema.descriptor['foreignKeys'].append(foreign_key_descriptor)
    schema.commit(strict=True)