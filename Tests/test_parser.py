import unittest
from Parser.parser import extract_data

class TestParser(unittest.TestCase):

    def test_extract_data(self):
        """Prueba la extracción de datos desde HTML"""
        html_content = """
        <html>
            <body>
                <a class='listing listing-card' data-location='Bogotá' data-price='$1000000' 
                   data-rooms='3' data-bathrooms='2' data-floorarea='50'></a>
            </body>
        </html>
        """
        data = extract_data(html_content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], "Bogotá")  # Verifica la ubicación
        self.assertEqual(data[0][2], "1000000")  # Verifica el precio
        self.assertEqual(data[0][3], "3")  # Verifica habitaciones
        self.assertEqual(data[0][4], "2")  # Verifica baños
        self.assertEqual(data[0][5], "50")  # Verifica área en m²

if __name__ == "__main__":
    unittest.main()
