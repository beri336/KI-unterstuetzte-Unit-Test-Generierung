import unittest
from unittest.mock import patch
import os
import sqlite3

# Import the functions from the given code
from address_book import create_database_file, create_connection, add_task, update_task, delete_task, view_task_by_name, view_all_tasks, reset_all_tasks

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.conn = create_database_file(self.database)

    def tearDown(self):
        if os.path.exists(self.database):
            os.remove(self.database)

    def test_create_database_file(self):
        self.assertIsNotNone(self.conn)

    def test_add_task(self):
        result = add_task(self.conn, "John Doe", 1234567890)
        self.assertEqual(result, "John Doe added successfully.")

    def test_update_task(self):
        add_task(self.conn, "Jane Doe", 2345678901)
        result = update_task(self.conn, "Jane Doe", 3456789012)
        self.assertEqual(result, "Jane Doe updated successfully.")

    def test_delete_task(self):
        add_task(self.conn, "John Smith", 4567890123)
        result = delete_task(self.conn, "John Smith")
        self.assertEqual(result, "John Smith deleted successfully.")

    def test_view_task_by_name(self):
        add_task(self.conn, "Emily Jones", 5678901234)
        result = view_task_by_name(self.conn, "Emily Jones")
        self.assertIsNotNone(result)

    def test_view_all_tasks(self):
        add_task(self.conn, "Mark Williams", 6789012345)
        result = view_all_tasks(self.conn)
        self.assertIsNotNone(result)

    def test_reset_all_tasks(self):
        add_task(self.conn, "Sarah Taylor", 7890123456)
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")

if __name__ == '__main__':
    unittest.main()