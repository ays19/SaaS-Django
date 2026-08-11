from django.test import TestCase
from helpers.numbers import shorten_number

class NumberHelperTests(TestCase):
    def test_shorten_number_thousands(self):
        self.assertEqual(shorten_number(1000), "1K")
        self.assertEqual(shorten_number(1500), "1.5K")
        self.assertEqual(shorten_number(9999), "10K")

    def test_shorten_number_millions(self):
        self.assertEqual(shorten_number(1000000), "1M")
        self.assertEqual(shorten_number(2500000), "2.5M")
        self.assertEqual(shorten_number(10000000), "10M")

    def test_shorten_number_billions(self):
        self.assertEqual(shorten_number(1000000000), "1B")
        self.assertEqual(shorten_number(1200000000), "1.2B")

    def test_shorten_number_small(self):
        self.assertEqual(shorten_number(500), "500")
        self.assertEqual(shorten_number(0), "0")
        self.assertEqual(shorten_number(-100), "-100")
        
    def test_shorten_number_invalid_input(self):
        self.assertEqual(shorten_number("invalid"), "invalid")
        self.assertEqual(shorten_number(None), "None")
