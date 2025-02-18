import unittest
import os
import sqlite3
from your_script_name import (
    create_database_file, create_connection, create_table, add_task, update_task, 
    delete_task, view_task_by_name, view_all_tasks, reset_all_tasks
)

class TestAddressBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the database for testing."""
        cls.test_db = "./test_address_book.db"
        cls.conn = create_database_file(cls.test_db)
        cls.create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                  );"""
        create_table(cls.conn, cls.create_table_sql)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    
    def setUp(self):
        """Reset the database before each test."""
        reset_all_tasks(self.conn)
    
    def test_create_database_file(self):
        """Test creating a new database file."""
        test_file = "./new_test_db.db"
        conn = create_database_file(test_file)
        self.assertTrue(os.path.exists(test_file))
        conn.close()
        os.remove(test_file)
    
    def test_add_task_success(self):
        """Test adding a new task successfully."""
        response = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(response, "Alice added successfully.")
    
    def test_add_task_duplicate_name(self):
        """Test adding a task with a duplicate name."""
        add_task(self.conn, "Alice", "1234567890")
        response = add_task(self.conn, "Alice", "0987654321")
        self.assertEqual(response, "Error: Alice already exists.")
    
    def test_add_task_invalid_phone_number(self):
        """Test adding a task with an invalid phone number."""
        response = add_task(self.conn, "Alice", "12345")
        self.assertEqual(response, "Error: Name cannot be empty, and phone number must be 10 digits.")
    
    def test_update_task_success(self):
        """Test updating an existing task."""
        add_task(self.conn, "Alice", "1234567890")
        response = update_task(self.conn, "Alice", "0987654321")
        self.assertEqual(response, "Alice updated successfully.")
    
    def test_update_task_not_found(self):
        """Test updating a task that does not exist."""
        response = update_task(self.conn, "Bob", "0987654321")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_delete_task_success(self):
        """Test deleting an existing task."""
        add_task(self.conn, "Alice", "1234567890")
        response = delete_task(self.conn, "Alice")
        self.assertEqual(response, "Alice deleted successfully.")
    
    def test_delete_task_not_found(self):
        """Test deleting a task that does not exist."""
        response = delete_task(self.conn, "Bob")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_view_task_by_name_success(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Alice", "1234567890")
        result = view_task_by_name(self.conn, "Alice")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Alice")
    
    def test_view_task_by_name_not_found(self):
        """Test viewing a task that does not exist."""
        response = view_task_by_name(self.conn, "Bob")
        self.assertEqual(response, "Error: Bob not found.")
    
    def test_view_all_tasks(self):
        """Test viewing all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        add_task(self.conn, "Bob", "0987654321")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 2)
    
    def test_reset_all_tasks(self):
        """Test resetting all tasks."""
        add_task(self.conn, "Alice", "1234567890")
        response = reset_all_tasks(self.conn)
        self.assertEqual(response, "All entries have been deleted successfully.")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()