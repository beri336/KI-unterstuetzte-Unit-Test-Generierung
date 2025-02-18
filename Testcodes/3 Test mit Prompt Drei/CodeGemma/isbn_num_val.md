# Unit Test Documentation
## Original File: ../ISBN-Validator/isbn_num_val.py

### Model: CodeGemma:7b

<hr>

### Prompt

```
Write a Unit Test for the following Python code. Focus on testing:
- Positive cases (where the function behaves as expected)
- Edge cases (input that might cause failures)
- Negative cases (where the function should throw errors or return incorrect results)
- Performance tests if applicable

Include comments to explain the purpose of each test case.

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
```python
import unittest

class TestValidISBN(unittest.TestCase):

    # Positive cases
    def test_valid_isbn10(self):
        self.assertTrue(valid_ISBN('0307950358'))

    def test_valid_isbn13(self):
        self.assertTrue(valid_ISBN('9780307950359'))

    # Edge cases
    def test_isbn_with_hyphens(self):
        self.assertTrue(valid_ISBN('978-0307950359'))

    def test_isbn_with_spaces(self):
        self.assertTrue(valid_ISBN('978 0307950359'))

    # Negative cases
    def test_invalid_isbn_length(self):
        self.assertFalse(valid_ISBN('123456789'))

    def test_invalid_isbn10_format(self):
        self.assertFalse(valid_ISBN('a307950358'))

    def test_invalid_isbn13_format(self):
        self.assertFalse(valid_ISBN('abcdefghijkl'))

    # Performance tests
    def test_performance(self):
        import timeit
        isbn = '9780307950359'
        number_of_iterations = 10000
        start_time = timeit.default_timer()
        for _ in range(number_of_iterations):
            valid_ISBN(isbn)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        self.assertLess(elapsed_time, 1)

if __name__ == '__main__':
    unittest.main()
```
```