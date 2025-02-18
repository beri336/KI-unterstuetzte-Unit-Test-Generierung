import unittest

class TestNumberConversion(unittest.TestCase):

    def test_ones(self):
        for i in range(10):
            self.assertEqual(fetch_words(str(i), 0), ones[i])

    def test_twos(self):
        for i in range(10):
            self.assertEqual(fetch_words(str(i), 0), twos[i])

    def test_tens(self):
        for i in range(10):
            self.assertEqual(fetch_words(str(i), 0), tens[i])

    def test_suffixes(self):
        self.assertEqual(fetch_words('000', 0), '')
        self.assertEqual(fetch_words('000', 1), 'Thousand')
        self.assertEqual(fetch_words('000', 2), 'Million')
        self.assertEqual(fetch_words('000', 3), 'Billion')

    def test_fetch_words(self):
        self.assertEqual(fetch_words('123', 0), 'One Hundred Twenty Three')
        self.assertEqual(fetch_words('000', 0), 'Zero')
        self.assertEqual(fetch_words('100', 0), 'One Hundred')
        self.assertEqual(fetch_words('20', 0), 'Twenty')

    def test_convert_to_words(self):
        self.assertEqual(convert_to_words(123456789), 'One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine')
        self.assertEqual(convert_to_words(12345), 'Twelve Thousand Three Hundred Forty Five')
        self.assertEqual(convert_to_words(1000), 'One Thousand')
        self.assertEqual(convert_to_words(0), 'Zero')

    def test_convert_number(self):
        self.assertEqual(convert_number(123456789), '123456789 in words is: One Hundred Twenty Three Million Four Hundred Fifty Six Thousand Seven Hundred Eighty Nine')
        self.assertEqual(convert_number(12345), '12345 in words is: Twelve Thousand Three Hundred Forty Five')
        self.assertEqual(convert_number(1000), '1000 in words is: One Thousand')
        self.assertEqual(convert_number(0), '0 in words is: Zero')

if __name__ == '__main__':
    unittest.main()