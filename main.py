from src.build_tableschema.add_keys import add_primary_and_foreign_keys_to_tableschema
from src.build_tableschema.reformat_snds_dico import build_tableschema_from_dico_snds
from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_relational_diagram
from src.utils import reset_data_directory

if __name__ == '__main__':
    reset_data_directory()

    # Building tableschema
    build_tableschema_from_dico_snds()
    add_primary_and_foreign_keys_to_tableschema()

    # Generating tableschema byproducts
    generate_documentation_snds()
    generate_dico_snds()

    generate_relational_diagram()
