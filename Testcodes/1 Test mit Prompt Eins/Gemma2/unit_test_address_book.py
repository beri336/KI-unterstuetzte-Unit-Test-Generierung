import unittest
from sqlite3 import Error  
from your_module import *  # Import your module here 

class TestAddressBook(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database = r"./test_address_book.db"  # Use a temporary database for testing
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    status_id integer NOT NULL
                                );"""

        try:
            conn = create_database_file(cls.database) 
            if conn:
                create_table(conn, sql_create_tasks_table)
                conn.close()  # Close the connection after creating the table
            else:
                print("Error: cannot create the database connection.")
        except Error as e:
            print(f"Error creating test database: {e}")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.database) # Remove the temporary database after testing

    def test_create_database_file(self):
        conn = create_database_file(self.database)  # Test with a different filename
        self.assertIsNotNone(conn, "Database connection should not be None")
        conn.close() 

    def test_add_task(self):
        conn = create_connection(self.database) 
        result = add_task(conn, "Alice", "1234567890")
        self.assertEqual(result, "Alice added successfully.", "Task should be added successfully")
        conn.close()

    def test_add_duplicate_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "Bob", "9876543210")  
        result = add_task(conn, "Bob", "1234567890")
        self.assertEqual(result, "Error: Bob already exists.", "Duplicate task should not be added") 
        conn.close()

    def test_update_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "Charlie", "1234567890")  
        result = update_task(conn, "Charlie", "9876543210")
        self.assertEqual(result, "Charlie updated successfully.", "Task should be updated") 
        conn.close()

    def test_delete_task(self):
        conn = create_connection(self.database) 
        add_task(conn, "David", "1234567890")  
        result = delete_task(conn, "David")
        self.assertEqual(result, "David deleted successfully.", "Task should be deleted") 
        conn.close()

    def test_view_all_tasks(self):
        conn = create_connection(self.database) 
        add_task(conn, "Emily", "1234567890")  
        result = view_all_tasks(conn)
        self.assertIsNotNone(result) 
        conn.close()

    def test_view_task_by_name(self):
        conn = create_connection(self.database) 
        add_task(conn, "Frank", "1234567890")  
        result = view_task_by_name(conn, "Frank")
        self.assertIsNotNone(result) 
        conn.close()

    # Add more tests as needed



if __name__ == '__main__':
    unittest.main()