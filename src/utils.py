import os
from typing import List

from tableschema import Schema

from src.constants import TABLESCHEMA_DIR


def get_all_schema(skipped_schemas_directory: List[str] = None) -> List[Schema]:
    schemas = list()
    for schema in os.listdir(TABLESCHEMA_DIR):
        schemas_directory = TABLESCHEMA_DIR + '/' + schema
        if skipped_schemas_directory is None or schemas_directory not in skipped_schemas_directory:
            schemas += get_schemas_in_directory(schemas_directory)
    return schemas


def get_schemas_in_directory(schemas_directory: str) -> List[Schema]:
    schemas = list()
    for table_schema in os.listdir(schemas_directory):
        path = os.path.join(schemas_directory, table_schema)
        schemas.append(Schema(path))
    return schemas


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
