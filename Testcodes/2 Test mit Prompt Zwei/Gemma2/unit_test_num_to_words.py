import unittest

ones = (
   'Zero', 'One', 'Two', 'Three', 'Four',
   'Five', 'Six', 'Seven', 'Eight', 'Nine'
)

twos = (
   'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
   'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'
)

tens = (
   'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty',
   'Seventy', 'Eighty', 'Ninety', 'Hundred'
)

suffixes = (
   '', 'Thousand', 'Million', 'Billion'
)

def fetch_words(number, index):
    # ... (Your existing fetch_words function)

def convert_to_words(number):
    # ... (Your existing convert_to_words function)

def convert_number(number):
    # ... (Your existing convert_number function)


class TestNumberConversion(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(convert_number(0), "0 in words is: Zero")

    def test_single_digit(self):
        for i in range(1, 10):
            self.assertEqual(convert_number(i), f"{i} in words is: {ones[i]}")

    def test_teens(self):
        self.assertEqual(convert_number(13), "13 in words is: Thirteen")
        self.assertEqual(convert_number(21), "21 in words is: Twenty One")

    def test_hundreds(self):
        self.assertEqual(convert_number(105), "105 in words is: One Hundred Five")
        self.assertEqual(convert_number(234), "234 in words is: Two Hundred Thirty Four")

    def test_thousands(self):
        self.assertEqual(convert_number(1000), "1000 in words is: One Thousand ") 
        self.assertEqual(convert_number(12345), "12345 in words is: Twelve Thousand Three Hundred Forty Five")

    def test_millions(self):
        self.assertEqual(convert_number(1000000), "1000000 in words is: One Million ") 

    def test_billions(self):
        self.assertEqual(convert_number(1000000000), "1000000000 in words is: One Billion ")

    def test_edge_case_max_length(self):
        self.assertEqual(convert_number(9999999999), 
                         "9999999999 in words is: Nine Billion Nine Hundred Ninety Nine Million Nine Hundred Ninety Nine Thousand Nine Hundred Ninety Nine ")

    def test_edge_case_overflow(self):
        with self.assertRaises(ValueError):
            convert_number(100000000000) # Exceeds the supported length 



if __name__ == '__main__':
    unittest.main()