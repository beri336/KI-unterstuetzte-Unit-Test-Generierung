import os
import sqlite3
from sqlite3 import Error
import unittest

list_of_names = [] # Global list of names for validation

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            status_id integer NOT NULL
                                        );"""
        self.conn = create_database_file(self.database)
        if self.conn:
            create_table(self.conn, self.sql_create_tasks_table)
        else:
            print("Error: cannot create the database connection.")

    def tearDown(self):
        self.conn.close()

    def test_create_database_file(self):
        self.assertTrue(os.path.exists(self.database))

    def test_create_connection(self):
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_add_task(self):
        name = "John Doe"
        number = "1234567890"
        result = add_task(self.conn, name, number)
        self.assertEqual(result, f"{name} added successfully.")

    def test_add_task_with_existing_name(self):
        name = "John Doe"
        number = "1234567890"
        add_task(self.conn, name, number)
        result = add_task(self.conn, name, number)
        self.assertEqual(result, f"Error: {name} already exists.")

    def test_update_task(self):
        name = "John Doe"
        number = "1234567890"
        add_task(self.conn, name, number)
        result = update_task(self.conn, name, "9876543210")
        self.assertEqual(result, f"{name} updated successfully.")

    def test_delete_task(self):
        name = "John Doe"
        number = "1234567890"
        add_task(self.conn, name, number)
        result = delete_task(self.conn, name)
        self.assertEqual(result, f"{name} deleted successfully.")

    def test_view_task_by_name(self):
        name = "John Doe"
        number = "1234567890"
        add_task(self.conn, name, number)
        result = view_task_by_name(self.conn, name)
        self.assertEqual(result[0][1], name)

    def test_view_all_tasks(self):
        result = view_all_tasks(self.conn)
        self.assertIsNotNone(result)

    def test_reset_all_tasks(self):
        name = "John Doe"
        number = "1234567890"
        add_task(self.conn, name, number)
        result = reset_all_tasks(self.conn)
        self.assertEqual(result, "All entries have been deleted successfully.")

if __name__ == '__main__':
    unittest.main()