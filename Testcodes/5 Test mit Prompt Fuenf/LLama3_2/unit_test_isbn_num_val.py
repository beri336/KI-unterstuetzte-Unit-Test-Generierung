import unittest
from main import validate_isbn  # Import the function to be tested

class TestValidateISBN(unittest.TestCase):

    def test_valid_normal_input(self):
        # Test with a valid ISBN-10 number
        isbn = '0345453747'
        self.assertEqual(validate_isbn(isbn), "Valid ISBN number.")
        
        # Test with a valid ISBN-13 number
        isbn = '9780262035613'
        self.assertEqual(validate_isbn(isbn), "Valid ISBN number.")

    def test_valid_edge_cases(self):
        # Test with an empty string (should be invalid)
        isbn = ''
        self.assertEqual(validate_isbn(isbn), "Invalid ISBN number.")
        
        # Test with a single digit (should be valid for ISBN-10, but not for ISBN-13)
        isbn = '9'
        self.assertEqual(validate_isbn(isbn), "Valid ISBN number." if len(isbn) == 10 else "Invalid ISBN number.")

    def test_invalid_input_cases(self):
        # Test with a string containing non-digit characters
        isbn = '123abc456'
        self.assertEqual(validate_isbn(isbn), "Invalid ISBN number.")
        
        # Test with an invalid check digit for ISBN-10 (should raise ValueError)
        isbn = '1234567890X'
        with self.assertRaises(ValueError):
            validate_isbn(isbn)

    def test_invalid_input_cases_check_digit(self):
        # Test with an invalid check digit for ISBN-13
        isbn = '9780262035614'
        with self.assertRaises(ValueError):
            validate_isbn(isbn)
        
        # Test with a valid check digit for ISBN-10 but incorrect weight (should raise ValueError)
        isbn = '1234567890X'  # corrected to use X instead of 10
        with self.assertRaises(ValueError):
            validate_isbn(isbn)

if __name__ == '__main__':
    unittest.main()
def valid_ISBN13(isbn):
    """
    Check if the entered number is a valid 13-digit ISBN.
    :param isbn: The ISBN-13 number as a string.
    :return: True if valid, False otherwise.
    """
    # Validate format of the ISBN-13
    if not isbn.isdigit():
        return False

    # Calculate the check digit
    check_digit = 0
    weight = [1, 3] * 6
    for digit, w in zip(isbn[:-1], weight):
        check_digit += int(digit) * w

    check_digit %= 10
    check_digit = (10 - check_digit) % 10

    if str(check_digit) != isbn[-1]:
        raise ValueError("Invalid ISBN-13 number")
    
    return True