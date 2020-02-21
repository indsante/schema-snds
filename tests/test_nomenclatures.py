import logging
import os
from pprint import pprint

import pandas as pd
import pytest
from goodtables import validate
from tableschema import Schema

from src.constants import NOMENCLATURES_DIR, ROOT_DIR
from src.utils import get_all_nomenclatures_csv_schema_path, get_all_nomenclatures_schema, get_used_nomenclatures, \
    get_present_nomenclatures


def test_nomenclatures_list():
    nomenclature_list = get_present_nomenclatures(ROOT_DIR)
    assert nomenclature_list, "No nomenclatures"
    assert len(nomenclature_list) == len(set(nomenclature_list)), "There are duplicate nomenclatures"


def test_nomenclature_presence():
    present_nomenclatures = get_present_nomenclatures(ROOT_DIR)
    print(present_nomenclatures)
    used_nomenclatures = get_used_nomenclatures(ROOT_DIR)
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
    assert 0 == df.duplicated().sum(), df[df.duplicated(keep=False)].sort_values(by=schema.primary_key)


# TODO
@pytest.mark.xfail(reason="Adding title should be done but is not finished")
@pytest.mark.parametrize('schema', get_all_nomenclatures_schema(NOMENCLATURES_DIR))
def test_nomenclature_have_title(schema):
    """
    Validate that nomenclature's schema have a title.
    """
    name = schema.descriptor['name']
    assert schema.descriptor["title"], "Nomenclature's schema for {} should have a title".format(name)


@pytest.mark.xfail(reason="Some nomenclature do not have any label")
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
