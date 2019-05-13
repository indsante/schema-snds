import logging
import os
from src.constants import PRODUIT_NOMENCLATURES, NOMENCLATURES_DIR
from distutils.dir_util import copy_tree

def cp_nomenclatures():
    path2oraval_nomenclatures = os.path.join(NOMENCLATURES_DIR, "ORAVAL")
    path2oraref_nomenclatures = os.path.join(NOMENCLATURES_DIR, "ORAREF")
    path2drees_nomenclatures = os.path.join(NOMENCLATURES_DIR, "DREES")

    logging.info("Copy the content of {}, {}, {} into {}".format(
        path2oraval_nomenclatures,
        path2oraref_nomenclatures,
        path2drees_nomenclatures,
        PRODUIT_NOMENCLATURES
    ))
    os.makedirs(PRODUIT_NOMENCLATURES)
    copy_tree(path2oraval_nomenclatures, PRODUIT_NOMENCLATURES)
    copy_tree(path2oraref_nomenclatures, PRODUIT_NOMENCLATURES)
    copy_tree(path2drees_nomenclatures, PRODUIT_NOMENCLATURES)
