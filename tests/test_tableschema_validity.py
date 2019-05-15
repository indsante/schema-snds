"""
These tests are looking at current schemas, not tests ones. Hence we do not use rooted schema dir
"""

import logging

import pytest
from tableschema import Schema

from src.utils import get_all_schema_path
from src.constants import SCHEMAS


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
    assert number_of_schemas == 143
