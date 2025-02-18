import unittest
import sqlite3
import os
from your_module import create_database_file, create_connection, create_table, add_task, update_task, delete_task, view_task_by_name, view_all_tasks, reset_all_tasks

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database for testing."""
        self.test_db = "./test_address_book.db"
        self.conn = create_database_file(self.test_db)
        self.assertIsNotNone(self.conn, "Database connection should not be None.")
        
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );"""
        create_table(self.conn, sql_create_tasks_table)

    def tearDown(self):
        """Clean up the test database."""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_task(self):
        """Test adding a task to the database."""
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")
        
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Error: Alice already exists.")

    def test_view_task_by_name(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Bob", "0987654321")
        result = view_task_by_name(self.conn, "Bob")
        self.assertTrue(len(result) > 0, "Task should exist.")
        self.assertEqual(result[0][1], "Bob", "Task name should match.")

        result = view_task_by_name(self.conn, "Charlie")
        self.assertEqual(result, "Error: Charlie not found.")

    def test_view_all_tasks(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 2, "There should be two tasks in the database.")

    def test_update_task(self):
        """Test updating a task."""
        add_task(self.conn, "Alice", "1234567890")
        result = update_task(self.conn, "Alice", "0987654321")
        self.assertEqual(result, "Alice updated successfully.")

        result = update_task(self.conn, "Charlie", "0987654321")
        self.assertEqual(result, "Error: Charlie not found.")

    def test_delete_task(self):
        """Test deleting a task."""
        add_task(self.conn, "Alice", "1234567890")
        result = delete_task(self.conn, "Alice")
        self.assertEqual(result, "Alice deleted successfully.")

        result = delete_task(self.conn, "Alice")
        self.assertEqual(result, "Error: Alice not found.")

    def test_reset_all_tasks(self):
        """Test resetting all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 0, "Database should be empty after reset.")

if __name__ == '__main__':
    unittest.main()