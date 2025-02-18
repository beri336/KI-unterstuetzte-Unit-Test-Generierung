import unittest
from main import *

class TestAddressBook(unittest.TestCase):

    def test_add_task_valid_input(self):
        conn = create_connection(database)
        result = add_task(conn, "John Doe", 1234567890)
        self.assertEqual(result, "John Doe added successfully.")

    def test_add_task_invalid_name(self):
        conn = create_connection(database)
        result = add_task(conn, "", 1234567890)
        self.assertEqual(result, "Error: Name cannot be empty.")

    def test_add_task_invalid_number(self):
        conn = create_connection(database)
        result = add_task(conn, "John Doe", "invalid_number")
        self.assertEqual(result, "Error: Phone number must be 10 digits.")

    def test_add_task_duplicate_name(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = add_task(conn, "John Doe", 1234567890)
        self.assertEqual(result, f"Error: John Doe already exists.")

    def test_update_task_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = update_task(conn, "John Doe", 9876543210)
        self.assertEqual(result, "John Doe updated successfully.")

    def test_update_task_invalid_name(self):
        conn = create_connection(database)
        result = update_task(conn, "Nonexistent Name", 9876543210)
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_delete_task_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = delete_task(conn, "John Doe")
        self.assertEqual(result, "John Doe deleted successfully.")

    def test_delete_task_invalid_name(self):
        conn = create_connection(database)
        result = delete_task(conn, "Nonexistent Name")
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_view_task_by_name_valid_input(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = view_task_by_name(conn, "John Doe")
        self.assertEqual(result[0][1], "John Doe")

    def test_view_task_by_name_invalid_name(self):
        conn = create_connection(database)
        result = view_task_by_name(conn, "Nonexistent Name")
        self.assertEqual(result, "Error: Nonexistent Name not found.")

    def test_view_all_tasks(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        add_task(conn, "Jane Doe", 9876543210)
        result = view_all_tasks(conn)
        self.assertEqual(len(result), 2)

    def test_reset_all_tasks(self):
        conn = create_connection(database)
        add_task(conn, "John Doe", 1234567890)
        result = reset_all_tasks(conn)
        self.assertEqual(result, "All entries have been deleted successfully.")

if __name__ == '__main__':
    unittest.main()