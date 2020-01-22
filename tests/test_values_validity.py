import pytest
from tableschema import Schema
import logging

from src.constants import ROOT_DIR
from src.utils import get_all_schema_path
from src.constants import NUMBER, INTEGER, TYPE_CSV


# Number is correct if it has comma or null
def number_is_correct(tstype, length):
    if length is not None:
        assert ',' in length


# Integer is correct if it doesnt have comma or is null
def integer_is_correct(tstype, length):
    if length is not None:
        assert ',' not in length


@pytest.mark.parametrize('schema_path', get_all_schema_path(ROOT_DIR))
def test_numeric_values_are_valid(schema_path):

    schema_to_validate = Schema(schema_path)
    for field in schema_to_validate.fields:
        tstype = field.descriptor.get(TYPE_CSV)
        length = field.descriptor.get('length')
        if tstype == NUMBER:
            number_is_correct(tstype, length)
        if tstype == INTEGER:
            integer_is_correct(tstype, length)


