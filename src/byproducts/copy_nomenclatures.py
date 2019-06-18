import logging
import os
from distutils.dir_util import copy_tree

from src.constants import PRODUIT_NOMENCLATURES, PATH2ORAVAL, PATH2ORAREF, PATH2DREES


def cp_nomenclatures():
    logging.info("Copy the content of {}, {}, {} into {}".format(
        PATH2ORAVAL,
        PATH2ORAREF,
        PATH2DREES,
        PRODUIT_NOMENCLATURES
    ))
    os.makedirs(PRODUIT_NOMENCLATURES)
    copy_tree(PATH2ORAVAL, PRODUIT_NOMENCLATURES)
    copy_tree(PATH2ORAREF, PRODUIT_NOMENCLATURES)
    copy_tree(PATH2DREES, PRODUIT_NOMENCLATURES)
