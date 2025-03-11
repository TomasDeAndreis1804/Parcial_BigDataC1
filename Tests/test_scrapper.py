import pytest
from unittest.mock import patch, MagicMock
from Scrapper.scrapper import app

@pytest.fixture
def mock_s3():
    """Simula el cliente de S3."""
    with patch("boto3.client") as mock:
        mock_s3_instance = MagicMock()
        mock.return_value = mock_s3_instance
        yield mock_s3_instance

@patch("requests.get")
def test_scrapper(mock_requests, mock_s3):
    """Prueba que el scrapper guarde correctamente los datos en S3."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Mock Page</body></html>"
    mock_requests.return_value = mock_response

    event = {}
    context = {}

    response = app(event, context)

    assert response["statusCode"] == 200
    mock_s3.put_object.assert_called_once()
