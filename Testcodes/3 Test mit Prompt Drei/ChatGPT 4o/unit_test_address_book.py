import unittest
import os
import sqlite3
from your_module import create_database_file, create_connection, create_table, add_task, update_task, delete_task, view_task_by_name, view_all_tasks, reset_all_tasks

class TestAddressBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment: Create a temporary database for testing."""
        cls.test_db = "./test_address_book.db"
        cls.create_tasks_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        status_id integer NOT NULL
                                    );"""
        cls.conn = create_database_file(cls.test_db)
        if cls.conn:
            create_table(cls.conn, cls.create_tasks_table_sql)

    @classmethod
    def tearDownClass(cls):
        """Clean up: Remove the temporary database."""
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        """Reset the database before each test."""
        reset_all_tasks(self.conn)

    # Positive Test Cases
    def test_add_task_success(self):
        """Test adding a task successfully."""
        result = add_task(self.conn, "John Doe", "1234567890")
        self.assertEqual(result, "John Doe added successfully.")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 1)

    def test_view_task_by_name_success(self):
        """Test viewing a task by name."""
        add_task(self.conn, "Jane Doe", "0987654321")
        task = view_task_by_name(self.conn, "Jane Doe")
        self.assertEqual(task[0][1], "Jane Doe")

    # Edge Cases
    def test_add_task_empty_name(self):
        """Test adding a task with an empty name."""
        result = add_task(self.conn, "", "1234567890")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_add_task_invalid_phone_length(self):
        """Test adding a task with an invalid phone number length."""
        result = add_task(self.conn, "John Doe", "12345")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_not_found(self):
        """Test updating a task that does not exist."""
        result = update_task(self.conn, "Nonexistent", "1111111111")
        self.assertEqual(result, "Error: Nonexistent not found.")

    # Negative Test Cases
    def test_add_duplicate_task(self):
        """Test adding a duplicate task."""
        add_task(self.conn, "John Doe", "1234567890")
        result = add_task(self.conn, "John Doe", "1234567890")
        self.assertEqual(result, "Error: John Doe already exists.")

    def test_delete_task_not_found(self):
        """Test deleting a task that does not exist."""
        result = delete_task(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    def test_view_task_not_found(self):
        """Test viewing a task that does not exist."""
        result = view_task_by_name(self.conn, "Nonexistent")
        self.assertEqual(result, "Error: Nonexistent not found.")

    # Performance Test Cases
    def test_add_large_number_of_tasks(self):
        """Test adding a large number of tasks to measure performance."""
        for i in range(1000):
            name = f"Task{i}"
            number = f"{i:010d}"
            result = add_task(self.conn, name, number)
            self.assertEqual(result, f"{name} added successfully.")

        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 1000)

    def test_reset_all_tasks_performance(self):
        """Test performance of resetting all tasks with many entries."""
        for i in range(1000):
            name = f"Task{i}"
            number = f"{i:010d}"
            add_task(self.conn, name, number)

        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")
        tasks = view_all_tasks(self.conn)
        self.assertEqual(len(tasks), 0)

if __name__ == "__main__":
    unittest.main()