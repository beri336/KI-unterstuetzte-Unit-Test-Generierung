# zusammengefuegter Code #

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
        # Setup a test database file
        self.test_db = "test_address_book.db"
        self.conn = create_database_file(self.test_db)
        create_table(
            self.conn,
            """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );""",
        )

    def tearDown(self):
        # Clean up and remove the test database file
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_create_database_file_valid_path(self):
        # Ensure the database file is created and accessible
        self.assertTrue(os.path.exists(self.test_db))

    def test_create_database_file_invalid_path(self):
        # Attempt to create a database with an invalid path
        invalid_path = "/invalid/path/address_book.db"
        conn = create_database_file(invalid_path)
        self.assertIsNone(conn)

    def test_create_connection_valid(self):
        # Ensure connection is successfully created
        conn = create_connection(self.test_db)
        self.assertIsNotNone(conn)

    def test_create_connection_invalid(self):
        # Attempt to connect to a non-existent database
        conn = create_connection("non_existent.db")
        self.assertIsNotNone(conn)

    def test_add_task_valid(self):
        result = add_task(self.conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.")

    def test_add_task_duplicate_name(self):
        add_task(self.conn, "Bob", "1234567890")
        result = add_task(self.conn, "Bob", "0987654321")
        self.assertEqual(result, "Error: Bob already exists.")

    def test_add_task_invalid_number(self):
        result = add_task(self.conn, "Charlie", "12345")
        self.assertEqual(result, "Error: Name cannot be empty, and phone number must be 10 digits.")

    def test_update_task_existing(self):
        add_task(self.conn, "Diana", "1234567890")
        result = update_task(self.conn, "Diana", "0987654321")
        self.assertEqual(result, "Diana updated successfully.")

    def test_update_task_nonexistent(self):
        result = update_task(self.conn, "Eve", "1234567890")
        self.assertEqual(result, "Error: Eve not found.")

    def test_delete_task_existing(self):
        add_task(self.conn, "Frank", "1234567890")
        result = delete_task(self.conn, "Frank")
        self.assertEqual(result, "Frank deleted successfully.")

    def test_delete_task_nonexistent(self):
        result = delete_task(self.conn, "Grace")
        self.assertEqual(result, "Error: Grace not found.")

    def test_view_task_by_name_existing(self):
        add_task(self.conn, "Henry", "1234567890")
        result = view_task_by_name(self.conn, "Henry")
        self.assertTrue(len(result) > 0)

    def test_view_task_by_name_nonexistent(self):
        result = view_task_by_name(self.conn, "Isla")
        self.assertEqual(result, "Error: Isla not found.")

    def test_view_all_tasks(self):
        add_task(self.conn, "Jack", "1234567890")
        add_task(self.conn, "Jill", "0987654321")
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 2)

    def test_reset_all_tasks(self):
        add_task(self.conn, "Kyle", "1234567890")
        reset_all_tasks(self.conn)
        result = view_all_tasks(self.conn)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
