import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# Assuming the provided code is in a file named "main.py"
import unittest

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        """Sets up the test environment by creating a temporary JSON file."""
        self.file_path = "./test.json" 
        os.makedirs("./test", exist_ok=True)  # Create a directory for testing

    def tearDown(self):
        """Clears up the test environment by deleting the temporary JSON file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path) 

    def test_jsonhandler_init_valid_input(self):
        """Tests initialization with a valid JSON file path."""
        handler = JSONHandler(self.file_path)  
        self.assertEqual(handler.file_path, self.file_path)

    def test_jsonhandler_init_nonexistent_file(self):
        """Tests initialization with a non-existent file path."""
        handler = JSONHandler(self.file_path) 
        with open(self.file_path, "r") as f:  # Trying to read the nonexistent file
            pass # This should raise an error if the handler didn't create the default structure

    def test_jsonhandler_load_data_empty_file(self):
        """Tests loading data from an empty JSON file."""
        with open(self.file_path, "w") as f:
            pass  # Create an empty file
        handler = JSONHandler(self.file_path) 
        self.assertEqual(handler.data, {"records": []})

    def test_jsonhandler_load_data_valid_json(self):
        """Tests loading data from a valid JSON file."""
        with open(self.file_path, "w") as f:
            json.dump({"records": [{"id": 1, "name": "Alice"}]}, f)  # Write sample JSON
        handler = JSONHandler(self.file_path)
        self.assertEqual(handler.data["records"][0]["id"], 1)

    def test_jsonhandler_load_data_invalid_json(self):
        """Tests handling invalid JSON."""
        with open(self.file_path, "w") as f:
            f.write("This is not valid JSON!")  # Write invalid JSON
        handler = JSONHandler(self.file_path) 
        self.assertEqual(handler.data, {"records": []})

    def test_jsonhandler_save_data(self):
        """Tests saving data to the JSON file."""
        handler = JSONHandler(self.file_path)
        handler.data["records"] = [{"id": 1, "name": "Bob"}]
        handler.save_data()  

        with open(self.file_path, "r") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data["records"][0]["name"], "Bob")

    # Add more tests for add_record, delete_record, update_record, list_records, export_data 


if __name__ == "__main__":
    unittest.main()