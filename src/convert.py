import logging
import os

from sqlalchemy.engine.base import Engine
from table_schema_to_markdown import convert_source
from tableschema import Schema
from tableschema_sql import Storage


def convert_schemas_to_markdown(tableschema_dir: str) -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for root, dirs, files in os.walk(tableschema_dir):
        for file in files:
            schema_path = os.path.join(root, file)
            markdown_path = schema_path.replace('tableschema', 'markdown').replace('.json', '.md')
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, 'a', encoding='utf8') as out:
                convert_source(schema_path, out)


def create_schema_in_storage(schemas_directory: str, engine: Engine) -> None:
    logging.info("Read schemas from '{}' and create them in SQL engine".format(schemas_directory))
    schemas = list()
    for table_schema in os.listdir(schemas_directory):
        path = os.path.join(schemas_directory, table_schema)
        schemas.append(Schema(path))

    storage = Storage(engine=engine)
    storage.create([schema.descriptor['title'] for schema in schemas],
                   [schema.descriptor for schema in schemas],
                   force=True)
