import pytest
from Scrapper.scrapper import download_html


def test_download_html():
    """Prueba que download_html devuelve una respuesta correcta."""
    response = download_html()
    assert response["statusCode"] == 200
    assert "Archivo guardado en s3" in response["body"]
