# zusammengefuegter Code #

import unittest
from sqlite3 import Error
class TestDatabaseFunctions(unittest.TestCase):

    def test_create_database_file_exists(self):
        # Create a temporary file that exists
        db_file = "test.db"
        with open(db_file, "w") as f:
            pass

        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)  # Ensure connection is not None
        with self.assertRaises(Error):  # Check if creation fails for an existing file
            create_database_file(db_file)

    def test_create_database_file_does_not_exist(self):
        # Create a temporary file that doesn't exist
        db_file = "test.db"

        conn = create_database_file(db_file)
        self.assertIsNotNone(conn)  # Ensure connection is not None

    def tearDown(self):
        import os
        # Remove the database file created during testing
        if os.path.exists("test.db"):
            os.remove("test.db")
def test_create_connection_valid_input(self):
    # Create a temporary file
    db_file = "test.db"

    conn = create_connection(db_file)
    self.assertIsNotNone(conn)  # Ensure connection is not None

def test_create_connection_invalid_input(self):
    # Create a database file with an invalid path (should fail)
    db_file = "/invalid/path/test.db"

    conn = create_connection(db_file)
    self.assertIsNone(conn)  # Ensure connection is None
def test_create_table_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""
    create_table(conn, sql_create_tasks_table)
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure table exists

def test_create_table_invalid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = "CREATE TABLE IF NOT EXISTS invalid_table( id integer PRIMARY KEY, name text NOT NULL )"
    with self.assertRaises(Error):  # Check if creation fails for an invalid table
        create_table(conn, sql_create_tasks_table)
def test_add_task_valid_input(self):
    # Create a temporary file
    db_file = "test.db"

    conn = create_connection(db_file)
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertEqual(len(list_of_names), 1)  # Ensure the task is added successfully

def test_add_task_empty_name(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    with self.assertRaises(ValueError):  # Check if the task is not added successfully due to empty name
        add_task(conn, "", "1234567890")

def test_add_task_invalid_phone_number(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    with self.assertRaises(ValueError):  # Check if the task is not added successfully due to invalid phone number
        add_task(conn, "Test Name", "123456")  # Invalid phone number
def test_create_table_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    create_table(conn, sql_create_tasks_table)
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure table exists

def test_create_table_invalid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = "CREATE TABLE IF NOT EXISTS invalid_table( id integer PRIMARY KEY, name text NOT NULL )"
    with self.assertRaises(Error):  # Check if creation fails for an invalid table
        create_table(conn, sql_create_tasks_table)
def test_delete_task_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure the task exists

    delete_task(conn)
    self.assertFalse(conn.execute("SELECT * FROM tasks").fetchone())  # Ensure the task is deleted successfully
def test_update_task_valid_input(self):
    conn = sqlite3.connect(":memory:")  # Create an in-memory database for testing
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                status_id integer NOT NULL
                            );"""

    add_task(conn, "Test Name", "1234567890")
    self.assertTrue(conn.execute("SELECT * FROM tasks").fetchone() is not None)  # Ensure the task exists

    update_task(conn, 1, "Updated Test Name", "1234567890")
    self.assertEqual(conn.execute("SELECT name FROM tasks WHERE id=1").fetchone()[0], "Updated Test Name")  # Ensure the task is updated successfully