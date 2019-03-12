import json
import logging
import os
import subprocess

from sqlalchemy.engine.base import Engine
from table_schema_to_markdown import convert_source
from tableschema_sql import Storage

from src.constants import MAIN_SCHEMA_DIR, TABLES_SIDEBAR_JS_PATH
from src.database import get_postgres_engine, does_postgres_accept_connection, wait_for_postgres
from src.utils import get_all_schema

START_POSTGRES_CONTAINER_IN_BACKGROUND = 'docker-compose up -d postgres'
RUN_SCHEMACRAWLER_CONTAINER = 'docker-compose up schemacrawler'
STOP_POSTGRES_CONTAINER = 'docker-compose stop postgres'

SKIPPED_SCHEMA_DIRS = []


def table_schema_to_markdown() -> None:
    logging.getLogger('table_schema_to_markdown').setLevel(logging.WARNING)
    logging.info("Convert schemas to Markdown")
    for root, dirs, files in os.walk(MAIN_SCHEMA_DIR):
        for file in files:
            schema_path = os.path.join(root, file)
            markdown_path = schema_path.replace('tableschema', 'markdown').replace('.json', '.md')
            os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
            with open(markdown_path, 'w', encoding='utf8') as out:
                convert_source(schema_path, out)


def generate_table_sidebar() -> None:
    logging.info("Generate 'table_sidebar.js' for VuePress documentation")
    sidebar = ['']
    for product_folder in os.listdir(MAIN_SCHEMA_DIR):
        table_schemas = os.listdir(os.path.join(MAIN_SCHEMA_DIR, product_folder))
        sidebar.append({
            'title': product_folder,
            'children': [product_folder + '/' + table[:-5] for table in table_schemas]
        })

    with open(TABLES_SIDEBAR_JS_PATH, 'w', encoding='utf8') as f:
        f.write('module.exports =')
        json.dump(sidebar, f, ensure_ascii=False, indent=4)
        f.write(';')


def table_schema_all_directories_to_sql(engine: Engine) -> None:
    logging.info("Create relational schema in PostgreSQL running in docker container.")
    schemas = get_all_schema(SKIPPED_SCHEMA_DIRS)
    storage = Storage(engine=engine)
    storage.create([schema.descriptor['name'] for schema in schemas],
                   [schema.descriptor for schema in schemas],
                   force=True)


def table_schema_to_sql_within_docker():
    engine = get_postgres_engine()
    if does_postgres_accept_connection(engine):
        table_schema_all_directories_to_sql(engine)
        logging.info("You can now create relational diagram with command `{}`"
                     .format(RUN_SCHEMACRAWLER_CONTAINER))
    else:
        logging.warning("PostgreSQL container is not running.")
        logging.warning("You must start PostgreSQL in the background with command `{}` before"
                        .format(START_POSTGRES_CONTAINER_IN_BACKGROUND))


def table_schema_to_relational_diagram_from_host(stop_postgres=False):
    logging.info('Starting PostgreSQL via docker-compose')
    subprocess.run(START_POSTGRES_CONTAINER_IN_BACKGROUND.split())

    engine = get_postgres_engine()
    wait_for_postgres(engine)
    drop_all_tables_postgres(engine)

    table_schema_all_directories_to_sql(engine)

    logging.info('Running schemacrawler via docker-compose to create diagram from PostgreSQL')
    subprocess.run(RUN_SCHEMACRAWLER_CONTAINER.split())

    if stop_postgres:
        logging.info('Stopping PostgreSQL via docker-compose')
        subprocess.run(STOP_POSTGRES_CONTAINER.split())


def drop_all_tables_postgres(engine):
    """ This allow a much faster table creation. """
    engine.execute("""
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;""")
