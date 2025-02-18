import unittest
from number_to_words import fetch_words, convert_to_words, convert_number

class TestNumberToWords(unittest.TestCase):
    # Tests for fetch_words
    def test_fetch_words_normal_case(self):
        self.assertEqual(fetch_words("123", 0), "One Hundred Twenty Three ")

    def test_fetch_words_with_suffix(self):
        self.assertEqual(fetch_words("001", 1), "One Thousand")

    def test_fetch_words_zero(self):
        self.assertEqual(fetch_words("000", 0), "Zero")

    def test_fetch_words_single_digit(self):
        self.assertEqual(fetch_words("7", 0), "Seven ")

    def test_fetch_words_two_digits(self):
        self.assertEqual(fetch_words("85", 0), "Eighty Five ")

    # Tests for convert_to_words
    def test_convert_to_words_small_number(self):
        self.assertEqual(convert_to_words(123), "One Hundred Twenty Three")

    def test_convert_to_words_large_number(self):
        self.assertEqual(convert_to_words(987654321), 
                         "Nine Hundred Eighty Seven Million Six Hundred Fifty Four Thousand Three Hundred Twenty One")

    def test_convert_to_words_max_supported_digits(self):
        self.assertEqual(convert_to_words(999999999999),
                         "Nine Hundred Ninety Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine")

    def test_convert_to_words_exceeding_max_digits(self):
        self.assertEqual(convert_to_words(1000000000000),
                         "This program supports a maximum of 12 digit numbers.")

    # Tests for convert_number
    def test_convert_number_small_number(self):
        self.assertEqual(convert_number(123), "123 in words is: One Hundred Twenty Three")

    def test_convert_number_large_number(self):
        self.assertEqual(convert_number(10001), "10001 in words is: Ten Thousand One")

    def test_convert_number_zero(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")