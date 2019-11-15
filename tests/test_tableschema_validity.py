"""
These tests are looking at current schemas, not tests ones. Hence we do not use rooted schema dir
"""

import logging
import os
import pytest
from tableschema import Schema

from src.constants import SCHEMAS, HISTORY, DATE_CREATED, DATE_MISSING, DATE_DELETED, NOMENCLATURE, OBSERVATION, \
    CHAMP, REGLE_GESTION, TYPE_CSV, TYPE_ORACLE
from src.utils import get_all_schema_path


@pytest.mark.parametrize('schema_path', get_all_schema_path(SCHEMAS))
def test_tableschema_is_valid(schema_path):
    schema = Schema(schema_path)
    if not schema.valid:
        for error in schema.errors:
            logging.info("Error in schema at path '{}'".format(schema_path))
            logging.error(error)
        assert schema.valid


@pytest.mark.parametrize('schema_path', get_all_schema_path(SCHEMAS))
def test_tableschema_name_and_produc(schema_path):
    filename = os.path.basename(schema_path)[:-5]
    schema = Schema(schema_path)
    name = schema.descriptor["name"]
    assert name == filename

    productname = schema_path.split("/")[-2]
    product = schema.descriptor["produit"]
    assert product == productname


def test_get_all_schema_path_return_all_schemas():
    number_of_schemas = len(list(get_all_schema_path(SCHEMAS)))
    assert number_of_schemas >= 143


@pytest.mark.parametrize('schema_path', get_all_schema_path(SCHEMAS))
def test_tableschema_contains_all_fields(schema_path):
    descriptor = Schema(schema_path).descriptor

    assert sorted(list(set(descriptor.keys()) - set(["foreignKeys", "primaryKey"]))) == \
           sorted(["fields", "name", "title", CHAMP, "produit", "missingValues", HISTORY, OBSERVATION])

    assert set(descriptor[HISTORY].keys()) == set([DATE_CREATED, DATE_DELETED, DATE_MISSING])

    for field in descriptor['fields']:
        assert sorted(list(set(field.keys()) - set(["constraints"]))) == \
               sorted(["name", "description", TYPE_CSV, NOMENCLATURE, "length", "format", OBSERVATION, REGLE_GESTION,
                       DATE_CREATED, DATE_DELETED, DATE_MISSING, TYPE_ORACLE])
