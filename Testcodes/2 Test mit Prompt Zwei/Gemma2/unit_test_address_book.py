import unittest
import sqlite3
from unittest.mock import patch
from your_module import (create_database_file, 
                        create_connection, 
                        create_table, 
                        add_task, 
                        update_task, 
                        delete_task, 
                        view_task_by_name, 
                        view_all_tasks, 
                        reset_all_tasks) # Import your functions


class TestAddressBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary database file for testing
        cls.database = r"./test_address_book.db"
        cls.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    @classmethod
    def tearDownClass(cls):
        # Delete the temporary database file after testing
        os.remove(cls.database) 

    def test_create_database_file(self):
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_exists(self):
        # Test when the database file already exists
        conn = create_database_file(self.database)  
        with self.assertRaises(sqlite3.Error): 
            create_database_file(self.database) 

    def test_create_connection(self):
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_table(self):
        # Connect to the database
        conn = sqlite3.connect(self.database)
        create_table(conn, self.sql_create_tasks_table)
        # Check if the table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_add_task(self):
        conn = create_connection(self.database)
        # Add a new task
        result = add_task(conn, "John Doe", "1234567890")
        self.assertEqual(result, "John Doe added successfully.")
        # Check if the task exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE name='John Doe'")
        rows = cursor.fetchall()
        self.assertIsNotNone(rows)

    def test_add_task_duplicate(self):
        conn = create_connection(self.database)
        # Add a duplicate task
        result = add_task(conn, "John Doe", "1234567890")
        self.assertEqual(result, "Error: John Doe already exists.")

    def test_add_task_invalid_name(self):
        conn = create_connection(self.database)
        # Add a task with an empty name
        result = add_task(conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_number(self):
        conn = create_connection(self.database)
        # Add a task with an invalid phone number length
        result = add_task(conn, "Jane Doe", "123456789")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task(self):
        conn = create_connection(self.database)
        # Add a task initially
        add_task(conn, "Alice", "9876543210")

        # Update the task
        result = update_task(conn, "Alice", "5551234567")
        self.assertEqual(result, "Task updated successfully.")

    def test_delete_task(self):
        conn = create_connection(self.database)
        # Add a task initially
        add_task(conn, "Bob", "0987654321")

        # Delete the task
        result = delete_task(conn, "Bob")
        self.assertEqual(result, "Task deleted successfully.")


    def test_view_task_by_name(self):
        conn = create_connection(self.database)
        add_task(conn, "Charlie", "1112223333")

        # View the task by name
        result = view_task_by_name(conn, "Charlie")
        self.assertIsNotNone(result)

    def test_view_all_tasks(self):
        conn = create_connection(self.database)
        add_task(conn, "David", "4445556666")
        add_task(conn, "Emily", "7778889999")

        # View all tasks
        result = view_all_tasks(conn)
        self.assertIsNotNone(result)

    def test_reset_all_entries(self):
        conn = create_connection(self.database)
        add_task(conn, "Frank", "2223334444")

        # Reset all entries
        result = reset_all_tasks(conn)
        self.assertEqual(result, "All entries have been deleted successfully.")



if __name__ == '__main__':
    unittest.main()