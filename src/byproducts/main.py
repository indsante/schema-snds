import logging
import shutil
from os.path import join as pjoin

from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.byproducts.relational_diagram import generate_relational_diagram
from src.byproducts.tsfaker_schemas import generate_synthetic_snds
from src.constants import WORKING_DIR, BYPRODUCTS_DIR


def generate_byproducts(generate_erd=False, work_dir=WORKING_DIR):
    rooted_byproducts_dir = pjoin(work_dir, BYPRODUCTS_DIR)

    logging.info("Suppression du dossier '{}' contenant les produits dérivés.".format(rooted_byproducts_dir))
    shutil.rmtree(rooted_byproducts_dir, ignore_errors=True)

    logging.info("Génération des produits dérivés dans le dossier '{}'.".format(rooted_byproducts_dir))
    generate_documentation_snds(work_dir)
    generate_dico_snds(work_dir)
    generate_synthetic_snds(work_dir)

    if generate_erd:
        generate_relational_diagram(work_dir)
