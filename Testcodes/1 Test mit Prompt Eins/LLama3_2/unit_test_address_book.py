import unittest
from sqlite3 import Error
from your_module import (
    list_of_names,  # assuming the global list is in a separate module
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

class TestAddressBook(unittest.TestCase):

    def setUp(self):
        self.database = r"./Address-Book/address_book.db"
        # Create the table and connection before each test
        self.conn = create_connection(self.database)
        create_table(self.conn, """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );""")
        
    def tearDown(self):
        # Reset the global list of names after each test
        global list_of_names
        list_of_names = []
        self.close_connection()

    def close_connection(self):
        if hasattr('conn', 'close'):
            self.conn.close()

    def test_create_database_file_success(self):
        """Test that create_database_file creates a new SQLite database file."""
        conn = create_database_file(self.database)
        self.assertIsNotNone(conn)

    def test_create_database_file_failure(self):
        """Test that create_database_file fails when creating a non-existent directory."""
        import os
        os.makedirs("/non/existent/dir")
        with self.assertRaises(Error) as e:
            create_database_file("/non/existent/dir")

    def test_create_connection_success(self):
        """Test that create_connection connects to the existing database file."""
        conn = create_connection(self.database)
        self.assertIsNotNone(conn)

    def test_create_connection_failure(self):
        """Test that create_connection fails when creating a new directory with no permissions."""
        import os
        os.makedirs("/new/dir")
        with self.assertRaises(Error) as e:
            create_connection("/new/dir")

    def test_add_task_success(self):
        """Test that add_task adds a new task to the database."""
        conn = self.conn
        name = "John Doe"
        number = "1234567890"
        result = add_task(conn, name, number)
        self.assertIn(name, [student[1] for student in view_all_tasks(conn)])

    def test_add_task_duplicate(self):
        """Test that add_task returns an error when trying to add a duplicate task."""
        conn = self.conn
        name = "John Doe"
        number = "1234567890"
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_empty_name(self):
        """Test that add_task returns an error when the task name is empty."""
        conn = self.conn
        name = ""
        number = "1234567890"
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_empty_number(self):
        """Test that add_task returns an error when the task phone number is empty."""
        conn = self.conn
        name = "John Doe"
        number = ""
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_add_task_invalid_number(self):
        """Test that add_task returns an error when the task phone number is not 10 digits."""
        conn = self.conn
        name = "John Doe"
        number = "12345678901"  # 11 digits instead of 10
        result = add_task(conn, name, number)
        with self.assertRaises(Error) as e:
            add_task(conn, name, number)

    def test_update_task_success(self):
        """Test that update_task updates a task's phone number."""
        conn = self.conn
        name = "John Doe"
        original_number = "1234567890"
        new_number = "9876543210"
        result = add_task(conn, name, original_number)
        updated_result = update_task(conn, name, new_number)
        self.assertIn(name, [student[1] for student in view_all_tasks(conn)])
        # Check that the task's phone number has been updated
        updated_row = view_task_by_name(conn, name)[0]
        self.assertEqual(updated_row[2], new_number)

    def test_update_task_failure(self):
        """Test that update_task returns an error when trying to update a non-existent task."""
        conn = self.conn
        name = "John Doe"
        original_number = "1234567890"
        new_number = "9876543210"
        result = add_task(conn, name, original_number)
        with self.assertRaises(Error) as e:
            update_task(conn, name, new_number)

    def test_delete_task_success(self):
        """Test that delete_task deletes a task from the database."""
        conn = self.conn
        name = "John Doe"
        result = add_task(conn, name, "1234567890")
        deleted_result = delete_task(conn, name)
        self.assertNotIn(name, [student[1] for student in view_all_tasks(conn)])

    def test_delete_task_failure(self):
        """Test that delete_task returns an error when trying to delete a non-existent task."""
        conn = self.conn
        result = delete_task(conn, "John Doe")

    def test_view_all_tasks_success(self):
        """Test that view_all_tasks returns all tasks in the database."""
        conn = self.conn
        name1 = "John Doe"
        name2 = "Jane Smith"
        result1 = add_task(conn, name1, "1234567890")
        result2 = add_task(conn, name2, "0987654321")
        self.assertEqual(len(view_all_tasks(conn)), 2)

    def test_view_all_tasks_failure(self):
        """Test that view_all_tasks returns an error when the database connection is closed."""
        conn = None
        with self.assertRaises(Error) as e:
            view_all_tasks(conn)

    def test_reset_all_tasks_success(self):
        """Test that reset_all_tasks resets the global list of names."""
        global list_of_names
        name1 = "John Doe"
        name2 = "Jane Smith"
        result1 = add_task(list_of_names, name1, "1234567890")
        result2 = add_task(list_of_names, name2, "0987654321")
        reset_all_tasks()
        self.assertEqual(len(list_of_names), 0)

if __name__ == '__main__':
    unittest.main()