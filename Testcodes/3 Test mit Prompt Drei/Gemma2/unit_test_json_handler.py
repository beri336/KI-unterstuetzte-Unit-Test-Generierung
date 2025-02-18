import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
import unittest

# Path for test data files (adjust as needed)
test_data_path = "./JSON-Handler/test_data/"  


class JSONHandlerTest(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.handler = JSONHandler(file_path=test_data_path + "test.json")

    def tearDown(self):
        """Clean up after each test case."""
        try:
            os.remove(test_data_path + "test.json")
        except FileNotFoundError:
            pass

    # --- Positive Cases ---

    def test_add_record(self):
        new_record = {"id": 5, "name": "Test Record", "value": 10}
        self.handler.add_record(new_record)
        loaded_data = self.handler._load_data()  # Reload data to check changes
        self.assertIn(new_record, loaded_data["records"])

    def test_delete_record(self):
        existing_records = self.handler.data["records"]  
        if existing_records:
            record_id_to_delete = existing_records[0].get("id") 
            self.handler.delete_record(record_id_to_delete)
            loaded_data = self.handler._load_data()  # Reload data to check changes
            self.assertNotIn({**existing_records[0]}, loaded_data["records"])

    def test_update_record(self):
        record_id_to_update = 1 # Replace with an existing record ID if testing 
        updates = {"value": 25}
        self.handler.update_record(record_id_to_update, updates)
        loaded_data = self.handler._load_data()  # Reload data to check changes
        updated_record = next((rec for rec in loaded_data["records"] if rec.get("id") == record_id_to_update), None)
        self.assertEqual(updated_record.get("value"), updates["value"])

    def test_list_records(self):
        self.handler.list_records()  # Test listing records 

    def test_export_data_txt(self):
        self.handler.export_data(test_data_path + "exported_data.txt", format="txt")
        with open(test_data_path + "exported_data.txt", "r") as file:
            content = file.read()
        # Check if data is exported correctly (example)
        self.assertIn("id: 1", content)  

    def test_export_data_xml(self):
        self.handler.export_data(test_data_path + "exported_data.xml", format="xml")
        tree = ElementTree.parse(test_data_path + "exported_data.xml")
        root = tree.getroot()
        # Check if XML structure is as expected (example)
        self.assertEqual(root.tag, "Records")

    # --- Edge Cases ---

    def test_empty_file(self):
        handler = JSONHandler(file_path=test_data_path + "empty_file.json")
        loaded_data = handler._load_data() 
        self.assertEqual(loaded_data, {"records": []})  # Check if empty data is handled

    def test_nonexistent_file(self):
        handler = JSONHandler(file_path=test_data_path + "nonexistent_file.json")
        loaded_data = handler._load_data()
        self.assertEqual(loaded_data, {"records": []})  # Check if non-existence is handled

    # --- Negative Cases --- (Error handling)
    def test_invalid_json(self):
        with open(test_data_path + "test_invalid_json.json", "w") as f:
            f.write("{'id': 1, 'name': 'Test'}")  # Intentionally write invalid JSON

        try:
            handler = JSONHandler(file_path=test_data_path + "test_invalid_json.json")
            handler._load_data()
            self.fail("Expected an exception due to invalid JSON") 
        except json.JSONDecodeError as e:
            # Test passed if a JSONDecodeError is raised
            self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()