import unittest

class TestFetchWords(unittest.TestCase):

    def test_fetch_words_zero(self):
        self.assertEqual(fetch_words('000', 0), 'Zero')

    def test_fetch_words_one_hundred(self):
        self.assertEqual(fetch_words('001', 0), 'One Hundred')

    def test_fetch_words_twenty_three(self):
        self.assertEqual(fetch_words('023', 0), 'Twenty Three')

    def test_fetch_words_exception(self):
        with self.assertRaises(ValueError):
            fetch_words('abc', 0)


class TestConvertToWords(unittest.TestCase):

    def test_convert_to_words_four_digits(self):
        self.assertEqual(convert_to_words(1234), 'One Thousand Two Hundred Thirty Four')

    def test_convert_to_words_ten_digits(self):
        self.assertEqual(convert_to_words(1234567890), 'One Billion Two Hundred Thirty Four Million Five Hundred Sixty Seven Thousand Eight Hundred Ninety')

    def test_convert_to_words_exception(self):
        with self.assertRaises(ValueError):
            convert_to_words('abc')


class TestConvertNumber(unittest.TestCase):

    def test_convert_number_to_words(self):
        self.assertEqual(convert_number(1234), '1234 in words is: One Thousand Two Hundred Thirty Four')

    def test_convert_number_to_words_exception(self):
        with self.assertRaises(ValueError):
            convert_number('abc')