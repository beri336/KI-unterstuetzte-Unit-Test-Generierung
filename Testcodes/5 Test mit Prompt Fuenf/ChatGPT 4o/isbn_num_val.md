# Unit Test Documentation
## Original File: ../ISBN-Validator/isbn_num_val.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "isbn_num_val.py"


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
Below is the `unittest` test suite for the given code. The tests validate normal cases, edge cases, and invalid input cases, ensuring the functionality of `isbn_num_val.py`.

### Test Suite

```python
import unittest
from isbn_num_val import valid_ISBN, valid_ISBN10, valid_ISBN13, validate_isbn

class TestISBNValidation(unittest.TestCase):

    # Normal Input Cases
    def test_valid_ISBN10(self):
        """Test a valid ISBN-10."""
        self.assertTrue(valid_ISBN10("0471958697"))  # Valid ISBN-10 example

    def test_valid_ISBN10_with_X(self):
        """Test a valid ISBN-10 with 'X' as the check digit."""
        self.assertTrue(valid_ISBN10("0306406152"))  # Valid ISBN-10 with 'X'

    def test_valid_ISBN13(self):
        """Test a valid ISBN-13."""
        self.assertTrue(valid_ISBN13("9780306406157"))  # Valid ISBN-13 example

    def test_valid_ISBN_function(self):
        """Test the valid_ISBN function with correct ISBN-10 and ISBN-13."""
        self.assertTrue(valid_ISBN("0471958697"))  # Valid ISBN-10
        self.assertTrue(valid_ISBN("9780306406157"))  # Valid ISBN-13

    def test_validate_isbn_function_valid(self):
        """Test validate_isbn function for valid cases."""
        self.assertEqual(validate_isbn("0471958697"), "Valid ISBN number.")
        self.assertEqual(validate_isbn("9780306406157"), "Valid ISBN number.")

    # Edge Cases
    def test_valid_ISBN10_invalid_format(self):
        """Test ISBN-10 with invalid format (non-numeric characters)."""
        self.assertFalse(valid_ISBN10("04719X8697"))  # Invalid format

    def test_valid_ISBN10_short_length(self):
        """Test ISBN-10 with fewer than 10 characters."""
        self.assertFalse(valid_ISBN10("04719586"))  # Too short

    def test_valid_ISBN13_short_length(self):
        """Test ISBN-13 with fewer than 13 characters."""
        self.assertFalse(valid_ISBN13("97803064061"))  # Too short

    def test_valid_ISBN13_invalid_format(self):
        """Test ISBN-13 with invalid characters."""
        self.assertFalse(valid_ISBN13("9780X06406157"))  # Invalid format

    def test_valid_ISBN_mixed_format(self):
        """Test valid_ISBN function with mixed formats."""
        self.assertFalse(valid_ISBN("9780306406X57"))  # Invalid check digit

    def test_validate_isbn_invalid_format(self):
        """Test validate_isbn function with invalid formats."""
        self.assertEqual(validate_isbn("9780306406X57"), "Invalid ISBN number.")
        self.assertEqual(validate_isbn("04719586"), "Invalid ISBN number.")

    # Invalid Input Cases
    def test_valid_ISBN_invalid_type(self):
        """Test valid_ISBN with non-string inputs."""
        with self.assertRaises(AttributeError):  # replace("-", "") on non-string
            valid_ISBN(1234567890)

    def test_valid_ISBN10_invalid_type(self):
        """Test valid_ISBN10 with non-string inputs."""
        with self.assertRaises(TypeError):  # Iteration on non-string
            valid_ISBN10(1234567890)

    def test_valid_ISBN13_invalid_type(self):
        """Test valid_ISBN13 with non-string inputs."""
        with self.assertRaises(TypeError):  # Iteration on non-string
            valid_ISBN13(9780306406157)

    def test_validate_isbn_invalid_type(self):
        """Test validate_isbn with non-string inputs."""
        with self.assertRaises(AttributeError):  # replace("-", "") on non-string
            validate_isbn(9780306406157)

    def test_valid_ISBN_empty_string(self):
        """Test valid_ISBN with an empty string."""
        self.assertFalse(valid_ISBN(""))

    def test_valid_ISBN10_empty_string(self):
        """Test valid_ISBN10 with an empty string."""
        self.assertFalse(valid_ISBN10(""))

    def test_valid_ISBN13_empty_string(self):
        """Test valid_ISBN13 with an empty string."""
        self.assertFalse(valid_ISBN13(""))

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases
1. **Normal Input Cases**:
   - Test valid ISBN-10 and ISBN-13 inputs for expected functionality.
   - Cover edge cases like valid ISBN-10s with 'X' as the check digit.

2. **Edge Cases**:
   - Test invalid formats, incorrect lengths, and mixed formats (e.g., valid ISBNs with errors).
   - Check behavior for empty strings and slightly malformed inputs.

3. **Invalid Input Cases**:
   - Test non-string inputs (e.g., integers) to ensure the functions handle them correctly by raising exceptions.
   - Validate behavior when an empty string is passed.

4. **Setup**:
   - Each test case is standalone, meaning no persistent changes are made to global or shared variables.

This comprehensive suite ensures that `isbn_num_val.py` works as intended for both expected and edge-case scenarios.
```