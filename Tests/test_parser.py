import unittest
from unittest.mock import patch, MagicMock
from Parser.parser import clean_price, extract_number, extract_data, save_to_s3

class TestParserFunctions(unittest.TestCase):


    def test_clean_price(self):
        self.assertEqual(clean_price("$1,500,000"), "1500000")
        self.assertEqual(clean_price("COP 2.300.000"), "2300000")
        self.assertEqual(clean_price(350000), "350000")
        self.assertEqual(clean_price(None), "N/A")


    def test_extract_number(self):
        self.assertEqual(extract_number("Área: 45m²"), 45)
        self.assertEqual(extract_number("120.5 m2"), 1205)
        self.assertEqual(extract_number("Sin datos"), None)
        self.assertEqual(extract_number(None), None)


    @patch("Parser.parser.s3_client")
    def test_save_to_s3(self, mock_s3_client):
        test_data = [["2025-03-11", "Chapinero", "1500000", "2", "2", "45"]]
        filename = "test.csv"

        mock_s3_client.put_object = MagicMock()
        save_to_s3(test_data, filename)

        mock_s3_client.put_object.assert_called_once_with(
            Bucket="bucket-parcial1-2",
            Key=filename,
            Body=b"FechaDescarga,Barrio,Valor,NumHabitaciones,NumBanos,mts2\n2025-03-11,Chapinero,1500000,2,2,45",
            ContentType="text/csv"
        )


    def test_extract_data(self):
        html_content = """
        <html>
            <body>
                <a class="listing listing-card" data-location="Chapinero" data-price="$1,500,000" data-floorarea="45">
                    <p data-test="bedrooms" content="2"></p>
                    <p data-test="bathrooms" content="2"></p>
                </a>
            </body>
        </html>
        """
        result = extract_data(html_content)
        expected = [["2025-03-11", "Chapinero", "1500000", "2", "2", 45]]

        # Ignorar la fecha exacta de descarga
        self.assertEqual(result[0][1:], expected[0][1:])

if __name__ == "__main__":
    unittest.main()

