import os
from typing import List

from tableschema import Schema


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
