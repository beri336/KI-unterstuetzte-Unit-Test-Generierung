import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from unittest.mock import patch, MagicMock
from unittest import TestCase

class TestJSONHandler(TestCase):

    def setUp(self):
        self.path = "./Test-JSON-Handler/"  # path to save all files
        self.json_handler = JSONHandler(self.path)

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('json.load')
    def test_init_loads_data_from_json_file(self, mock_json_load, mock_path_exists, mock_makedirs):
        # Test that the data is loaded correctly from the JSON file
        mock_path_exists.return_value = False
        self.json_handler._load_data()
        mock_json_load.assert_called_once_with(open(self.path, 'r').close)

    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_init_creates_new_file_and_loads_default_data(self, mock_path_exists, mock_makedirs):
        # Test that a new file is created and default data loaded
        mock_path_exists.return_value = True
        self.json_handler._load_data()
        mock_json_load.assert_called_once_with(open(self.path, 'r').close)
        # Verify the initial data structure

    def test_save_data(self):
        # Test saving data back to the JSON file
        with open(self.path, "w") as file:
            json.dump({"records": []}, file, indent=4)
        self.json_handler.save_data()
        with open(self.path, 'r') as file:
            loaded_data = json.load(file)
            self.assertEqual(loaded_data, {"records": []})

    def test_add_record(self):
        # Test adding a new record to the dataset
        initial_count = len(self.json_handler.data["records"])
        self.json_handler.add_record({"id": 1, "name": "John Doe"})
        self.assertEqual(len(self.json_handler.data["records"]), initial_count + 1)

    def test_delete_record(self):
        # Test deleting a record by ID
        records_before = self.json_handler.data["records"]
        self.json_handler.delete_record(1)
        self.assertEqual(len(self.json_handler.data["records"]), len(records_before) - 1)

    def test_update_record(self):
        # Test updating a record by ID
        initial_data = self.json_handler.data["records"][0].copy()
        self.json_handler.update_record(1, {"name": "Jane Doe"})
        for rec in self.json_handler.data["records"]:
            if rec.get("id") == 1:
                self.assertEqual(rec, {"id": 1, "name": "Jane Doe"})

    def test_list_records(self):
        # Test listing all records in the dataset
        record = MagicMock()
        record.id = 1
        record.name = "John Doe"
        self.json_handler.data["records"].append(record)
        self.json_handler.list_records()
        for rec in self.json_handler.data["records"]:
            self.assertEqual(rec, record)

    def test_export_to_txt(self):
        # Test exporting the dataset to a TXT file
        export_path = "export.txt"
        with open(export_path, 'w') as file:
            for record in self.json_handler.data["records"]:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")
        self.json_handler.export_data(export_path)
        with open(export_path, "r") as txt_file, open(self.path + 'export.txt', 'w') as file:
            for line in txt_file.readlines():
                if line not in file.read():  # Check that all lines are present in the file
                    self.fail(f"Missing line: {line}")

    @patch('os.makedirs')
    def test_export_to_xml(self, mock_makedirs):
        # Test exporting the dataset to an XML file
        export_path = "export.xml"
        root_element = MagicMock()
        for record in self.json_handler.data["records"]:
            record_element = MagicMock()
            sub_elements = [MagicMock() for _ in range(len(record))]
            for key, value in record.items():
                child_element = MagicMock()
                child_element.text = str(value)
                sub_elements[key] = child_element
            root_element.append(sub_elements[0])
        mock_makedirs.return_value = True
        self.json_handler._export_to_xml(export_path)
        with open(export_path, 'wb') as xml_file:
            tree = ElementTree(root_element)
            tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    @patch('xml.etree.ElementTree.tostring')
    def test_export_to_xml_to_bytes(self, mock_tostring):
        # Test that the XML export returns bytes
        with open(self.path + 'export.xml', 'wb') as xml_file:
            self.json_handler.export_data(self.path + 'export.xml', format='xml')
            result = mock_tostring.return_value.encode('utf-8')
        self.assertEqual(result, b'<root><record id="1"><name>John Doe</name></record></root>')


if __name__ == '__main__':
    unittest.main()