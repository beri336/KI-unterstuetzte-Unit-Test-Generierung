import unittest
from isbn_validation import validate_isbn  # Assuming the function is in a file named 'isbn_validation.py'

class TestISBNValidation(unittest.TestCase):

    def test_valid_positive_cases(self):
        """
        Testing positive cases where the ISBN is valid.
        """
        
        # Test valid 10-digit ISBN-10
        self.assertTrue(validate_isbn('0345453747'))
        
        # Test valid 13-digit ISBN-13
        self.assertTrue(validate_isbn('9780345453747'))
        
        # Test valid 10-digit ISBN-10 with check digit 'X'
        self.assertTrue(validate_isbn('0345453747X'))
        
        # Test valid 13-digit ISBN-13 with check digit '0' to '9'
        for i in range(1, 11):
            self.assertTrue(validate_isbn(f'{i}9780345453747'))

    def test_edge_cases(self):
        """
        Testing edge cases.
        """
        
        # Test empty string
        self.assertFalse(validate_isbn(''))
        
        # Test single digit
        self.assertFalse(validate_isbn('1'))
        
        # Test multiple spaces and hyphens
        self.assertTrue(validate_isbn(' 0345453747 '))
        
        # Test invalid ISBN-10 format (non-digit characters)
        self.assertFalse(validate_isbn('034545374X'))
        
        # Test invalid ISBN-13 format (non-digit characters)
        self.assertFalse(validate_isbn('97803454537X'))

    def test_negative_cases(self):
        """
        Testing negative cases where the ISBN is invalid.
        """
        
        # Test valid 10-digit ISBN-10 with invalid check digit
        self.assertFalse(validate_isbn('0345453748'))
        
        # Test valid 13-digit ISBN-13 with invalid check digit
        self.assertFalse(validate_isbn(f'{i}97803454537X' for i in range(1, 11)))
        
        # Test invalid 10-digit ISBN-10 format (too long)
        self.assertFalse(validate_isbn('123456789012'))
        
        # Test valid 13-digit ISBN-13 with invalid length
        self.assertFalse(validate_isbn(f'{i}9780345453747' for i in range(1, 12)))

    def test_performance(self):
        """
        Testing performance.
        """
        
        # Generate a large list of valid and invalid ISBNs to check performance
        import random
        isbn_list = []
        for _ in range(1000):
            isbn_list.append(f'{random.randint(1, 9):02d}978{random.randint(1, 99):03d}')
        
        # Measure time taken by validate_isbn function
        import time
        start_time = time.time()
        for isbn in isbn_list:
            validate_isbn(isbn)
        end_time = time.time()
        print(f"Time taken to validate {len(isbn_list)} ISBNs: {end_time - start_time} seconds")

if __name__ == '__main__':
    unittest.main()