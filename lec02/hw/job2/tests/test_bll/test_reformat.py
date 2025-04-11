from unittest.mock import patch

import pytest
from lec02.hw.job2.bll.reformat import convert_to_avro


@patch("lec02.hw.job2.bll.reformat.directory_process")
@patch("lec02.hw.job2.bll.reformat.read_disk")
@patch("lec02.hw.job2.bll.reformat.write_disk")
@patch("os.listdir")
def test_convert_to_avro_success(mock_listdir, mock_write_disk, mock_read_disk, mock_directory_process):
    # Mock directory operations
    mock_directory_process.check_dir_path.side_effect = [True, True]
    mock_directory_process.check_dir_content.return_value = True
    mock_directory_process.empty_directory.return_value = None

    # Mock file operations
    mock_listdir.return_value = ["file1.json", "file2.json"]
    mock_read_disk.read_json.side_effect = [{"client": "John"}, {"client": "Doe"}]
    mock_write_disk.write_to_avro.return_value = None

    # Call the function
    convert_to_avro("/mock/raw_dir", "/mock/stg_dir")

    # Assertions
    mock_directory_process.check_dir_path.assert_any_call("/mock/raw_dir", raise_error=True)
    mock_directory_process.check_dir_content.assert_called_once_with("/mock/raw_dir", raise_error=True)
    mock_directory_process.check_dir_path.assert_any_call("/mock/stg_dir")
    mock_directory_process.empty_directory.assert_called_once_with("/mock/stg_dir")
    mock_listdir.assert_called_once_with("/mock/raw_dir")
    mock_read_disk.read_json.assert_any_call("/mock/raw_dir", "file1.json")
    mock_read_disk.read_json.assert_any_call("/mock/raw_dir", "file2.json")
    mock_write_disk.write_to_avro.assert_any_call({"client": "John"}, "/mock/stg_dir", "file1.avro", {
        "type": "record",
        "name": "PurchaseRecord",
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "int"}
        ]
    })
    mock_write_disk.write_to_avro.assert_any_call({"client": "Doe"}, "/mock/stg_dir", "file2.avro", {
        "type": "record",
        "name": "PurchaseRecord",
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "int"}
        ]
    })


@patch("lec02.hw.job2.bll.reformat.directory_process")
def test_convert_to_avro_raw_dir_not_found(mock_directory_process):
    # Mock directory operations
    mock_directory_process.check_dir_path.side_effect = FileNotFoundError("Raw directory not found")

    # Call the function and expect an exception
    with pytest.raises(FileNotFoundError, match="Raw directory not found"):
        convert_to_avro("/mock/raw_dir", "/mock/stg_dir")

    # Assertions
    mock_directory_process.check_dir_path.assert_called_once_with("/mock/raw_dir", raise_error=True)
