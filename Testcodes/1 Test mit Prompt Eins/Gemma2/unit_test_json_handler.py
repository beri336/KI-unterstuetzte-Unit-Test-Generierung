import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import unittest

# Your existing JSONHandler class 
# ... (Paste your code here)

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.handler = JSONHandler("./test_file.json")  # Using a test file
        os.makedirs(os.path.dirname("./test_file.json"), exist_ok=True) 

    def tearDown(self):
        os.remove("./test_file.json")  # Clean up the test file

    def test_load_data(self):
        # Test loading an existing file
        with open("./test_file.json", "w") as f:
            json.dump({"records": [{"id": 1, "name": "Alice"}]}, f)
        
        loaded_data = self.handler._load_data()
        self.assertEqual(loaded_data["records"][0]["id"], 1)

    def test_load_data_new_file(self):
        # Test loading a new file (should create with default data)
        self.handler._load_data()  
        with open("./test_file.json", "r") as f:
            loaded_data = json.load(f)
        self.assertEqual(len(loaded_data["records"]), 0)

    def test_add_record(self):
        self.handler.add_record({"id": 2, "name": "Bob"})
        loaded_data = self.handler._load_data()  
        self.assertEqual(len(loaded_data["records"]), 1)
        self.assertEqual(loaded_data["records"][0]["name"], "Bob")

    def test_delete_record(self):
        # Add a record first
        self.handler.add_record({"id": 3, "name": "Charlie"})

        # Delete it
        self.handler.delete_record(3)
        loaded_data = self.handler._load_data()
        self.assertEqual(len(loaded_data["records"]), 0)  

    def test_update_record(self):
        self.handler.add_record({"id": 4, "name": "David"})
        self.handler.update_record(4, {"name": "Dave"})

        loaded_data = self.handler._load_data()  
        self.assertEqual(loaded_data["records"][0]["name"], "Dave")

    def test_list_records(self):
        # Add a few records
        self.handler.add_record({"id": 5, "name": "Emma"})
        self.handler.add_record({"id": 6, "name": "Frank"})

        # List them
        self.handler.list_records()  # Output should show both records


    def test_export_data(self):
        self.handler.add_record({"id": 7, "name": "Grace"})
        self.handler.export_data("./test_export.txt")  

if __name__ == "__main__":
    unittest.main()