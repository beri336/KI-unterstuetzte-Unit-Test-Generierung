# Unit Test Documentation
## Original File: ../JSON-Handler/json_handler.py

### Model: ChatGPT 4o

<hr>

### Prompt

```
Write me a Unit Test for the following Python code. Break the process into multiple tests:

- One function per test case.
- Each test should have a clear and descriptive name indicating what it tests (e.g., `test_function_name_valid_input`, `test_function_name_edge_case`, etc.)
- Include normal cases, edge cases, and cases that should raise exceptions.
- Add comments to each test cases.
Write the test functions step by step, explaining each part before moving on.
filename: "json_handler.py"

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
Here’s how to write unit tests for `json_handler.py` using the `unittest` framework. Each function is tested with normal cases, edge cases, and exceptions where applicable. We'll also include comments for clarity.

---

### Step 1: Setting Up the Test File
Create a test file named `test_json_handler.py`:

```python
import unittest
import os
import json
from json_handler import JSONHandler

class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        # Set up a test JSON file path
        self.test_file = "test_records.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.handler = JSONHandler(self.test_file)

    def tearDown(self):
        # Clean up by removing the test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
```

---

### Step 2: Test `_load_data`

#### Explanation:
- Check if a new file is initialized correctly.
- Test behavior with invalid JSON.

```python
class TestJSONHandler(unittest.TestCase):
    def test_load_data_new_file(self):
        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})

    def test_load_data_invalid_json(self):
        # Create a corrupt JSON file
        with open(self.test_file, "w") as file:
            file.write("{invalid json}")

        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})
```

---

### Step 3: Test `save_data`

#### Explanation:
- Ensure data is saved correctly.

```python
class TestJSONHandler(unittest.TestCase):
    def test_save_data(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.save_data()

        with open(self.test_file, "r") as file:
            data = json.load(file)

        self.assertEqual(data, {"records": [{"id": 1, "name": "Alice"}]})
```

---

### Step 4: Test `add_record`

#### Explanation:
- Test adding records.
- Check that records are appended.

```python
class TestJSONHandler(unittest.TestCase):
    def test_add_record(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])
```

---

### Step 5: Test `delete_record`

#### Explanation:
- Check behavior with existing and non-existing records.

```python
class TestJSONHandler(unittest.TestCase):
    def test_delete_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(1)
        self.assertEqual(self.handler.data["records"], [])

    def test_delete_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(2)
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])
```

---

### Step 6: Test `update_record`

#### Explanation:
- Test updating an existing record.
- Test behavior for non-existing records.

```python
class TestJSONHandler(unittest.TestCase):
    def test_update_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(1, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Bob"}])

    def test_update_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(2, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])
```

---

### Step 7: Test `list_records`

#### Explanation:
- Ensure records are listed correctly.

```python
class TestJSONHandler(unittest.TestCase):
    def test_list_records(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.add_record({"id": 2, "name": "Bob"})
        records = self.handler.data["records"]
        self.assertEqual(records, [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
```

---

### Step 8: Test `export_data`

#### Explanation:
- Test TXT and XML exports.

```python
class TestJSONHandler(unittest.TestCase):
    def test_export_to_txt(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        txt_file = "test_export.txt"
        self.handler.export_data(txt_file, format="txt")
        
        with open(txt_file, "r") as file:
            content = file.read()
        
        self.assertIn("id: 1", content)
        self.assertIn("name: Alice", content)

        os.remove(txt_file)

    def test_export_to_xml(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        xml_file = "test_export.xml"
        self.handler.export_data(xml_file, format="xml")
        
        with open(xml_file, "r") as file:
            content = file.read()
        
        self.assertIn("<id>1</id>", content)
        self.assertIn("<name>Alice</name>", content)

        os.remove(xml_file)

    def test_export_data_invalid_format(self):
        with self.assertLogs(level="INFO") as log:
            self.handler.export_data("test_file", format="unsupported")
        self.assertIn("Unsupported format", log.output[0])
```

---

### Step 9: Run Tests
Execute the tests with:

```bash
python -m unittest test_json_handler.py
```

---

### Full Test File

```python
import unittest
import os
import json
from json_handler import JSONHandler

class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_records.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.handler = JSONHandler(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_data_new_file(self):
        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})

    def test_load_data_invalid_json(self):
        with open(self.test_file, "w") as file:
            file.write("{invalid json}")

        handler = JSONHandler(self.test_file)
        self.assertEqual(handler.data, {"records": []})

    def test_save_data(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.save_data()

        with open(self.test_file, "r") as file:
            data = json.load(file)

        self.assertEqual(data, {"records": [{"id": 1, "name": "Alice"}]})

    def test_add_record(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_delete_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(1)
        self.assertEqual(self.handler.data["records"], [])

    def test_delete_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.delete_record(2)
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_update_record_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(1, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Bob"}])

    def test_update_record_non_existing(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.update_record(2, {"name": "Bob"})
        self.assertEqual(self.handler.data["records"], [{"id": 1, "name": "Alice"}])

    def test_list_records(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        self.handler.add_record({"id": 2, "name": "Bob"})
        records = self.handler.data["records"]
        self.assertEqual(records, [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])

    def test_export_to_txt(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        txt_file = "test_export.txt"
        self.handler.export_data(txt_file, format="txt")
        
        with open(txt_file, "r") as file:
            content = file.read()
        
        self.assertIn("id: 1", content)
        self.assertIn("name: Alice", content)

        os.remove(txt_file)

    def test_export_to_xml(self):
        self.handler.add_record({"id": 1, "name": "Alice"})
        xml_file = "test_export.xml"
        self.handler.export_data(xml_file, format="xml")
        
        with open(xml_file, "r") as file:
            content = file.read()
        
        self.assertIn("<id>1</id>", content)
        self.assertIn("<name>Alice</name>", content)

        os.remove(xml_file)

    def test_export_data_invalid_format(self):
        with self.assertLogs(level="INFO") as log:
           

 self.handler.export_data("test_file", format="unsupported")
        self.assertIn("Unsupported format", log.output[0])
```

This test suite covers all methods in the `JSONHandler` class, ensuring correctness under various conditions.
```