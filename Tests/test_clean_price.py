import pytest
from Parser.parser import clean_price

def test_clean_price():
    """Prueba que clean_price elimina caracteres no numéricos."""
    assert clean_price("$1.000.000") == "1000000"
    assert clean_price("USD 500") == "500"
    assert clean_price("COP 200000") == "200000"
    assert clean_price(None) == "N/A"
