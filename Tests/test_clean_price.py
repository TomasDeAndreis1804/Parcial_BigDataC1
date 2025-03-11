import unittest
from Parser.parser import clean_price

class TestCleanPrice(unittest.TestCase):

    def test_clean_price(self):
        """Prueba la limpieza del precio en diferentes formatos"""
        self.assertEqual(clean_price("$1.000.000"), "1000000")
        self.assertEqual(clean_price("USD 500"), "500")
        self.assertEqual(clean_price("COP 200000"), "200000")
        self.assertEqual(clean_price(None), "N/A")

if __name__ == "__main__":
    unittest.main()
