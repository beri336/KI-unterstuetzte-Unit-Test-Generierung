import unittest
from your_module import convert_number, fetch_words, ones, twos, tens, suffixes  # Import the functions and constants from your module

class TestNumberConverter(unittest.TestCase):

    def test_fetch_words(self):
        self.assertEqual(fetch_words('100', 0), 'One Hundred')
        self.assertEqual(fetch_words('20', 1), 'Twenty')
        self.assertEqual(fetch_words('5', 2), 'Five Thousand')

    def test_convert_to_words(self):
        self.assertEqual(convert_to_words(12345), "Twelve Thousand Three Hundred Forty Five")
        self.assertEqual(convert_to_words(1000000), "One Million")

    def test_convert_number(self):
        result = convert_number(12345)
        self.assertIn('in words is:', result)

    def test_fetch_words_hundred_suffix(self):
        self.assertEqual(fetch_words('00', 0), 'Zero Hundred')
        self.assertEqual(fetch_words('100', 1), 'One Thousand')

    def test_convert_to_words_hundred_suffix(self):
        self.assertEqual(convert_to_words(11000), "Eleven Thousand")

    def test_fetch_words_teen_suffix(self):
        self.assertEqual(fetch_words('11', 2), 'Eleven')
        self.assertEqual(fetch_words('21', 3), 'Twenty One')

    def test_convert_to_words_teen_suffix(self):
        self.assertEqual(convert_to_words(1111), "One Thousand Eleven")

    def test_fetch_words_nineteen(self):
        self.assertEqual(fetch_words('19', 0), 'Nineteen')
        self.assertEqual(fetch_words('29', 2), 'Twenty Nine')

    def test_convert_to_words_nineteen_suffix(self):
        self.assertEqual(convert_to_words(1999), "One Thousand Ninety Nine")

    def test_fetch_words_hundred_suffix_with_teens(self):
        self.assertEqual(fetch_words('120', 1), 'One Hundred and Twenty')
        self.assertEqual(fetch_words('130', 2), 'One Hundred and Thirty')

    def test_convert_to_words_hundred_suffix_with_teens(self):
        self.assertEqual(convert_to_words(1120), "One Thousand One Hundred and Twenty")

    def test_fetch_words_single_digit(self):
        self.assertEqual(fetch_words('1', 0), 'One')
        self.assertEqual(fetch_words('5', 2), 'Five')

    def test_convert_to_words_single_digit(self):
        self.assertEqual(convert_to_words(11), "Eleven")
        self.assertEqual(convert_to_words(5), "Five")

if __name__ == '__main__':
    unittest.main()