import pytest
from tableschema import Schema

from src.constants import NUMBER, INTEGER, TYPE_CSV, IGNORED_DATE_NOMENCLATURE
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


@pytest.mark.parametrize('schema_path', get_all_schema_path(ROOT_DIR))
def test_date_type_values_are_valid(schema_path):
    schema_to_validate = Schema(schema_path)
    for field in schema_to_validate.fields:
        tstype = field.descriptor.get(TYPE_CSV)
        name = field.descriptor.get('name')
        nomenclature = field.descriptor.get('nomenclature')
        if nomenclature == IGNORED_DATE_NOMENCLATURE or 'MOI' in name:
            assert tstype == 'date' or tstype == 'yearmonth'

