import pytest

from src.byproducts.main import generate_byproducts
from src.constants import TESTS_DIR, ROOT_DIR


@pytest.fixture(scope="module")
def generate_byproducts_root():
    generate_byproducts(False, ROOT_DIR)


@pytest.fixture(scope="module")
def generate_byproducts_tests():
    generate_byproducts(False, TESTS_DIR)
