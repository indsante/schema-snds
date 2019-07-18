import logging
import shutil

from src.byproducts.copy_nomenclatures import cp_nomenclatures
from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.nomenclatures_as_foreign_keys import generate_schema_with_nomenclature_as_foreign_keys
from src.byproducts.relational_diagram import generate_relational_diagram
from src.constants import ROOTED_BYPRODUCTS_DIR


def generate_byproducts(generate_erd=False):
    logging.info("Suppression du dossier '{}' contenant les produits dérivés.".format(ROOTED_BYPRODUCTS_DIR))
    shutil.rmtree(ROOTED_BYPRODUCTS_DIR, ignore_errors=True)

    logging.info("Génération des produits dérivés dans le dossier '{}'.".format(ROOTED_BYPRODUCTS_DIR))
    generate_documentation_snds()
    generate_dico_snds()
    cp_nomenclatures()
    generate_schema_with_nomenclature_as_foreign_keys()

    if generate_erd:
        generate_relational_diagram()
