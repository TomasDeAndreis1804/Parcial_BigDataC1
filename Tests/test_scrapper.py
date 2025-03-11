import unittest
from unittest.mock import patch, MagicMock
import boto3
from Scrapper.scrapper import app

class TestScrapper(unittest.TestCase):

    @patch("boto3.client")
    def test_s3_download(self, mock_boto3_client):
        """Simula la descarga de un archivo desde S3"""
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: b"<html><body><a class='listing listing-card' data-location='Bogotá' data-price='$1000000' data-rooms='3' data-bathrooms='2' data-floorarea='50'></a></body></html>")
        }

        event = {
            "Records": [{"s3": {"bucket": {"name": "bucket-parcial1-1"}, "object": {"key": "test.html"}}}]
        }
        response = app(event, None)
        self.assertEqual(response["statusCode"], 200)

if __name__ == "__main__":
    unittest.main()
