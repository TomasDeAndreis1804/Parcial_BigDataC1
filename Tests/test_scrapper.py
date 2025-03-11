import pytest
from Scrapper.scrapper import extract_data  # Importación correcta de la función

@pytest.fixture
def sample_html():
    """HTML de prueba con datos de un apartamento."""
    return """
    <html>
        <body>
            <a class="listing listing-card" data-location="Bogotá"
                data-price="1200000" data-rooms="2" data-bathrooms="1" 
                data-floorarea="50">
            </a>
        </body>
    </html>
    """


def test_extract_data(sample_html):
    """Prueba que extract_data extrae correctamente la información esperada."""
    data = extract_data(sample_html)
    expected = [["2025-03-10", "Bogotá", "1200000", "2", "1", "50"]]
    assert data == expected
