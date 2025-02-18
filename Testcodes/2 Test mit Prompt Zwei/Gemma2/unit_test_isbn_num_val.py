import unittest

class TestISBNValidation(unittest.TestCase):

    def test_valid_isbn10(self):
        # Valid ISBN-10
        self.assertTrue(valid_ISBN("0-306-40512-8"))  
        self.assertTrue(valid_ISBN("978-0-306-40512-8"))

    def test_valid_isbn13(self):
        # Valid ISBN-13
        self.assertTrue(valid_ISBN("978-0-306-40512-8")) 

    def test_invalid_length(self):
        # Invalid length (too short)
        self.assertFalse(valid_ISBN("030640512"))
        # Invalid length (too long)
        self.assertFalse(valid_ISBN("978-0-306-40512-8X")) 

    def test_invalid_format_isbn10(self):
        # Incorrect characters in ISBN-10
        self.assertFalse(valid_ISBN("0-306-405abc-8"))  
        self.assertFalse(valid_ISBN("0-306-40512X9")) 

    def test_invalid_format_isbn13(self):
        # Incorrect characters in ISBN-13
        self.assertFalse(valid_ISBN("978-0-306-40512a-8"))  

    def test_empty_string(self):
        # Empty string input
        self.assertFalse(valid_ISBN(""))

    def test_whitespace_only(self):
        # Whitespace only input
        self.assertFalse(valid_ISBN("   ")) 

    def test_non_numeric_characters(self):
        # Non-numeric characters in ISBN
        self.assertFalse(valid_ISBN("978-0-306-40512a"))



if __name__ == '__main__':
    unittest.main()