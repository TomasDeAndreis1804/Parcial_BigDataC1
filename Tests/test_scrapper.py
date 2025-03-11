import pytest
from unittest.mock import patch, MagicMock
from Scrapper.scrapper import app


@pytest.fixture
def mock_s3():
    """Mock del cliente S3."""
    with patch("boto3.client") as mock:
        mock_s3_instance = MagicMock()
        mock.return_value = mock_s3_instance
        mock_s3_instance.put_object.return_value = {}  # Simula respuesta de S3
        yield mock_s3_instance


@patch("requests.get")
def test_app(mock_requests, mock_s3):
    """Prueba que app descarga y sube el archivo a S3 correctamente."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Mock Page</body></html>"
    mock_requests.return_value = mock_response

    # Simular respuesta de S3 para evitar errores de archivo no encontrado
    mock_s3.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=b"<html><body>Mock Page</body></html>"))
    }

    # Evento S3 simulado con un archivo válido
    mock_event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "bucket-parcial1-1"},
                "object": {"key": "mock-file.html"}
            }
        }]
    }
    mock_context = {}

    response = app(mock_event, mock_context)

    assert response["statusCode"] == 200
    assert "Archivo guardado en s3" in response["body"]

    # Depurar si put_object no se llama
    if mock_s3.put_object.call_count == 0:
        print("⚠ ERROR: La función app() no llamó a put_object(). Verifica si hay errores previos en la ejecución.")

    mock_s3.put_object.assert_called_once()
