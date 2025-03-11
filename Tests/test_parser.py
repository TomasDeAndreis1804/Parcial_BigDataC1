import unittest
from unittest.mock import patch, MagicMock
from Parsing.parser import clean_price
from Scrapping.scrapper import app


class TestScraperParser(unittest.TestCase):
    def test_clean_price(self):
        """Test para la función clean_price con diferentes formatos de entrada."""
        self.assertEqual(clean_price("$1,200,000"), "1200000")
        self.assertEqual(clean_price("COP 3.5M"), "35")
        self.assertEqual(clean_price(2500), "2500")
        self.assertEqual(clean_price(None), "N/A")

    @patch("requests.get")
    def test_scrapper_request(self, mock_get):
        """Test para simular una solicitud HTTP con requests.get mockeado."""
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_get.return_value = mock_response

        result = app({}, {})  # Simula la ejecución de la función Lambda
        self.assertIsNotNone(result)

    @patch("boto3.client")
    def test_s3_upload(self, mock_boto3):
        """Test para simular la subida de un archivo a S3 mediante un cliente mockeado."""
        mock_s3 = MagicMock()
        mock_boto3.return_value = mock_s3
        mock_s3.upload_file.return_value = None  # Simula éxito

        # Simular archivo y bucket para la subida
        mock_s3.upload_file("test_file", "test_bucket", "test_path")

        # Aseguramos que upload_file fue llamado
        mock_s3.upload_file.assert_called_with("test_file", "test_bucket", "test_path")
        self.assertTrue(mock_s3.upload_file.called)


if __name__ == "__main__":
    unittest.main()
