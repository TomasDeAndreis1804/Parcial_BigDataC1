import json
import pytest
from unittest.mock import MagicMock
from Scrapper.scrapper import extract_data  # Asegúrate de importar correctamente la función

@pytest.fixture
def sample_html():
    return """
    <html>
        <body>
            <a class="listing listing-card" data-location="Bogotá"
                data-price="1.200.000" data-rooms="2" data-bathrooms="1" 
                data-floorarea="50">
            </a>
        </body>
    </html>
    """
    
def test_extract_data(sample_html):
    """Prueba que extract_data extrae correctamente la información."""
    data = extract_data(sample_html)
    expected = [["2025-03-10", "Bogotá", "1200000", "2", "1", "50"]]
    assert data == expected
