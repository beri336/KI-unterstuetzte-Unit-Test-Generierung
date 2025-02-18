import unittest

from main import valid_ISBN, valid_ISBN10, valid_ISBN13

class TestISBNValidation(unittest.TestCase):

    def test_valid_isbn10(self):
      """Test valid 10-digit ISBN."""
      self.assertTrue(valid_ISBN10("978026540448"))  # Example valid ISBN-10

    def test_invalid_isbn10(self):
      """Test invalid 10-digit ISBN (wrong format)."""
      self.assertFalse(valid_ISBN10("978026540448x"))  
      self.assertFalse(valid_ISBN10("978-0265-40448")) 

    def test_valid_isbn13(self):
      """Test valid 13-digit ISBN."""
      self.assertTrue(valid_ISBN13("978-026540448-6"))  # Example valid ISBN-13

    def test_invalid_isbn13(self):
      """Test invalid 13-digit ISBN (wrong format)."""
      self.assertFalse(valid_ISBN13("9780265404486X"))
      self.assertFalse(valid_ISBN13("978-0265-40448-7-6"))

    def test_valid_isbn(self):
      """Test valid ISBN (both 10 and 13)."""
      self.assertTrue(valid_ISBN("978-026540448-6"))  
      self.assertTrue(valid_ISBN("978026540448"))

    def test_invalid_isbn(self):
      """Test invalid ISBN (wrong length)."""
      self.assertFalse(valid_ISBN("123456789")) 
      self.assertFalse(valid_ISBN("978-026540448-66"))

    def test_validate_isbn(self):
      """Test the function validate_isbn."""
      self.assertEqual(validate_isbn("978-026540448-6"), "Valid ISBN number.") 
      self.assertEqual(validate_isbn("123456789"), "Invalid ISBN number.")

if __name__ == '__main__':
    unittest.main()