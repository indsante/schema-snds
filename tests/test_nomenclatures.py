import logging
import os
import re
from pprint import pprint

import pytest
from goodtables import validate

from src.byproducts.main import generate_byproducts
from src.constants import SCHEMAS, NOMENCLATURES, NO_NOMENCLATURE
from src.utils import get_all_nomenclatures_csv_schema_path
from src.utils import get_all_schema


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


def test_nomenclatures_list():
    nomenclature_list = list_present_nomenclatures()
    assert nomenclature_list
    assert len(nomenclature_list) == len(set(nomenclature_list))


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


def test_all_nomenclatures_have_schema():
    for nomenclature_path, schema_path in get_all_nomenclatures_csv_schema_path(NOMENCLATURES):
        print(schema_path)
        assert os.path.exists(schema_path), "Missing schema for nomenclature '{}'.".format(nomenclature_path)


@pytest.mark.parametrize('nomenclature_path,schema_path', get_all_nomenclatures_csv_schema_path(NOMENCLATURES))
def test_validate_nomenclature_schema(nomenclature_path, schema_path):
    """
    Validate that nomenclature's schema is valid.
    """
    report = validate(nomenclature_path, schema=schema_path)
    pprint(report)
    assert report['error-count'] == 0
