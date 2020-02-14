import os
from os.path import join as pjoin

import pytest

from src.byproducts.update_byproducts_repositories import update_all_byproducts
from src.constants import TESTS_DIR, ROOT_DIR, BYPRODUCTS_DIR

EXPECTED_BYPRODUCTS_DIR = 'expected_byproducts'


def test_generate_byproducts_root(generate_byproducts_root):
    pass


def test_generate_byproducts_tests(generate_byproducts_tests):
    pass


def get_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield root, file


@pytest.mark.parametrize('root,file', get_files_in_directory(pjoin(TESTS_DIR, BYPRODUCTS_DIR)))
def test_generated_byproducts_equal_files(generate_byproducts_tests, root, file):
    actual_file_path = os.path.join(root, file)
    expected_file_path = actual_file_path.replace(BYPRODUCTS_DIR, EXPECTED_BYPRODUCTS_DIR)
    with open(actual_file_path, encoding="utf-8") as f:
        actual = f.read().split("\n")
    with open(expected_file_path, encoding="utf-8") as f:
        expected = f.read().split("\n")
    for expected_line, actual_line in zip(expected, actual):
        assert expected_line == actual_line


def test_update_all_byproducts_locally(generate_byproducts_root):
    update_all_byproducts(local=True, work_dir=ROOT_DIR)
