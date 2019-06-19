from src.byproducts.update_byproducts_repositories import update_all_byproducts
from src.byproducts.main import generate_byproducts

EXPECTED_BYPRODUCTS_DIR = 'expected_byproducts'


def test_update_all_byproducs_pass():
    generate_byproducts()
    update_all_byproducts(local=True)
