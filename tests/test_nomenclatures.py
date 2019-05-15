import logging
import os
import re

from src.constants import SCHEMAS, NOMENCLATURES, NO_NOMENCLATURE
from src.utils import get_all_schema
from src.byproducts.main import generate_byproducts


def list_nomenclatures_usage():
    used_nomenclatures = set()
    for schema in get_all_schema(SCHEMAS):
        for field in schema.fields:
            nomenclature = field.descriptor['nomenclature']
            if nomenclature != NO_NOMENCLATURE:
                used_nomenclatures.add(nomenclature)
    return used_nomenclatures


def list_present_nomenclatures():
    present_nomenclatures_files = []
    for root, dirs, files in os.walk(NOMENCLATURES):
        present_nomenclatures_files += files
    present_nomenclatures = [re.sub('.csv$', '', nom) for nom in present_nomenclatures_files]
    return present_nomenclatures


def test_number_nomenclatures_sup_1():
    assert list_present_nomenclatures()


def test_nomenclature_presence():
    generate_byproducts()
    present_nomenclatures = list_present_nomenclatures()
    print(present_nomenclatures)
    used_nomenclatures = list_nomenclatures_usage()
    nomenclatures_difference = list(set(used_nomenclatures) - set(present_nomenclatures))
    if len(nomenclatures_difference) != 0:
        logging.error(
            "Following nomenclatures are described in schema but not added in nomenclature folder; {}"
            .format(nomenclatures_difference))
    assert len(nomenclatures_difference) == 0
