# Unit Test Documentation
## Original File: ../JSON-Handler/json_handler.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
"Write unit tests for the following Python code using the `unittest` framework. Write test cases in the following order:
- First, test normal input cases with common values.
- Then, test edge cases (e.g., empty lists, negative numbers, etc.).
- Finally, test invalid input cases that should raise exceptions.
- Write code-comments for each test case to explain its purpose.
- filename is "json_handler.py"


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
Here is the `unittest` test suite for the provided `JSONHandler` class. The test cases follow the prescribed structure: normal cases, edge cases, and invalid input cases.

### Test Suite

```python
import unittest
import os
import json
from json_handler import JSONHandler


class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        """Set up a temporary JSON file for testing."""
        self.file_path = "./test_data.json"
        self.json_handler = JSONHandler(self.file_path)
        self.json_handler.data = {"records": []}  # Start with empty data
        self.json_handler.save_data()

    def tearDown(self):
        """Clean up by removing the temporary JSON file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # Normal Input Cases
    def test_add_record(self):
        """Test adding a normal record."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.assertIn(record, self.json_handler.data["records"])

    def test_delete_record(self):
        """Test deleting a record by ID."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.delete_record(1)
        self.assertNotIn(record, self.json_handler.data["records"])

    def test_update_record(self):
        """Test updating a record by ID."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        updates = {"email": "alice_new@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.update_record(1, updates)
        updated_record = next(rec for rec in self.json_handler.data["records"] if rec["id"] == 1)
        self.assertEqual(updated_record["email"], "alice_new@example.com")

    def test_list_records(self):
        """Test listing all records."""
        records = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
        for record in records:
            self.json_handler.add_record(record)
        listed_records = self.json_handler.data["records"]
        self.assertEqual(listed_records, records)

    def test_export_to_txt(self):
        """Test exporting records to a TXT file."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        export_path = "./test_data.txt"
        self.json_handler.export_data(export_path, format="txt")
        self.assertTrue(os.path.exists(export_path))
        os.remove(export_path)

    def test_export_to_xml(self):
        """Test exporting records to an XML file."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        export_path = "./test_data.xml"
        self.json_handler.export_data(export_path, format="xml")
        self.assertTrue(os.path.exists(export_path))
        os.remove(export_path)

    # Edge Cases
    def test_add_empty_record(self):
        """Test adding an empty record."""
        record = {}
        self.json_handler.add_record(record)
        self.assertIn(record, self.json_handler.data["records"])

    def test_delete_nonexistent_record(self):
        """Test deleting a record that does not exist."""
        initial_count = len(self.json_handler.data["records"])
        self.json_handler.delete_record(999)  # Nonexistent ID
        self.assertEqual(len(self.json_handler.data["records"]), initial_count)

    def test_update_nonexistent_record(self):
        """Test updating a record that does not exist."""
        updates = {"email": "new_email@example.com"}
        self.json_handler.update_record(999, updates)  # Nonexistent ID
        self.assertNotIn(updates, self.json_handler.data["records"])

    def test_list_records_empty(self):
        """Test listing records when no records exist."""
        listed_records = self.json_handler.data["records"]
        self.assertEqual(listed_records, [])

    # Invalid Input Cases
    def test_invalid_file_path(self):
        """Test initializing with an invalid file path."""
        invalid_path = "/invalid_path/test.json"
        handler = JSONHandler(invalid_path)
        self.assertEqual(handler.data, {"records": []})

    def test_export_invalid_format(self):
        """Test exporting data in an unsupported format."""
        record = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        self.json_handler.add_record(record)
        self.json_handler.export_data("./test_data.unsupported", format="unsupported")
        self.assertFalse(os.path.exists("./test_data.unsupported"))

    def test_non_dict_record(self):
        """Test adding a record that is not a dictionary."""
        with self.assertRaises(AttributeError):  # .get() is called on record
            self.json_handler.add_record(["not", "a", "dict"])

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases

1. **Setup and Teardown**:
   - Temporary JSON file `test_data.json` is created for testing and deleted after each test to ensure isolation.

2. **Normal Input Cases**:
   - Test standard operations like adding, deleting, updating, listing, and exporting records.

3. **Edge Cases**:
   - Test operations with unusual inputs, like empty records, nonexistent IDs, and listing records when none exist.

4. **Invalid Input Cases**:
   - Test behavior when provided with invalid paths, unsupported export formats, or non-dictionary records.

This test suite ensures the robustness of the `JSONHandler` class in handling various scenarios.
```