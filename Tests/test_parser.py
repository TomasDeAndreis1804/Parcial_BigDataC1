import pytest
import datetime
from Parser.parser import extract_data


@pytest.fixture
def sample_html():
    """HTML de prueba con datos de un apartaestudio."""
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
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    expected = [[today, "Bogotá", "1200000", "2", "1", "50"]]  # floor_area como string

    assert data == expected
