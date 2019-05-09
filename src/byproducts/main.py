import logging
import shutil

from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_relational_diagram
from src.constants import BYPRODUCTS_DIR


def generate_byproducts(generate_erd=False):
    logging.info("Suppression du dossier '{}' contenant les produits dérivés.".format(BYPRODUCTS_DIR))
    shutil.rmtree(BYPRODUCTS_DIR, ignore_errors=True)

    logging.info("Génération des produits dérivés dans le dossier '{}'.".format(BYPRODUCTS_DIR))
    generate_documentation_snds()
    generate_dico_snds()
    if generate_erd:
        generate_relational_diagram()
