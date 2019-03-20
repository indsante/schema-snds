import logging
import subprocess

from sqlalchemy.engine import Engine
from tableschema_sql import Storage

from src.byproducts.postgres import get_postgres_engine, does_postgres_accept_connection, wait_for_postgres
from src.utils import get_all_schema

START_POSTGRES_CONTAINER_IN_BACKGROUND = 'docker-compose up -d postgres'
RUN_SCHEMACRAWLER_CONTAINER = 'docker-compose up schemacrawler'
STOP_POSTGRES_CONTAINER = 'docker-compose stop postgres'


def generate_postgresql_tables(engine: Engine) -> None:
    logging.info("Create relational schema in PostgreSQL running in docker container.")
    schemas = get_all_schema()
    storage = Storage(engine=engine)
    storage.create([schema.descriptor['name'] for schema in schemas],
                   [schema.descriptor for schema in schemas],
                   force=True)


def generate_postgresql_tables_within_docker():
    engine = get_postgres_engine()
    if does_postgres_accept_connection(engine):
        generate_postgresql_tables(engine)
        logging.info("You can now create relational diagram with command `{}`"
                     .format(RUN_SCHEMACRAWLER_CONTAINER))
    else:
        logging.warning("PostgreSQL container is not running.")
        logging.warning("You must start PostgreSQL in the background with command `{}` before"
                        .format(START_POSTGRES_CONTAINER_IN_BACKGROUND))


def generate_relational_diagram_from_host(stop_postgres=False):
    logging.info('Starting PostgreSQL via docker-compose')
    subprocess.run(START_POSTGRES_CONTAINER_IN_BACKGROUND.split())

    engine = get_postgres_engine()
    wait_for_postgres(engine)
    drop_all_tables_postgres(engine)

    generate_postgresql_tables(engine)

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
