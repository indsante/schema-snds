import pytest
import pandas as pd

from src.reformat_snds_dico import FORMAT_SOURCE, extract_type_and_length, add_type_and_length_columns

input_arg_to_expected_output = [
    ('Numérique (4)', ['Numérique ', '4']),
    ('num', ['num', None]),
    ('NUMBER(11,2)', ['NUMBER', '11,2'])
]


@pytest.mark.parametrize('input_arg,expected_output', input_arg_to_expected_output)
def test_extract_type_and_length(input_arg, expected_output):
    assert expected_output == extract_type_and_length(input_arg)


def test_add_type_and_length():
    # Given
    input_df = pd.DataFrame.from_dict({
        FORMAT_SOURCE: ['Numérique (4)', 'Caractère (2)']
    })

    expected_output = pd.DataFrame({
        FORMAT_SOURCE: ['Numérique (4)', 'Caractère (2)'],
        'type': ['numérique ', 'caractère '],
        'length': ['4', '2']
    })

    # When
    actual_output = add_type_and_length_columns(input_df)
    print(actual_output.to_records())

    assert expected_output.equals(actual_output)
