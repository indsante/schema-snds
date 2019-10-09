"""
These tests are looking at current schemas, not tests ones. Hence we do not use rooted schema dir
"""

import logging

import pytest
from tableschema import Schema

from src.constants import SCHEMAS, HISTORY, DATE_CREATED, DATE_MISSING, DATE_DELETED, NOMENCLATURE
from src.utils import get_all_schema_path


@pytest.mark.parametrize('schema_path', get_all_schema_path(SCHEMAS))
def test_tableschema_is_valid(schema_path):
    schema = Schema(schema_path)
    if not schema.valid:
        for error in schema.errors:
            logging.info("Error in schema at path '{}'".format(schema_path))
            logging.error(error)
        assert schema.valid


def test_get_all_schema_path_return_all_schemas():
    number_of_schemas = len(list(get_all_schema_path(SCHEMAS)))
    assert number_of_schemas >= 143


@pytest.mark.parametrize('schema_path', get_all_schema_path(SCHEMAS))
def test_tableschema_contains_all_fields(schema_path):
    descriptor = Schema(schema_path).descriptor

    assert sorted(list(set(descriptor.keys()) - set(["foreignKeys", "primaryKey"]))) == \
           sorted(["fields", "name", "title", "description", "produit", "missingValues", HISTORY])

    assert set(descriptor[HISTORY].keys()) == set([DATE_CREATED, DATE_DELETED, DATE_MISSING])

    for field in descriptor['fields']:
        assert sorted(list(set(field.keys()) - set(["constraints"]))) == \
               sorted(["name", "description", "type", NOMENCLATURE, "length", "format", DATE_CREATED, DATE_DELETED,
                       DATE_MISSING])
