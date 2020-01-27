import logging
import os
import re
from os.path import join as pjoin
from typing import List, Union, Tuple

from tableschema import Schema

from src.constants import SCHEMAS_DIR, NOMENCLATURES_DIR, NO_NOMENCLATURE


def get_all_schema(work_dir) -> List[Schema]:
    return [Schema(schema_path) for schema_path in get_all_schema_path(work_dir)]


def get_all_schema_path(work_dir) -> List[str]:
    schemas_dir = pjoin(work_dir, SCHEMAS_DIR)

    for root, dirs, files in os.walk(schemas_dir):
        dirs.sort()
        for file in sorted(files):
            if not file.endswith('.json'):
                continue
            schema_path = os.path.join(root, file)
            yield schema_path


def get_all_nomenclatures_schema(nomenclatures_dir=NOMENCLATURES_DIR) -> List[Schema]:
    result = []
    for _, schema_path in get_all_nomenclatures_csv_schema_path(nomenclatures_dir):
        schema = Schema(schema_path)
        result.append(schema)
    return result


def get_all_nomenclatures_csv_schema_path(nomenclatures_dir=NOMENCLATURES_DIR) -> List[Tuple[str, str]]:
    for root, dirs, files in os.walk(nomenclatures_dir):
        dirs.sort()
        for file in sorted(files):
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                schema_path = csv_path[:-4] + '.json'
                yield csv_path, schema_path


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


def get_logging_level_value(logging_level):
    logging_level_value = logging._nameToLevel.get(logging_level.upper(), None)
    if logging_level_value is None:
        raise ValueError('Logging level {} is not valid. It should take one of the following values {}'
                         .format(logging_level, list(logging._nameToLevel.keys())))
    return logging_level_value


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


def get_used_nomenclatures(work_dir):
    used_nomenclatures = set()
    for schema in get_all_schema(work_dir):
        for field in schema.fields:
            nomenclature = field.descriptor['nomenclature'].split(':')[0]
            if nomenclature != NO_NOMENCLATURE:
                used_nomenclatures.add(nomenclature)
    return used_nomenclatures


def get_present_nomenclatures(work_dir):
    present_nomenclatures_files = []
    for root, dirs, files in os.walk(pjoin(work_dir, NOMENCLATURES_DIR)):
        present_nomenclatures_files += files
    present_nomenclatures = [re.sub('.csv$', '', nom) for nom in present_nomenclatures_files]
    return present_nomenclatures


if __name__ == '__main__':
    print(list(get_all_nomenclatures_csv_schema_path(NOMENCLATURES_DIR)))
