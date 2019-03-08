from src.add_keys import add_all_keys_to_tableschema
from src.convert import table_schema_to_markdown, table_schema_to_sql_within_docker, \
    table_schema_to_relational_diagram_from_host, generate_table_sidebar
from src.dico_snds import table_schema_to_app_dico
from src.reformat_snds_dico import dico_snds_to_table_schema
from src.utils import is_running_in_docker

dico_snds_to_table_schema()
add_all_keys_to_tableschema()
table_schema_to_markdown()
table_schema_to_app_dico()
generate_table_sidebar()

if is_running_in_docker():
    table_schema_to_sql_within_docker()
else:
    table_schema_to_relational_diagram_from_host()
