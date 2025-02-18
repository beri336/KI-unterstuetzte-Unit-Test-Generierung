# Unit Test Documentation
## Original File: ../ISBN-Validator/isbn_num_val.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following Python Code, write comments and add special cases and edge cases:

def valid_ISBN(isbn):
    """
    Check if the entered number is a valid ISBN-10 or ISBN-13.
    :param isbn: The ISBN number as a string.
    :return: True if valid, False otherwise.
    """
    # Remove hyphens and spaces from the ISBN
    isbn = isbn.replace('-', '').replace(' ', '')

    # Check if the length of the ISBN is valid
    if len(isbn) == 10:
        return valid_ISBN10(isbn)
    elif len(isbn) == 13:
        return valid_ISBN13(isbn)
    else:
        return False

def valid_ISBN10(isbn):
    """
    Check if the entered number is a valid 10-digit ISBN.
    :param isbn: The ISBN-10 number as a string.
    :return: True if valid, False otherwise.
    """
    # Validate format of the ISBN-10
    if not isbn[:-1].isdigit() or not isbn[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']:
        return False

    # Calculate the check digit
    check_digit = 0
    weight = 10
    for digit in isbn[:-1]:
        check_digit += int(digit) * weight
        weight -= 1

    check_digit %= 11
    if isbn[-1] == 'X':
        return check_digit == 10
    return str(check_digit) == isbn[-1]

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

    return str(check_digit) == isbn[-1]

def validate_isbn(isbn):
    """
    Validate an ISBN.
    :param isbn: The ISBN number as a string.
    :return: "Valid ISBN number." or "Invalid ISBN number."
    """
    if valid_ISBN(isbn):
        return "Valid ISBN number."
    else:
        return "Invalid ISBN number."
```

<hr>

### Generated Output

```
Here’s a unit test for your `valid_ISBN` and related functions, using Python's `unittest` framework. This test suite includes various cases, including special and edge cases.

### Unit Test Code

```python
import unittest
from your_script_name import valid_ISBN, validate_isbn

class TestISBNValidation(unittest.TestCase):
    def test_valid_ISBN10(self):
        """Test valid ISBN-10 numbers."""
        self.assertTrue(valid_ISBN("0471958697"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("0-471-95869-7"))  # Valid ISBN-10 with hyphens
        self.assertTrue(valid_ISBN("047195869X"))  # Valid ISBN-10 with 'X' as check digit
    
    def test_invalid_ISBN10(self):
        """Test invalid ISBN-10 numbers."""
        self.assertFalse(valid_ISBN("0471958698"))  # Invalid checksum
        self.assertFalse(valid_ISBN("047195869"))  # Too short
        self.assertFalse(valid_ISBN("04719586999"))  # Too long
        self.assertFalse(valid_ISBN("04719586X7"))  # Invalid character placement
    
    def test_valid_ISBN13(self):
        """Test valid ISBN-13 numbers."""
        self.assertTrue(valid_ISBN("9780470059029"))  # Valid ISBN-13
        self.assertTrue(valid_ISBN("978-0-13-149505-0"))  # Valid ISBN-13 with hyphens
        self.assertTrue(valid_ISBN("978 0 471 48648 0"))  # Valid ISBN-13 with spaces
    
    def test_invalid_ISBN13(self):
        """Test invalid ISBN-13 numbers."""
        self.assertFalse(valid_ISBN("9780470059028"))  # Invalid checksum
        self.assertFalse(valid_ISBN("978047005902"))  # Too short
        self.assertFalse(valid_ISBN("97804700590299"))  # Too long
        self.assertFalse(valid_ISBN("97804700X9029"))  # Invalid character
    
    def test_edge_cases(self):
        """Test edge cases for ISBN validation."""
        self.assertFalse(valid_ISBN(""))  # Empty string
        self.assertFalse(valid_ISBN(" "))  # String with only spaces
        self.assertFalse(valid_ISBN("-"))  # Single hyphen
        self.assertFalse(valid_ISBN("1234567890"))  # Valid length but invalid ISBN-10 checksum
        self.assertFalse(valid_ISBN("1234567890123"))  # Valid length but invalid ISBN-13 checksum
    
    def test_validate_isbn_function(self):
        """Test the `validate_isbn` function."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("0471958698"), "Invalid ISBN number.")
        self.assertEqual(validate_isbn("9780470059028"), "Invalid ISBN number.")
    
    def test_invalid_characters(self):
        """Test ISBNs with invalid characters."""
        self.assertFalse(valid_ISBN("04719586#7"))  # Invalid character in ISBN-10
        self.assertFalse(valid_ISBN("97804@0059029"))  # Invalid character in ISBN-13
    
    def test_ISBN_with_mixed_delimiters(self):
        """Test ISBNs with mixed delimiters."""
        self.assertTrue(valid_ISBN("978-0 471-48648 0"))  # Mixed hyphens and spaces
        self.assertFalse(valid_ISBN("978-0 471-48648X"))  # Mixed delimiters with invalid check digit
    
    def test_ISBN_with_leading_trailing_spaces(self):
        """Test ISBNs with leading or trailing spaces."""
        self.assertTrue(valid_ISBN(" 9780470059029 "))  # Valid ISBN-13 with spaces
        self.assertTrue(valid_ISBN(" 0471958697 "))  # Valid ISBN-10 with spaces

if __name__ == "__main__":
    unittest.main()
```

### Explanation of the Test Suite:
1. **Valid ISBN-10**: Tests proper handling of valid 10-digit ISBNs, including checks for formatting and `X` check digit.
2. **Invalid ISBN-10**: Covers common invalid cases, such as incorrect lengths and invalid characters.
3. **Valid ISBN-13**: Verifies the handling of valid 13-digit ISBNs with various formatting (spaces, hyphens).
4. **Invalid ISBN-13**: Includes edge cases like incorrect checksums, wrong lengths, and invalid characters.
5. **Edge Cases**: Tests empty strings, strings with only spaces, and incorrect but valid-length strings.
6. **`validate_isbn` Function**: Checks the output string messages for both valid and invalid ISBNs.
7. **Invalid Characters**: Ensures ISBNs with non-numeric characters (except `X` for ISBN-10) are rejected.
8. **Mixed Delimiters**: Verifies behavior with inconsistent formatting.
9. **Leading and Trailing Spaces**: Ensures the function can handle whitespace properly.

### How to Run:
1. Replace `your_script_name` with the filename where your `valid_ISBN` functions are defined.
2. Save the test code in a separate file (e.g., `test_isbn_validation.py`).
3. Run the test with the following command:
   ```bash
   python -m unittest test_isbn_validation.py
   ```

The test suite ensures the robustness of your ISBN validation functions across a variety of scenarios.
```