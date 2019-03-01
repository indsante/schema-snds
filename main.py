from src.add_keys import add_dcirs_keys, add_dcir_keys, add_beneficiary_central_table_DCIR_keys, \
    add_beneficiary_central_table_DCIRS_keys, add_DCIR_beneficiary_link, add_DCIRS_beneficiary_link, add_DA_PRA_R_keys
from src.convert import table_schema_to_markdown, table_schema_to_sql_within_docker, \
    table_schema_to_relational_diagram_from_host, generate_table_sidebar
from src.reformat_snds_dico import dico_snds_to_table_schema
from src.utils import is_running_in_docker

dico_snds_to_table_schema()
add_DA_PRA_R_keys()
add_dcirs_keys()
add_dcir_keys()
add_beneficiary_central_table_DCIR_keys()
add_beneficiary_central_table_DCIRS_keys()
add_DCIR_beneficiary_link()
add_DCIRS_beneficiary_link()
table_schema_to_markdown()
generate_table_sidebar()

if is_running_in_docker():
    table_schema_to_sql_within_docker()
else:
    table_schema_to_relational_diagram_from_host()
