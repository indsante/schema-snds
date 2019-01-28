import os
from typing import List

from tableschema import Schema


def get_schemas_in_directory(schemas_directory: str) -> List[Schema]:
    schemas = list()
    for table_schema in os.listdir(schemas_directory):
        path = os.path.join(schemas_directory, table_schema)
        schemas.append(Schema(path))

    return schemas
