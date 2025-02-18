import unittest
import sqlite3
import os
from address_book import (
    create_database_file,
    create_connection,
    create_table,
    add_task,
    update_task,
    delete_task,
    view_task_by_name,
    view_all_tasks,
    reset_all_tasks,
)

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database for testing."""
        self.db_file = "./test_address_book.db"
        self.conn = create_database_file(self.db_file)
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Clean up by removing the temporary database file."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    # Test normal cases
    def test_add_task_normal(self):
        """Test adding a valid task."""
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_view_task_by_name_normal(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Bob", "0987654321")
        result = view_task_by_name(self.conn, "Bob")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Bob")
        self.assertEqual(result[0][2], 987654321)

    def test_update_task_normal(self):
        """Test updating an existing task's phone number."""
        add_task(self.conn, "Charlie", "1234567890")
        result = update_task(self.conn, "Charlie", "0987654321")
        self.assertEqual(result, "Charlie updated successfully.")
        updated_task = view_task_by_name(self.conn, "Charlie")
        self.assertEqual(updated_task[0][2], 987654321)

    def test_delete_task_normal(self):
        """Test deleting a task by name."""
        add_task(self.conn, "Daisy", "1234567890")
        result = delete_task(self.conn, "Daisy")
        self.assertEqual(result, "Daisy deleted successfully.")
        result = view_task_by_name(self.conn, "Daisy")
        self.assertEqual(result, "Error: Daisy not found.")

    def test_view_all_tasks_normal(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Eve", "1234567890")
        add_task(self.conn, "Frank", "0987654321")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 2)

    # Test edge cases
    def test_add_task_empty_name(self):
        """Test adding a task with an empty name."""
        result = add_task(self.conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_length(self):
        """Test adding a task with a phone number of invalid length."""
        result = add_task(self.conn, "George", "12345")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_nonexistent(self):
        """Test updating a task that does not exist."""
        result = update_task(self.conn, "Nonexistent", "0987654321")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_delete_task_nonexistent(self):
        """Test deleting a task that does not exist."""
        result = delete_task(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_reset_all_tasks_empty(self):
        """Test resetting all tasks when the table is already empty."""
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        self.assertEqual(view_all_tasks(self.conn), [])

    # Test invalid input cases
    def test_add_task_invalid_type(self):
        """Test adding a task with invalid data types."""
        with self.assertRaises(TypeError):
            add_task(self.conn, 123, 456)

    def test_update_task_invalid_type(self):
        """Test updating a task with invalid data types."""
        with self.assertRaises(TypeError):
            update_task(self.conn, 123, 456)

    def test_delete_task_invalid_type(self):
        """Test deleting a task with invalid data types."""
        with self.assertRaises(TypeError):
            delete_task(self.conn, 123)

if __name__ == "__main__":
    unittest.main()