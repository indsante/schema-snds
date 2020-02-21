import logging
import shutil
from os.path import join as pjoin

from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_schema_md
from src.byproducts.relational_diagram import generate_relational_diagram
from src.byproducts.tsfaker_schemas import generate_synthetic_snds
from src.constants import BYPRODUCTS_DIR


def generate_byproducts(generate_erd: bool, work_dir: str, products: list = None):
    """

    :param generate_erd: Generate relational diagram
    :param work_dir: Working directory, either ROOT_DIR or TEST_DIR
    :param products: Restrict generation to these products
    :return:
    """
    rooted_byproducts_dir = pjoin(work_dir, BYPRODUCTS_DIR)

    logging.info("Suppression du dossier '{}' contenant les produits dérivés.".format(rooted_byproducts_dir))
    shutil.rmtree(rooted_byproducts_dir, ignore_errors=True)

    logging.info(f"Génération des produits dérivés pour les produits {products} "
                 f"dans le dossier '{rooted_byproducts_dir}'.")
    generate_schema_md(work_dir, products)
    generate_dico_snds(work_dir, products)
    generate_synthetic_snds(work_dir, products)

    if generate_erd:
        generate_relational_diagram(work_dir, products)
