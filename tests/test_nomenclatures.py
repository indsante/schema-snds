import logging
import os
import re
from pprint import pprint

import pandas as pd
import pytest
from goodtables import validate
from tableschema import Schema

from src.byproducts.main import generate_byproducts
from src.constants import SCHEMAS, NOMENCLATURES_DIR, NO_NOMENCLATURE
from src.utils import get_all_nomenclatures_csv_schema_path, get_all_nomenclatures_schema
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
    for root, dirs, files in os.walk(NOMENCLATURES_DIR):
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
    for nomenclature_path, schema_path in get_all_nomenclatures_csv_schema_path(NOMENCLATURES_DIR):
        print(schema_path)
        assert os.path.exists(schema_path), "Missing schema for nomenclature '{}'.".format(nomenclature_path)


@pytest.mark.parametrize('nomenclature_path,schema_path', get_all_nomenclatures_csv_schema_path(NOMENCLATURES_DIR))
def test_validate_nomenclature_schema(nomenclature_path, schema_path):
    """
    Validate that nomenclature csv is valid when compared to its's schema
    """
    report = validate(nomenclature_path, schema=schema_path)
    pprint(report)
    assert report['error-count'] == 0


@pytest.mark.parametrize('nomenclature_path,schema_path', get_all_nomenclatures_csv_schema_path(NOMENCLATURES_DIR))
def test_nomenclature_schema_name_equal_file_name(nomenclature_path, schema_path):
    """
    Validate that nomenclature filename equal schema.descriptor.name
    """
    filename = os.path.basename(schema_path)[:-5]
    name = Schema(schema_path).descriptor["name"]
    assert name == filename


@pytest.mark.parametrize('nomenclature_path,schema_path', get_all_nomenclatures_csv_schema_path(NOMENCLATURES_DIR))
def test_nomenclature_primary_keys_is_unique(nomenclature_path, schema_path):
    """
    Validate that nomenclature have a primary key, and that it is unique.
    """
    schema = Schema(schema_path)
    assert schema.primary_key, "Schema of nomenclature {} should contain a primaryKey".format(schema.descriptor['name'])
    df = pd.read_csv(nomenclature_path, sep=';', usecols=schema.primary_key)
    assert 0 == df.duplicated().sum()


# TODO
@pytest.mark.xfail(reason="To be done")
@pytest.mark.parametrize('schema', get_all_nomenclatures_schema(NOMENCLATURES_DIR))
def test_nomenclature_have_title(schema):
    """
    Validate that nomenclature's schema have a title.
    """
    name = schema.descriptor['name']
    assert schema.descriptor["title"], "Nomenclature's schema for {} should have a title".format(name)


@pytest.mark.parametrize('schema', get_all_nomenclatures_schema(NOMENCLATURES_DIR))
def test_nomenclatures_have_one_field_with_role_label(schema):
    name = schema.descriptor['name']
    if name in ['IR_DTE_V', 'IR_MTR_V', 'IR_ORG_V']:
        return

    label_fields = []
    for field in schema.fields:
        if 'role' in field.descriptor and field.descriptor['role'] == 'label':
            label_fields.append(field.name)
    assert len(label_fields) == 1, \
        "Nomenclature's schema for {} should have one and only one field with role 'label'".format(name)


@pytest.mark.parametrize('schema', get_all_nomenclatures_schema(NOMENCLATURES_DIR))
def test_nomenclatures_have_one_field__with_role_code(schema):
    name = schema.descriptor['name']

    code_fields = []
    for field in schema.fields:
        if 'role' in field.descriptor and field.descriptor['role'] == 'code':
            code_fields.append(field.name)
    assert len(code_fields) == 1, \
        "Nomenclature's schema for {} should have one and only one field with role 'code'".format(name)
