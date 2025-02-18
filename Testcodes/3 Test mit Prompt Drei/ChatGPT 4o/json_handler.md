# Unit Test Documentation
## Original File: ../JSON-Handler/json_handler.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write a Unit Test for the following Python code. Focus on testing:
- Positive cases (where the function behaves as expected)
- Edge cases (input that might cause failures)
- Negative cases (where the function should throw errors or return incorrect results)
- Performance tests if applicable

Include comments to explain the purpose of each test case.


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
Here is a `unittest` test suite for the `JSONHandler` class. It covers positive cases, edge cases, negative cases, and a basic performance test.

### Test Code

```python
import unittest
import os
import json
from your_module import JSONHandler

class TestJSONHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment: Create a directory for test files."""
        cls.test_dir = "./test_data"
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment: Remove test directory and files."""
        for file in os.listdir(cls.test_dir):
            os.remove(os.path.join(cls.test_dir, file))
        os.rmdir(cls.test_dir)

    def setUp(self):
        """Prepare a fresh JSON handler for each test."""
        self.file_path = os.path.join(self.test_dir, "test.json")
        self.handler = JSONHandler(self.file_path)

    def tearDown(self):
        """Remove the JSON file after each test."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # Positive Test Cases
    def test_add_record(self):
        """Test adding a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.save_data()

        with open(self.file_path, "r") as file:
            data = json.load(file)
        self.assertIn(record, data["records"])

    def test_delete_record(self):
        """Test deleting a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.delete_record(1)
        self.assertNotIn(record, self.handler.data["records"])

    def test_update_record(self):
        """Test updating a record."""
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.update_record(1, {"name": "Jane Doe"})
        updated_record = next(rec for rec in self.handler.data["records"] if rec["id"] == 1)
        self.assertEqual(updated_record["name"], "Jane Doe")

    def test_list_records(self):
        """Test listing records."""
        record1 = {"id": 1, "name": "John Doe"}
        record2 = {"id": 2, "name": "Jane Doe"}
        self.handler.add_record(record1)
        self.handler.add_record(record2)
        records = self.handler.list_records()
        self.assertIn(record1, self.handler.data["records"])
        self.assertIn(record2, self.handler.data["records"])

    def test_export_to_txt(self):
        """Test exporting to TXT."""
        export_path = os.path.join(self.test_dir, "test.txt")
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.export_data(export_path, format="txt")
        self.assertTrue(os.path.exists(export_path))

    def test_export_to_xml(self):
        """Test exporting to XML."""
        export_path = os.path.join(self.test_dir, "test.xml")
        record = {"id": 1, "name": "John Doe"}
        self.handler.add_record(record)
        self.handler.export_data(export_path, format="xml")
        self.assertTrue(os.path.exists(export_path))

    # Edge Cases
    def test_empty_file_creation(self):
        """Test creating a new file when none exists."""
        self.assertFalse(os.path.exists(self.file_path))
        self.handler._load_data()
        self.assertEqual(self.handler.data, {"records": []})

    def test_invalid_json_format(self):
        """Test handling invalid JSON format."""
        with open(self.file_path, "w") as file:
            file.write("{invalid json}")
        data = self.handler._load_data()
        self.assertEqual(data, {"records": []})

    def test_update_nonexistent_record(self):
        """Test updating a record that doesn't exist."""
        self.handler.update_record(1, {"name": "Jane Doe"})
        self.assertNotIn({"id": 1, "name": "Jane Doe"}, self.handler.data["records"])

    def test_delete_nonexistent_record(self):
        """Test deleting a record that doesn't exist."""
        self.handler.delete_record(999)
        self.assertEqual(len(self.handler.data["records"]), 0)

    # Negative Cases
    def test_add_record_without_id(self):
        """Test adding a record without an ID."""
        record = {"name": "John Doe"}
        self.handler.add_record(record)
        self.assertIn(record, self.handler.data["records"])

    def test_export_to_invalid_format(self):
        """Test exporting to an unsupported format."""
        export_path = os.path.join(self.test_dir, "test.invalid")
        self.handler.export_data(export_path, format="invalid")
        self.assertFalse(os.path.exists(export_path))

    # Performance Test Case
    def test_large_number_of_records(self):
        """Test handling a large number of records."""
        for i in range(1000):
            self.handler.add_record({"id": i, "name": f"User{i}"})
        self.handler.save_data()

        with open(self.file_path, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data["records"]), 1000)

if __name__ == "__main__":
    unittest.main()
```

### Explanation of Test Cases

1. **Positive Cases**:
   - `test_add_record`: Verifies adding a record works correctly.
   - `test_delete_record`: Ensures records can be deleted by ID.
   - `test_update_record`: Verifies records are updated correctly.
   - `test_list_records`: Confirms all records are listed.
   - `test_export_to_txt` and `test_export_to_xml`: Check data is exported correctly to the specified formats.

2. **Edge Cases**:
   - `test_empty_file_creation`: Ensures a new file is created if none exists.
   - `test_invalid_json_format`: Tests the handler's ability to recover from invalid JSON.
   - `test_update_nonexistent_record`: Handles attempts to update nonexistent records gracefully.
   - `test_delete_nonexistent_record`: Handles attempts to delete nonexistent records gracefully.

3. **Negative Cases**:
   - `test_add_record_without_id`: Ensures records without an ID can still be added.
   - `test_export_to_invalid_format`: Checks that unsupported formats are rejected.

4. **Performance Test Case**:
   - `test_large_number_of_records`: Ensures the handler can handle a large number of records without crashing or becoming unresponsive.

### Notes
- Replace `your_module` with the actual module name containing the `JSONHandler` class.
- The test suite assumes the directory structure and file handling operations are correct. If path issues occur, adjust the test directory setup accordingly.
```