import logging
import subprocess
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from tableschema_sql import Storage

from src.constants import SCHEMAS
from src.utils import get_all_schema, is_running_in_docker

START_POSTGRES_CONTAINER_IN_BACKGROUND = 'docker-compose up -d postgres'
RUN_SCHEMACRAWLER_CONTAINER = 'docker-compose up schemacrawler'


def generate_relational_diagram():
    if is_running_in_docker():
        logging.info("Generate PostgreSQL tables within Docker")
        generate_postgresql_tables_within_docker()
    else:
        logging.info("Generate relational diagram from host")
        generate_relational_diagram_from_host()


def generate_postgresql_tables_within_docker():
    engine = get_postgres_engine()
    if does_postgres_accept_connection(engine):
        generate_postgresql_tables(engine)
        logging.info("Vous pouvez maintenant créer un diagramme relationnel avec la commande `{}`"
                     .format(RUN_SCHEMACRAWLER_CONTAINER))
    else:
        logging.warning("Le containeur PostgreSQL n'est pas démarré.")
        logging.warning("Vous devez d'abord le démarrer en arrière plan avec la commande `{}`"
                        .format(START_POSTGRES_CONTAINER_IN_BACKGROUND))


def generate_postgresql_tables(engine: Engine) -> None:
    logging.info("Creation des tables correspondant au schéma relationnel du SNDS, "
                 "dans la base PostgreSQL exposée depuis un containeur Docker.")
    schemas = get_all_schema(SCHEMAS)
    schemas = [schema for schema in schemas if schema.descriptor["produit"] != "PMSI SSR"]
    storage = Storage(engine=engine)
    storage.create([schema.descriptor['name'] for schema in schemas],
                   [schema.descriptor for schema in schemas],
                   force=True)


def generate_relational_diagram_from_host():
    logging.info('Démarrage de PostgreSQL avec docker-compose')
    subprocess.run(START_POSTGRES_CONTAINER_IN_BACKGROUND.split())

    engine = get_postgres_engine()
    wait_for_postgres(engine)
    drop_all_tables_postgres(engine)

    generate_postgresql_tables(engine)

    logging.info('Lancement de schemacrawler avec docker-compose, pour créer un diagramme relationnel')
    subprocess.run(RUN_SCHEMACRAWLER_CONTAINER.split())


def drop_all_tables_postgres(engine):
    """ This allow a much faster table creation. """
    engine.execute("""
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;""")


def get_postgres_engine() -> Engine:
    postgres_host = 'postgres' if is_running_in_docker() else 'localhost'
    return create_engine('postgresql://postgres@{}:5432/postgres'.format(postgres_host))


def wait_for_postgres(engine: Engine, max_waiting_time: int = 10):
    logging.info('Waiting until PostgreSQL accept connexions')
    for i in range(max_waiting_time):
        if does_postgres_accept_connection(engine):
            logging.info('PostgreSQL is ready to accept connexions')
            return
        logging.info('PostgreSQL is not ready to accept connexions, waiting {} more seconds'
                     .format(max_waiting_time - i))
        sleep(1)

    engine.connect()  # Raise exception


def does_postgres_accept_connection(engine: Engine) -> bool:
    """ Test if the target PostgreSQL database accept connexions
    """
    try:
        engine.connect()
    except OperationalError:
        return False
    else:
        return True


if __name__ == '__main__':
    generate_relational_diagram()
