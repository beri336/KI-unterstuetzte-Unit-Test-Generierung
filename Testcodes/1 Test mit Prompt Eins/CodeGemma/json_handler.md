# Unit Test Documentation
## Original File: ../JSON-Handler/json_handler.py

### Model: codegemma:7b

<hr>

### Prompt

```
Write me a Unit Test for the following given Python Code:

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
```python
import unittest
from json_handler import JSONHandler

class JSONHandlerTest(unittest.TestCase):

    def setUp(self):
        self.test_file_path = "test.json"
        self.handler = JSONHandler(self.test_file_path)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_init(self):
        self.assertEqual(self.handler.file_path, self.test_file_path)
        self.assertIsInstance(self.handler.data, dict)

    def test_load_data(self):
        self.handler._load_data()
        self.assertEqual(self.handler.data, {"records": []})

    def test_save_data(self):
        self.handler.save_data()
        self.assertTrue(os.path.exists(self.test_file_path))

    def test_add_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.assertEqual(len(self.handler.data["records"]), 1)

    def test_delete_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.delete_record(1)
        self.assertEqual(len(self.handler.data["records"]), 0)

    def test_update_record(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.update_record(1, {"name": "Jane"})
        self.assertEqual(self.handler.data["records"][0]["name"], "Jane")

    def test_list_records(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.list_records()

    def test_export_data(self):
        self.handler.add_record({"id": 1, "name": "John"})
        self.handler.export_data("test.txt", "txt")
        self.assertTrue(os.path.exists("test.txt"))

if __name__ == "__main__":
    unittest.main()
```
```