import pytest
from unittest.mock import patch, MagicMock
from Scrapper.scrapper import download_html


@pytest.fixture
def mock_s3():
    """Mock del cliente S3."""
    with patch("boto3.client") as mock:
        mock_s3_instance = MagicMock()
        mock.return_value = mock_s3_instance
        yield mock_s3_instance


@patch("requests.get")
def test_download_html(mock_requests, mock_s3):
    """Prueba que download_html descarga y sube el archivo a S3 correctamente."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Mock Page</body></html>"
    mock_requests.return_value = mock_response

    response = download_html()

    assert response["statusCode"] == 200
    assert "Archivo guardado en s3" in response["body"]
    mock_s3.put_object.assert_called_once()
