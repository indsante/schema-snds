from src.utils import get_all_schema_path


def test_get_all_schema_path_return_all_schemas():
    number_of_schemas = len(list(get_all_schema_path()))
    assert number_of_schemas == 142
