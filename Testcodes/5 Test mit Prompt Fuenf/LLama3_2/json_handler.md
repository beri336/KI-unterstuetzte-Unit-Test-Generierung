# Unit Test Documentation
## Original File: ../JSON-Handler/json_handler.py

### Model: LLama3.2:3b

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "main.py"

import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree


path = "./JSON-Handler/" # path to save all files

class JSONHandler:
    def __init__(self, file_path):
        """
        Initialize the JSON handler with a file path.
        :param file_path: Path to the JSON file.
        """
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        """
        Load data from the JSON file.
        :return: Data as a Python dictionary.
        """
        if not os.path.exists(self.file_path):
            print(f"{self.file_path} not found. Creating a new file.")
            return {"records": []} # Default structure

        with open(self.file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Invalid JSON format. Starting with an empty dataset.")
                return {"records": []}

    def save_data(self):
        """
        Save the current data back to the JSON file.
        """
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)
        print("Data saved successfully.")

    def add_record(self, record):
        """
        Add a new record to the dataset.
        :param record: A dictionary representing the new record.
        """
        self.data["records"].append(record)
        print(f"Record added: {record}")

    def delete_record(self, record_id):
        """
        Delete a record by ID.
        :param record_id: The ID of the record to delete.
        """
        initial_count = len(self.data["records"])
        self.data["records"] = [rec for rec in self.data["records"] if rec.get("id") != record_id]
        if len(self.data["records"]) < initial_count:
            print(f"Record with ID {record_id} deleted.")
        else:
            print(f"No record found with ID {record_id}.")

    def update_record(self, record_id, updates):
        """
        Update a record by ID.
        :param record_id: The ID of the record to update.
        :param updates: A dictionary of updates.
        """
        for rec in self.data["records"]:
            if rec.get("id") == record_id:
                rec.update(updates)
                print(f"Record with ID {record_id} updated.")
                return
        print(f"No record found with ID {record_id}.")

    def list_records(self):
        """
        List all records in the dataset.
        """
        if not self.data["records"]:
            print("No records found.")
        for record in self.data["records"]:
            print(record)

    def export_data(self, export_path, format="txt"):
        """
        Export the current dataset to another file in TXT or XML format.
        :param export_path: Path to the export file.
        :param format: The format for the export file ("txt" or "xml").
        """
        if format == "txt":
            self._export_to_txt(export_path)
        elif format == "xml":
            self._export_to_xml(export_path)
        else:
            print(f"Unsupported format: {format}")

    def _export_to_txt(self, export_path):
        """
        Export the dataset to a TXT file.
        :param export_path: Path to the TXT file.
        """
        with open(export_path, "w") as file:
            for record in self.data["records"]:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")
        print(f"Data exported to TXT file at {export_path}.")

    def _export_to_xml(self, export_path):
        """
        Export the dataset to an XML file.
        :param export_path: Path to the XML file.
        """
        root = Element("Records")
        for record in self.data["records"]:
            record_element = SubElement(root, "Record")
            for key, value in record.items():
                child = SubElement(record_element, key)
                child.text = str(value)
        
        tree = ElementTree(root)
        with open(export_path, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)
        print(f"Data exported to XML file at {export_path}.")
```

<hr>

### Generated Output

```
Below are the unit tests for your `JSONHandler` class using the `unittest` framework.

```python
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
```
To run the unit tests for your `JSONHandler` class, create a new Python file (e.g., `test_json_handler.py`) and copy the above code into it. Make sure to import the `JSONHandler` class from your main script.

Then, run the test by executing the following command in your terminal:

```bash
python test_json_handler.py
```

If all tests pass without raising any assertions errors, you can be confident that your `JSONHandler` class works as expected.
```