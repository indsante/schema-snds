import os
from typing import List

from tableschema import Schema

from src.constants import TABLESCHEMA_DIR


def get_all_schema() -> List[Schema]:
    return [Schema(schema_path) for schema_path in get_all_schema_path()]


def get_all_schema_path() -> List[str]:
    for root, dirs, files in os.walk(TABLESCHEMA_DIR):
        for file in files:
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
