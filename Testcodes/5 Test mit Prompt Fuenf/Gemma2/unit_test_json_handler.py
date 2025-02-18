import unittest
import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# Import the JSONHandler class from main.py
from main import JSONHandler

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        """
        Set up test environment by creating a temporary file for each test case.
        """
        self.test_file = "test.json"
        # Remove any existing test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """
        Clean up test environment by removing the temporary test file.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # Normal Input Cases

    def test_load_save_data(self):
        """
        Test loading and saving data to a JSON file with normal input.
        """
        handler = JSONHandler(self.test_file)
        sample_data = {"name": "John", "age": 30}
        handler.add_record(sample_data)
        handler.save_data()

        # Reload data from the file
        loaded_handler = JSONHandler(self.test_file)
        self.assertEqual(len(loaded_handler.data["records"]), 1)
        self.assertEqual(loaded_handler.data["records"][0], sample_data)

    def test_add_record(self):
        """
        Test adding a new record to the dataset with normal input.
        """
        handler = JSONHandler(self.test_file)
        sample_data = {"name": "Jane", "age": 25}
        handler.add_record(sample_data)

        self.assertEqual(len(handler.data["records"]), 1)
        self.assertEqual(handler.data["records"][0], sample_data)

    def test_delete_record(self):
        """
        Test deleting a record by ID with normal input.
        """
        handler = JSONHandler(self.test_file)
        sample_data1 = {"name": "Alice", "age": 35, "id": 1}
        sample_data2 = {"name": "Bob", "age": 40, "id": 2}
        handler.add_record(sample_data1)
        handler.add_record(sample_data2)

        handler.delete_record(1)  # Delete record with ID 1

        self.assertEqual(len(handler.data["records"]), 1)
        self.assertEqual(handler.data["records"][0], sample_data2)


    # Edge Cases

    def test_empty_list(self):
        """
        Test handling an empty list of records.
        """
        handler = JSONHandler(self.test_file)
        self.assertEqual(len(handler.data["records"]), 0)

    def test_delete_nonexistent_record(self):
        """
        Test deleting a record that doesn't exist.
        """
        handler = JSONHandler(self.test_file)
        sample_data1 = {"name": "Alice", "age": 35, "id": 1}
        handler.add_record(sample_data1)

        handler.delete_record(2)  # Delete non-existent record
        self.assertEqual(len(handler.data["records"]), 1)


    # Invalid Input Cases (Exception Handling)

    def test_invalid_json(self):
        """
        Test handling an invalid JSON file (should raise a ValueError).
        """
        with open(self.test_file, "w") as f:
            f.write("This is not valid JSON")  
        
        try:
            handler = JSONHandler(self.test_file)
            self.fail("Expected ValueError to be raised")
        except ValueError:
            pass 



    # Additional Tests

    def test_export_to_xml(self):
        """Test exporting data to XML format."""
        handler = JSONHandler(self.test_file)
        sample_data = {"name": "John", "age": 30}
        handler.add_record(sample_data)

        handler.save_data()  
        handler.export_to_xml("test.xml")  
        # Check if the XML file was generated correctly (you'll need a way to validate XML content).



if __name__ == "__main__":
    unittest.main()