import logging
import os
import shutil
from typing import List

from tableschema import Schema

from src.constants import DATA_DIR, SOURCES, TABLESCHEMA_DIR


def reset_data_directory():
    logging.info("Reset data directory")
    for folder in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder)
        if folder == SOURCES:
            continue
        if not os.path.isdir(folder_path):
            logging.warning("'{}' is not a folder. We do not delete it.".format(folder_path))
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
