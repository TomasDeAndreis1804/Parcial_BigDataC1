import unittest
from unittest.mock import patch, MagicMock
from Parsing.parser import clean_price
from Scrapping.scrapper import app


class TestScraperParser(unittest.TestCase):
    """Test case for Scraper and Parser functions."""

    def test_clean_price(self):
        """Test the clean_price function with various inputs."""
        self.assertEqual(clean_price("$1,200,000"), "1200000")
        self.assertEqual(clean_price("COP 3.5M"), "35")
        self.assertEqual(clean_price(2500), "2500")
        self.assertEqual(clean_price(None), "N/A")

    @patch("requests.get")
    def test_scrapper_request(self, mock_get):
        """Test the scrapper request function with a mocked response."""
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test</body></html>"
        mock_get.return_value = mock_response

        result = app({}, {})  # Simulate Lambda function execution
        self.assertIsNotNone(result)

    @patch("boto3.client")
    def test_s3_upload(self, mock_boto3):
        """Test the S3 upload function with a mocked S3 client."""
        mock_s3 = MagicMock()
        mock_boto3.return_value = mock_s3
        mock_s3.upload_file.return_value = None  # Simulate success

        app({}, {})  # Simulate function execution
        mock_s3.upload_file.assert_called()

if __name__ == "__main__":
    unittest.main()
