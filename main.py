from src.add_keys import add_dcirs_key_to_schemas
from src.convert import convert_schemas_to_markdown, create_sql_schema_from_docker, create_relational_diagram_from_host
from src.reformat_snds_dico import snds_dico_to_schemas
from src.utils import is_running_in_docker

snds_dico_to_schemas()
add_dcirs_key_to_schemas()
convert_schemas_to_markdown()

if is_running_in_docker():
    create_sql_schema_from_docker()
else:
    create_relational_diagram_from_host()
