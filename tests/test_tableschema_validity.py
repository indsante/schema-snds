import logging
import os
import shutil

import pytest
from tableschema import Schema

from src.byproducts.dico_snds import generate_dico_snds
from src.byproducts.documentation_snds import generate_documentation_snds
from src.constants import TESTS_DIR, BYPRODUCTS_DIR
from src.utils import get_all_schema_path


@pytest.mark.parametrize('schema_path', get_all_schema_path())
def test_tableschema_is_valid(schema_path):
    schema = Schema(schema_path)
    if not schema.valid:
        for error in schema.errors:
            logging.info("Error in schema at path '{}'".format(schema_path))
            logging.error(error)
        assert schema.valid


def test_generated_byproducts_equal_files():
    shutil.rmtree(BYPRODUCTS_DIR)
    generate_dico_snds()
    generate_documentation_snds()

    for root, dirs, files in os.walk(BYPRODUCTS_DIR):
        for file in files:
            actual_file_path = os.path.join(root, file)
            expected_file_path = os.path.join(root[len(TESTS_DIR) + 1:], file)
            with open(actual_file_path, encoding="utf-8") as f:
                actual = f.read().split("\n")
            with open(expected_file_path, encoding="utf-8") as f:
                expected = f.read().split("\n")
            assert expected == actual
