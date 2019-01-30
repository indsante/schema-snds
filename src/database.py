import logging
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError

from src.utils import is_running_in_docker


def get_sqlite_engine() -> Engine:
    return create_engine('sqlite:///notebooks/ignore/db.sql')


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
