import unittest
from json_handler import JSONHandler  # Import JSONHandler from main.py
import os
import json

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.path = "./Test-Data/"  # path to save all test files
        os.makedirs(self.path, exist_ok=True)  # Create the directory if it doesn't exist

    def tearDown(self):
        for file in os.listdir(self.path):
            os.remove(os.path.join(self.path, file))

    def test_normal_input_cases(self):
        """
        Test normal input cases with common values.
        """
        data_path = self.path + "normal_data.json"
        # Create a JSON file with some records
        with open(data_path, 'w') as f:
            json.dump({"records": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}, f)
        
        json_handler = JSONHandler(data_path)
        self.assertEqual(json_handler.data["records"], [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}])
        
        json_handler.add_record({"id": 3, "name": "Bob"})
        self.assertEqual(len(json_handler.data["records"]), 3)

    def test_empty_input_cases(self):
        """
        Test cases with empty input.
        """
        data_path = self.path + "empty_data.json"
        # Create a JSON file with some records
        with open(data_path, 'w') as f:
            json.dump({"records": []}, f)
        
        json_handler = JSONHandler(data_path)
        self.assertEqual(json_handler.data["records"], [])
        
        json_handler.add_record({"id": 1, "name": "John"})
        self.assertEqual(len(json_handler.data["records"]), 1)

    def test_negative_input_cases(self):
        """
        Test cases with negative input.
        """
        data_path = self.path + "negative_data.json"
        # Create a JSON file with some records
        with open(data_path, 'w') as f:
            json.dump({"records": [{"id": -1, "name": "John"}, {"id": -2, "name": "Jane"}]}, f)
        
        json_handler = JSONHandler(data_path)
        self.assertEqual(json_handler.data["records"], [{"id": -1, "name": "John"}, {"id": -2, "name": "Jane"}])
        
        # Test deletion with a negative record ID
        self.assertEqual(len(json_handler.delete_record(-3)), 0)

    def test_invalid_input_cases(self):
        """
        Test invalid input cases that should raise exceptions.
        """
        data_path = self.path + "invalid_data.json"
        
        try:
            # Create an instance of JSONHandler with a non-existent file path
            json_handler = JSONHandler(data_path)
            assert False, f"Expected ValueError when initializing JSONHandler with {data_path}"
        except FileNotFoundError as e:
            print(f"{e}")
        
        try:
            # Create an instance of JSONHandler with a non-JSON file path
            json_handler = JSONHandler(self.path + "non_json_file.txt")
            assert False, f"Expected ValueError when loading data from {self.path + 'non_json_file.txt'}"
        except json.JSONDecodeError as e:
            print(f"{e}")
        
        # Test invalid format export
        try:
            # Create an instance of JSONHandler with a non-JSON file path and XML format
            json_handler = JSONHandler(self.path, "xml")
            assert False, f"Expected ValueError when exporting data to {self.path} in XML format"
        except ValueError as e:
            print(f"{e}")

    def test_export_data(self):
        """
        Test export data to both TXT and XML format.
        """
        # Create a JSON file with some records
        data_path = self.path + "data.json"
        with open(data_path, 'w') as f:
            json.dump({"records": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}, f)
        
        # Create an instance of JSONHandler
        json_handler = JSONHandler(data_path)
        
        # Test export to TXT format
        txt_file_path = self.path + "exported_txt.txt"
        json_handler.export_data(txt_file_path, 'txt')
        with open(txt_file_path, 'r') as f:
            exported_data_txt = f.read()
        assert exported_data_txt in str(json_handler.data["records"]) * 2
        
        # Test export to XML format
        xml_file_path = self.path + "exported_xml.xml"
        json_handler.export_data(xml_file_path, 'xml')
        with open(xml_file_path, 'r') as f:
            exported_data_xml = f.read()
        assert "<record>" in exported_data_xml

if __name__ == '__main__':
    unittest.main()