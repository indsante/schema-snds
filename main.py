from src.build_tableschema.add_keys import add_all_keys_to_tableschema
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_postgresql_tables_within_docker, \
    generate_relational_diagram_from_host
from src.byproducts.dico_snds import generate_dico_snds
from src.build_tableschema.reformat_snds_dico import build_tableschema_from_dico_snds
from src.utils import is_running_in_docker

# Building tableschema
build_tableschema_from_dico_snds()
add_all_keys_to_tableschema()

# Generating tableschema byproducts
generate_documentation_snds()
generate_dico_snds()

if is_running_in_docker():
    generate_postgresql_tables_within_docker()
else:
    generate_relational_diagram_from_host()
