import logging
import os
import subprocess

from sqlalchemy.engine.base import Engine
from table_schema_to_markdown import convert_source
from tableschema_sql import Storage

from src.constants import DCIRS_SCHMEMA_DIR, DCIR_SCHMEMA_DIR, MAIN_SCHEMA_DIR, BENEFICIARY_SCHEMA_DIR, \
    DECES_SCHEMA_DIR, DCIR_DCIRS_SCHEMA_DIR
from src.database import get_postgres_engine, does_postgres_accept_connection, wait_for_postgres
from src.utils import get_schemas_in_directory

START_POSTGRES_CONTAINER_IN_BACKGROUND = 'docker-compose up -d postgres'
RUN_SCHEMACRAWLER_CONTAINER = 'docker-compose up schemacrawler'
STOP_POSTGRES_CONTAINER = 'docker-compose stop postgres'


def table_schema_to_markdown() -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for root, dirs, files in os.walk(MAIN_SCHEMA_DIR):
        for file in files:
            schema_path = os.path.join(root, file)
            markdown_path = schema_path.replace('tableschema', 'markdown').replace('.json', '.md')
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, 'a', encoding='utf8') as out:
                convert_source(schema_path, out)


def table_schema_directory_to_sql(schemas_directory: str, engine: Engine) -> None:
    logging.info("Read schemas from '{}' and create them in SQL engine".format(schemas_directory))
    schemas = get_schemas_in_directory(schemas_directory)
    storage = Storage(engine=engine)
    storage.create([schema.descriptor['title'] for schema in schemas],
                   [schema.descriptor for schema in schemas],
                   force=True)


def table_schema_to_sql(engine):
    table_schema_directory_to_sql(DCIRS_SCHMEMA_DIR, engine)
    table_schema_directory_to_sql(DCIR_SCHMEMA_DIR, engine)
    table_schema_directory_to_sql(BENEFICIARY_SCHEMA_DIR, engine)
    table_schema_directory_to_sql(DECES_SCHEMA_DIR, engine)
    table_schema_directory_to_sql(DCIR_DCIRS_SCHEMA_DIR, engine)


def table_schema_to_sql_within_docker():
    logging.info("Create relational schema in PostgreSQL running in docker container.")
    engine = get_postgres_engine()
    if does_postgres_accept_connection(engine):
        table_schema_to_sql(engine)
        logging.info("You can now create relational diagram with command `{}`"
                     .format(RUN_SCHEMACRAWLER_CONTAINER))
    else:
        logging.warning("PostgreSQL container is not running.")
        logging.warning("You must start PostgreSQL in the background with command `{}` before"
                        .format(START_POSTGRES_CONTAINER_IN_BACKGROUND))


def table_schema_to_relational_diagram_from_host():
    logging.info('Starting PostgreSQL via docker-compose')
    subprocess.run(START_POSTGRES_CONTAINER_IN_BACKGROUND.split())

    engine = get_postgres_engine()
    wait_for_postgres(engine)

    table_schema_to_sql(engine)

    logging.info('Running schemacrawler via docker-compose to create diagram from PostgreSQL')
    subprocess.run(RUN_SCHEMACRAWLER_CONTAINER.split())

    logging.info('Stopping PostgreSQL via docker-compose')
    subprocess.run(STOP_POSTGRES_CONTAINER.split())
