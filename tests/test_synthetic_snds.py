from os.path import join as pjoin

import pytest
from tableschema import Schema

from src.constants import ROOT_DIR, TESTS_DIR, SYNTHETIC_SNDS_DIR
from src.utils import get_all_schema_path

SYNTHETIC_SNDS_TEST_DIR = pjoin(TESTS_DIR, SYNTHETIC_SNDS_DIR)


@pytest.mark.parametrize('schema_path', (*get_all_schema_path(ROOT_DIR), *get_all_schema_path(SYNTHETIC_SNDS_TEST_DIR)))
def test_column_in_only_one_foreign_key(schema_path):
    """ Each column should appear as field in at most one foreign key, otherwise generation will not be coherent. """
    schema = Schema(schema_path)
    fk_fields = set()
    for fk in schema.foreign_keys:
        for field in fk['fields']:
            if (
                    field == 'BEN_IDT_ANO' and
                    fk['reference']['resource'] in ['IR_IBA_R', 'IR_BEN_R'] and
                    TESTS_DIR not in schema_path
            ):  # no test for BEN_IDT_ANO -> IR_IBA_R/IR_BEN_R in ROOT_DIR schemas
                pass
            else:
                assert field not in fk_fields
                fk_fields.add(field)
