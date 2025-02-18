# Unit Test Documentation
## Original File: ../ISBN-Validator/isbn_num_val.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following given Python Code:


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
Here's a `unittest`-based test suite to validate the `valid_ISBN`, `valid_ISBN10`, `valid_ISBN13`, and `validate_isbn` functions:

```python
import unittest
from your_module import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):

    def test_valid_ISBN10(self):
        """Test cases for valid ISBN-10."""
        self.assertTrue(valid_ISBN10("0471958697"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN10("0-321-14653-0".replace('-', '')), "Should return True for valid ISBN-10 with hyphens.")
        self.assertTrue(valid_ISBN10("0306406152"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN10("359821508X"), "Should return True for valid ISBN-10 ending with X.")
        self.assertFalse(valid_ISBN10("0471958698"), "Should return False for invalid ISBN-10.")
        self.assertFalse(valid_ISBN10("1234567890"), "Should return False for invalid ISBN-10.")
        self.assertFalse(valid_ISBN10("047195869X"), "Should return False for invalid check digit.")

    def test_valid_ISBN13(self):
        """Test cases for valid ISBN-13."""
        self.assertTrue(valid_ISBN13("9780470059029"), "Should return True for valid ISBN-13.")
        self.assertTrue(valid_ISBN13("978-0-13-149505-0".replace('-', '')), "Should return True for valid ISBN-13 with hyphens.")
        self.assertTrue(valid_ISBN13("9780306406157"), "Should return True for valid ISBN-13.")
        self.assertFalse(valid_ISBN13("9780470059028"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN13("9780306406156"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN13("97804700590"), "Should return False for incomplete ISBN-13.")

    def test_valid_ISBN(self):
        """Test cases for the combined ISBN validation function."""
        self.assertTrue(valid_ISBN("0471958697"), "Should return True for valid ISBN-10.")
        self.assertTrue(valid_ISBN("9780470059029"), "Should return True for valid ISBN-13.")
        self.assertFalse(valid_ISBN("123456789"), "Should return False for invalid length.")
        self.assertFalse(valid_ISBN("9780470059028"), "Should return False for invalid ISBN-13.")
        self.assertFalse(valid_ISBN("0471958698"), "Should return False for invalid ISBN-10.")

    def test_validate_isbn(self):
        """Test cases for validate_isbn function."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.", "Should return 'Valid ISBN number.' for valid ISBN-10.")
        self.assertEqual(validate_isbn("9780470059029"), "Valid ISBN number.", "Should return 'Valid ISBN number.' for valid ISBN-13.")
        self.assertEqual(validate_isbn("123456789"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid length.")
        self.assertEqual(validate_isbn("9780470059028"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid ISBN-13.")
        self.assertEqual(validate_isbn("0471958698"), "Invalid ISBN number.", "Should return 'Invalid ISBN number.' for invalid ISBN-10.")

if __name__ == '__main__':
    unittest.main()
```

### Key Points:
1. **Test Cases**:
   - Valid ISBN-10 examples including edge cases (e.g., ending with 'X').
   - Valid ISBN-13 examples including hyphenated formats.
   - Invalid ISBNs to test edge cases and incorrect formats.
2. **`setUp`/`tearDown` Not Needed**: Since the functions don't rely on external state, setup/teardown methods are not required.
3. **Assertions**: Verifies correct behavior for each type of ISBN validation and error handling.

### Usage:
- Replace `your_module` with the actual file name where the code resides.
- Save the test code in a separate file and run it using:
  ```bash
  python -m unittest <test_file_name>.py
  ```
```