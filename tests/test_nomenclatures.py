import logging
import os
import numpy as np
import re

from src.constants import ROOTED_BYPRODUCTS_DIR
from src.utils import get_all_schema

def list_nomenclatures_usage():
    schemas = get_all_schema()
    used_nomenclatures = [
        [field.descriptor['nomenclature'] for field in schema.fields] for schema in schemas]
    unique_nomenclatures = [
        nom for nom in np.unique(np.concatenate(used_nomenclatures)) if nom != '-']
    return unique_nomenclatures


def list_present_nomenclatures():
    present_nomenclatures_files = os.listdir(ROOTED_BYPRODUCTS_DIR)
    present_nomenclatures = [re.sub('.csv$', '', nom) for nom in present_nomenclatures_files]
    return present_nomenclatures

def test_nomenclature_presence():
    present_nomenclatures = list_present_nomenclatures()
    used_nomenclatures = list_nomenclatures_usage()
    nomenclatures_difference = list(set(used_nomenclatures) - set(present_nomenclatures))
    if len(nomenclatures_difference) != 0:
        logging.info("Following nomenclatures are described in schema but not added in nomenclature folder; {}"
                     .format(nomenclatures_difference ))
    assert len(nomenclatures_difference) == 0

test_nomenclature_presence()