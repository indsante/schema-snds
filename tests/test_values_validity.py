import pytest
from tableschema import Schema

from src.constants import NUMBER, INTEGER, TYPE_CSV
from src.constants import ROOT_DIR
from src.utils import get_all_schema_path


@pytest.mark.parametrize('schema_path', get_all_schema_path(ROOT_DIR))
def test_length_values_are_valid(schema_path):
    schema_to_validate = Schema(schema_path)
    for field in schema_to_validate.fields:
        tstype = field.descriptor.get(TYPE_CSV)
        length = field.descriptor.get('length')
        if length is None:
            continue
        if tstype == NUMBER:
            assert ',' in length
        if tstype == INTEGER:
            assert ',' not in length
