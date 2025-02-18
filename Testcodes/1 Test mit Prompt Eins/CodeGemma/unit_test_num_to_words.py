import unittest

class TestNumberConversion(unittest.TestCase):

    def test_fetch_words_zero(self):
        self.assertEqual(fetch_words('000', 0), 'Zero')

    def test_fetch_words_hundreds(self):
        self.assertEqual(fetch_words('001', 0), 'One Hundred')

    def test_fetch_words_tens(self):
        self.assertEqual(fetch_words('012', 0), 'Twelve')

    def test_fetch_words_ones(self):
        self.assertEqual(fetch_words('007', 0), 'Seven')

    def test_fetch_words_hundreds_tens(self):
        self.assertEqual(fetch_words('025', 0), 'Twenty Five')

    def test_fetch_words_hundreds_tens_ones(self):
        self.assertEqual(fetch_words('047', 0), 'Forty Seven')

    def test_fetch_words_with_suffix(self):
        self.assertEqual(fetch_words('001', 1), 'One Thousand')

    def test_convert_to_words_small_number(self):
        self.assertEqual(convert_to_words(123), 'One Hundred Twenty Three')

    def test_convert_to_words_large_number(self):
        self.assertEqual(convert_to_words(1234567890), 'One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety')

    def test_convert_number(self):
        self.assertEqual(convert_number(123), '123 in words is: One Hundred Twenty Three')

if __name__ == '__main__':
    unittest.main()