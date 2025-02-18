import unittest
from address_book import *

class TestAddressBook(unittest.TestCase):

    # Positive cases
    def test_add_task_positive(self):
        self.assertEqual(add_task(conn, "John Doe", 1234567890), "John Doe added successfully.")

    def test_update_task_positive(self):
        self.assertEqual(update_task(conn, "John Doe", 9876543210), "John Doe updated successfully.")

    def test_delete_task_positive(self):
        self.assertEqual(delete_task(conn, "John Doe"), "John Doe deleted successfully.")

    def test_view_task_by_name_positive(self):
        self.assertIsNotNone(view_task_by_name(conn, "John Doe"))

    def test_view_all_tasks_positive(self):
        self.assertIsNotNone(view_all_tasks(conn))

    # Edge cases
    def test_add_task_with_existing_name(self):
        self.assertEqual(add_task(conn, "John Doe", 1234567890), "Error: John Doe already exists.")

    def test_update_task_with_non_existent_name(self):
        self.assertEqual(update_task(conn, "Nonexistent Name", 9876543210), "Error: Nonexistent Name not found.")

    def test_delete_task_with_non_existent_name(self):
        self.assertEqual(delete_task(conn, "Nonexistent Name"), "Error: Nonexistent Name not found.")

    # Negative cases
    def test_add_task_with_invalid_name(self):
        self.assertEqual(add_task(conn, "", 1234567890), "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_with_invalid_phone_number(self):
        self.assertEqual(add_task(conn, "John Doe", 123456789), "Error: Name cannot be empty, and phone number must be 10 digits.")

    # Performance tests
    def test_add_and_delete_tasks(self):
        for i in range(100):
            add_task(conn, f"Test User {i}", i)
        for i in range(100):
            delete_task(conn, f"Test User {i}")

if __name__ == '__main__':
    unittest.main()