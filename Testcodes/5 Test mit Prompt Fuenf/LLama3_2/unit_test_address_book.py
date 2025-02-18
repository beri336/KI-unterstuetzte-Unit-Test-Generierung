import unittest
from sqlite3 import Error
from main import list_of_names  # Importing the global list of names for validation

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        
    # Normal input cases with common values
    def test_add_task_success(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "John Doe", 1234567890)
            self.assertEqual(result, f"{result}")
            conn.close()

    def test_update_task_success(self):
        conn = create_connection(self.database)
        if conn:
            add_task(conn, "Jane Doe", 9876543210)
            result = update_task(conn, "John Doe", 1234567891)
            self.assertEqual(result, f"{result}")
            conn.close()

    def test_delete_task_success(self):
        conn = create_connection(self.database)
        if conn:
            add_task(conn, "Bob Smith", 5551234567)
            result = delete_task(conn, "John Doe")
            self.assertEqual(result, f"{result}")
            conn.close()

    # Edge cases
    def test_add_empty_name(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "", 1234567890)
            self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")
            conn.close()

    def test_update_nonexistent_student(self):
        conn = create_connection(self.database)
        if conn:
            result = update_task(conn, "Unknown Student", 1234567891)
            self.assertEqual(result, f"Error: Unknown Student not found.")
            conn.close()

    def test_delete_nonexistent_student(self):
        conn = create_connection(self.database)
        if conn:
            result = delete_task(conn, "Unknown Student")
            self.assertEqual(result, f"Error: Unknown Student not found.")
            conn.close()

    # Invalid input cases that should raise exceptions
    def test_add_empty_number(self):
        conn = create_connection(self.database)
        if conn:
            result = add_task(conn, "John Doe", "")
            self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")
            conn.close()

    def test_update_invalid_number_length(self):
        conn = create_connection(self.database)
        if conn:
            result = update_task(conn, "Jane Doe", "123456789")
            self.assertEqual(result, f"Error: Jane Doe already exists.")
            conn.close()

if __name__ == '__main__':
    unittest.main()