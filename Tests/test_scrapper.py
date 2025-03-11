import datetime
import unittest
from unittest.mock import patch, MagicMock
from Scrapping.scrapper import app


class TestScrapperApp(unittest.TestCase):
    @patch('scrapper.s3_client')
    @patch('scrapper.requests.get')
    @patch('scrapper.datetime.datetime.utcnow', return_value=datetime.datetime(2025, 3, 11))
    def test_app(self, mock_utcnow, mock_requests_get, mock_s3_client):
        # Configuramos el mock de requests.get para que siempre retorne una respuesta exitosa.
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.text = "Contenido de prueba"
        mock_requests_get.return_value = fake_response

        # Ejecutar la función app con event y context dummy
        event = {}   # No se utiliza dentro de la función
        context = None
        result = app(event, context)

        # Se espera que se hayan consultado 10 páginas, concatenando el contenido de cada una.
        expected_html = ("Contenido de prueba\n\n") * 10

        # Verificar que se llamó a s3_client.put_object con los parámetros correctos.
        mock_s3_client.put_object.assert_called_once_with(
            Bucket="bucket-parcial1-1",
            Key="2025-03-11.html",
            Body=expected_html.encode("utf-8"),
            ContentType="text/html"
        )

        # Verificar la respuesta de la función.
        self.assertEqual(result["statusCode"], 200)
        self.assertIn("s3://bucket-parcial1-1/2025-03-11.html", result["body"])


if __name__ == "__main__":
    unittest.main()
