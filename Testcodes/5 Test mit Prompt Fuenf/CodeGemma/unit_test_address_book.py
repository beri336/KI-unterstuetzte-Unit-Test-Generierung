import unittest
from main import *

class TestAddressBook(unittest.TestCase):

    # Test normal input cases with common values
    def test_add_task_normal(self):
        conn = create_connection(database)
        result = add_task(conn, "John Doe", 1234567890)
        self.assertEqual(result, "John Doe added successfully.")

    def test_update_task_normal(self):
        conn = create_connection(database)
        add_task(conn, "Jane Smith", 2345678901)
        result = update_task(conn, "Jane Smith", 3456789012)
        self.assertEqual(result, "Jane Smith updated successfully.")

    def test_view_task_by_name_normal(self):
        conn = create_connection(database)
        add_task(conn, "David Lee", 4567890123)
        result = view_task_by_name(conn, "David Lee")
        self.assertIsNotNone(result)

    # Test edge cases
    def test_add_task_empty_name(self):
        conn = create_connection(database)
        result = add_task(conn, "", 1234567890)
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_non_existent_name(self):
        conn = create_connection(database)
        result = update_task(conn, "NonExistent", 1234567890)
        self.assertEqual(result, "Error: NonExistent not found.")

    def test_delete_task_non_existent_name(self):
        conn = create_connection(database)
        result = delete_task(conn, "NonExistent")
        self.assertEqual(result, "Error: NonExistent not found.")

    # Test invalid input cases that should raise exceptions
    def test_add_task_invalid_phone_number(self):
        conn = create_connection(database)
        with self.assertRaises(ValueError):
            add_task(conn, "John Doe", "invalid_phone_number")

    def test_update_task_invalid_phone_number(self):
        conn = create_connection(database)
        add_task(conn, "Jane Smith", 2345678901)
        with self.assertRaises(ValueError):
            update_task(conn, "Jane Smith", "invalid_phone_number")

    def test_reset_all_tasks_invalid_database_path(self):
        with self.assertRaises(Error):
            reset_all_tasks("invalid_database_path")


if __name__ == '__main__':
    unittest.main()