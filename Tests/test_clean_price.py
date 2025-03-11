import pytest
from Parser.parser import clean_price


@pytest.mark.parametrize("input_value, expected_output", [
    ("$1.000.000", "1000000"),
    ("USD 500", "500"),
    ("COP 200000", "200000"),
    (None, "N/A"),
    ("$", "N/A")
])
def test_clean_price(input_value, expected_output):
    """Prueba que clean_price elimina caracteres no numéricos."""
    assert clean_price(input_value) == expected_output
