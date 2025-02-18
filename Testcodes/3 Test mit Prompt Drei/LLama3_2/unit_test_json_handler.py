import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from unittest.mock import patch, MagicMock
from your_module import JSONHandler  # Replace 'your_module' with the actual module name

class TestJSONHandler:
    def setUp(self):
        self.path = "./JSON-Handler/test.json"
        self.handler = JSONHandler(self.path)

    def test_positive_add_record(self):
        """
        Test adding a new record to the dataset.
        """
        data = {"id": 1, "name": "John"}
        self.handler.add_record(data)
        self.assertEqual(len(self.handler.data["records"]), 1)
        self.assertEqual(self.handler.data["records"][0], data)

    def test_positive_update_record(self):
        """
        Test updating a record in the dataset.
        """
        initial_data = {"id": 1, "name": "John"}
        updated_data = {"id": 1, "name": "Jane"}
        self.handler.add_record(initial_data)
        self.handler.update_record(1, {"name": "Jane"})
        self.assertEqual(self.handler.data["records"][0], updated_data)

    def test_positive_delete_record(self):
        """
        Test deleting a record from the dataset.
        """
        initial_data = {"id": 1, "name": "John"}
        self.handler.add_record(initial_data)
        self.handler.delete_record(1)
        self.assertEqual(len(self.handler.data["records"]), 0)

    def test_negative_add_invalid_record(self):
        """
        Test adding an invalid record to the dataset.
        """
        with patch("json.JSONDecodeError", side_effect=Exception) as mock_error:
            try:
                data = {"id": 1, "name": "John"}
                self.handler.add_record(data)
            except Exception as e:
                mock_error.assert_called_once()
                assert e

    def test_negative_delete_non_existent_record(self):
        """
        Test deleting a non-existent record from the dataset.
        """
        initial_data = {"id": 1, "name": "John"}
        self.handler.add_record(initial_data)
        with patch("json.JSONDecodeError", side_effect=Exception) as mock_error:
            try:
                self.handler.delete_record(2)
            except Exception as e:
                mock_error.assert_called_once()
                assert e

    def test_positive_export_to_txt(self):
        """
        Test exporting the dataset to a TXT file.
        """
        initial_data = {"id": 1, "name": "John"}
        self.handler.add_record(initial_data)
        export_path = "./JSON-Handler/export.txt"
        self.handler.export_data(export_path)
        with open(export_path, "r") as file:
            contents = file.read()
            assert contents == f"{'id': '1', 'name': 'John'}\n\n"

    def test_positive_export_to_xml(self):
        """
        Test exporting the dataset to an XML file.
        """
        initial_data = {"id": 1, "name": "John"}
        self.handler.add_record(initial_data)
        export_path = "./JSON-Handler/export.xml"
        self.handler.export_data(export_path, format="xml")
        with open(export_path, "rb") as file:
            contents = tostring(ElementTree.fromstring(file.read()))
            assert contents == b<?xml version='1.0' encoding='utf-8'?><Records><Record id='1'/><Record name='John'/></Records>

    def test_negative_export_to_invalid_format(self):
        """
        Test exporting the dataset to an invalid format.
        """
        initial_data = {"id": 1, "name": "John"}
        self.handler.add_record(initial_data)
        export_path = "./JSON-Handler/export.txt"
        with patch("json.dump", side_effect=Exception) as mock_error:
            try:
                self.handler.export_data(export_path, format="pdf")
            except Exception as e:
                mock_error.assert_called_once()
                assert e

if __name__ == "__main__":
    unittest.main()