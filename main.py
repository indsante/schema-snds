import logging

from src.add_keys import add_dcirs_keys
from src.convert import convert_schemas_to_markdown, create_schemas_in_sql_storage, create_diagram_from_postgresql
from src.database import get_postgres_engine, start_postgres, stop_postgres
from src.reformat_snds_dico import get_dico_snds_variables, write_all_schema

DICO_SNDS_PATH = '../dico-snds'
MAIN_SCHEMA_DIR = 'data/tableschema'
DCIRS_SCHMEMA_DIR = 'data/tableschema/DCIRS'

df = get_dico_snds_variables(DICO_SNDS_PATH)

logging.info("Write reformated snds-dico information")
df.to_csv('data/variables.csv', index=False)

write_all_schema(df, MAIN_SCHEMA_DIR)

add_dcirs_keys(DCIRS_SCHMEMA_DIR)

convert_schemas_to_markdown(MAIN_SCHEMA_DIR)

start_postgres()
engine = get_postgres_engine()
# engine = get_sqlite_engine()
create_schemas_in_sql_storage(DCIRS_SCHMEMA_DIR, engine)
create_diagram_from_postgresql()
stop_postgres()
