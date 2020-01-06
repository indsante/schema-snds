from src.byproducts.relational_diagram import generate_relational_diagram
from src.constants import ROOT_DIR


def test_generate_relational_diagram():
    generate_relational_diagram(ROOT_DIR)
