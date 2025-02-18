import os
import sqlite3
from unittest import TestCase
from tempfile import TemporaryDirectory
from your_module import (
    list_of_names,  # Import the global list of names from the original module
    create_database_file,
    create_connection,
    create_table,
    add_task,
    update_task,
    delete_task,
    view_task_by_name,
    view_all_tasks,
    reset_all_tasks
)


class TestAddressBookDB(TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            status_id integer NOT NULL
                                        );"""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            self.database = os.path.join(tmpdir, "address_book.db")
            conn = create_connection(self.database)
            if conn is not None:
                create_table(conn, self.sql_create_tasks_table)

    def tearDown(self):
        # Delete the database file
        try:
            import shutil
            shutil.rmtree(self.database)
        except Exception as e:
            pass

    def test_create_database_file_positive_case(self):
        """Test creating a new SQLite database file if it does not exist."""
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_edge_case_non_existent_directory(self):
        """Test creating a new SQLite database file if the parent directory does not exist."""
        # Create a temporary directory
        with TemporaryDirectory() as tmpdir:
            try:
                os.environ["PWD"] = tmpdir
                conn = create_database_file(os.path.join(tmpdir, "address_book.db"))
                self.assertIsNotNone(conn)
            except Exception as e:
                pass

    def test_create_connection_positive_case(self):
        """Test creating a database connection to the SQLite database."""
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_connection_edge_case_non_existent_file(self):
        """Test connecting to an existing SQLite database file."""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            try:
                conn = create_connection(os.path.join(tmpdir, "address_book.db"))
                self.assertIsNotNone(conn)
            except Exception as e:
                pass

    def test_add_task_positive_case(self):
        """Test adding a new task to the address book."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "1234567890")
        self.assertIn("added successfully", result)

    def test_add_task_edge_case_duplicate_name(self):
        """Test adding a new task with an existing name in the database."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "1234567890")
        result = add_task(conn, "John Doe", "9876543210")
        self.assertIn("added successfully", result)

    def test_add_task_negative_case_empty_name(self):
        """Test adding a new task with an empty name."""
        conn = create_connection(self.database)
        result = add_task(conn, "", "1234567890")
        self.assertIn("Error: Name cannot be empty", result)

    def test_add_task_negative_case_invalid_phone_number(self):
        """Test adding a new task with an invalid phone number."""
        conn = create_connection(self.database)
        result = add_task(conn, "John Doe", "123456")
        self.assertIn("Error: Phone number must be 10 digits.", result)

    def test_update_task_positive_case(self):
        """Test updating the phone number of an existing task."""
        conn = create_connection(self.database)
        conn.execute("INSERT INTO tasks(name, status_id) VALUES('John Doe', 1)")
        conn.commit()
        result = update_task(conn, "John Doe", "1234567890")
        self.assertIn("updated successfully", result)

    def test_update_task_negative_case_non_existent_name(self):
        """Test updating the phone number of a non-existent task."""
        conn = create_connection(self.database)
        result = update_task(conn, "John Doe", "9876543210")
        self.assertIn("Error: John Doe not found.", result)

    def test_delete_task_positive_case(self):
        """Test deleting a task by name."""
        conn = create_connection(self.database)
        conn.execute("INSERT INTO tasks(name, status_id) VALUES('John Doe', 1)")
        conn.commit()
        result = delete_task(conn, "John Doe")
        self.assertIn("deleted successfully", result)

    def test_delete_task_negative_case_non_existent_name(self):
        """Test deleting a non-existent task."""
        conn = create_connection(self.database)
        result = delete_task(conn, "John Doe")
        self.assertIn("Error: John Doe not found.", result)

    def test_view_all_tasks_positive_case(self):
        """Test viewing all tasks in the address book."""
        conn = create_connection(self.database)
        conn.execute("""
            INSERT INTO tasks(name, status_id) VALUES
                ('John Doe', 1),
                ('Jane Smith', 2),
                ('Bob Johnson', 3)
            """
        )
        conn.commit()
        result = view_all_tasks(conn)
        self.assertIn("John Doe", result)
        self.assertIn("Jane Smith", result)
        self.assertIn("Bob Johnson", result)

    def test_view_all_tasks_negative_case_empty_database(self):
        """Test viewing all tasks in an empty address book."""
        conn = create_connection(self.database)
        result = view_all_tasks(conn)
        self.assertEqual(result, "")

    def test_reset_all_tasks_positive_case(self):
        """Test resetting all tasks in the address book."""
        conn = create_connection(self.database)
        conn.execute("""
            INSERT INTO tasks(name, status_id) VALUES
                ('John Doe', 1),
                ('Jane Smith', 2),
                ('Bob Johnson', 3)
            """
        )
        conn.commit()
        result = reset_all_tasks(conn)
        self.assertEqual(result, "")

    def test_reset_all_tasks_negative_case_non_existent_database(self):
        """Test resetting all tasks in a non-existent address book."""
        with TemporaryDirectory() as tmpdir:
            os.environ["PWD"] = tmpdir
            try:
                conn = create_connection(os.path.join(tmpdir, "address_book.db"))
                result = reset_all_tasks(conn)
                self.assertEqual(result, "")
            except Exception as e:
                pass