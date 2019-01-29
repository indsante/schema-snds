import logging
import subprocess
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError


def get_sqlite_engine() -> Engine:
    return create_engine('sqlite:///notebooks/ignore/db.sql')


def get_postgres_engine() -> Engine:
    return create_engine('postgresql://postgres@localhost:5432/postgres')


def start_postgres() -> None:
    logging.info('Starting PostgreSQL via docker-compose')
    subprocess.run('docker-compose up -d postgres'.split())
    engine = get_postgres_engine()
    wait_for_postgres(engine)


def stop_postgres() -> None:
    logging.info('Stopping PostgreSQL via docker-compose')
    subprocess.run('docker-compose stop postgres'.split())


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
