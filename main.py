import logging

from src.add_keys import add_dcirs_keys
from src.convert import convert_schemas_to_markdown
from src.reformat_snds_dico import get_dico_snds_variables, write_all_schema

DICO_SNDS_PATH = '../dico-snds'
TABLESCHEMA_DIR = 'data/tableschema'

df = get_dico_snds_variables(DICO_SNDS_PATH)

logging.info("Write reformated snds-dico information")
df.to_csv('data/variables.csv', index=False)

write_all_schema(df, TABLESCHEMA_DIR)

add_dcirs_keys()

convert_schemas_to_markdown(TABLESCHEMA_DIR)
