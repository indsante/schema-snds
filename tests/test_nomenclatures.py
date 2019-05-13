import logging
import os
import numpy as np
import re

from src.constants import ROOTED_NOMENCLATURES_DIR
from src.utils import get_all_schema


PATH2ORAVAL = os.path.join(ROOTED_NOMENCLATURES_DIR, "ORAVAL")
PATH2ORAREF = os.path.join(ROOTED_NOMENCLATURES_DIR, "ORAREF")
PATH2DREES = os.path.join(ROOTED_NOMENCLATURES_DIR, "DREES")

print(os.listdir('.'))

def list_nomenclatures_usage():
    schemas = get_all_schema()
    used_nomenclatures = [
        [field.descriptor['nomenclature'] for field in schema.fields] for schema in schemas]
    unique_nomenclatures = [
        nom for nom in np.unique(np.concatenate(used_nomenclatures)) if nom != '-']
    return unique_nomenclatures


def list_present_nomenclatures():
    oraval_noms = os.listdir(PATH2ORAVAL)
    oraref_noms = os.listdir(PATH2ORAREF)
    drees_noms = os.listdir(PATH2DREES)
    present_nomenclatures_files = oraval_noms + oraref_noms + drees_noms
    present_nomenclatures = [re.sub('.csv$', '', nom) for nom in present_nomenclatures_files]
    #print(present_nomenclatures)
    #print(len(present_nomenclatures))
    return present_nomenclatures

def test_nomenclature_presence():
    present_nomenclatures = list_present_nomenclatures()
    used_nomenclatures = list_nomenclatures_usage()
    nomenclatures_difference = list(set(used_nomenclatures) - set(present_nomenclatures))
    logging.info("Following nomenclatures are described in schema but not added in nomenclature folder; {}"
                 .format(nomenclatures_difference ))
    assert len(nomenclatures_difference) == 0

test_nomenclature_presence()