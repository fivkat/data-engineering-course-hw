from unittest.mock import mock_open, patch

import pytest
from lec02.hw.job2.dal.write_disk import write_to_avro


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.join")
@patch("fastavro.writer")
def test_write_to_avro_success(mock_fastavro_writer, mock_path_join, mock_open_file):
    # Mock os.path.join behavior
    mock_path_join.return_value = "/mock/path/mock_file.avro"

    # Mock schema and data
    mock_schema = {
        "type": "record",
        "name": "TestRecord",
        "fields": [{"name": "field1", "type": "string"}],
    }
    mock_data = [{"field1": "value1"}]

    # Call the function
    write_to_avro(mock_data, "/mock/path", "mock_file.avro", mock_schema)

    # Assertions
    mock_path_join.assert_called_once_with("/mock/path", "mock_file.avro")
    mock_open_file.assert_called_once_with("/mock/path/mock_file.avro", mode="wb")
    mock_fastavro_writer.assert_called_once_with(mock_open_file(), mock_schema, mock_data)


@patch("builtins.open", side_effect=OSError("File write error"))
@patch("os.path.join")
def test_write_to_avro_file_write_error(mock_path_join, mock_open_file):
    # Mock os.path.join behavior
    mock_path_join.return_value = "/mock/path/mock_file.avro"

    # Mock schema and data
    mock_schema = {
        "type": "record",
        "name": "TestRecord",
        "fields": [{"name": "field1", "type": "string"}],
    }
    mock_data = [{"field1": "value1"}]

    # Call the function and expect an exception
    with pytest.raises(OSError, match="File write error"):
        write_to_avro(mock_data, "/mock/path", "mock_file.avro", mock_schema)

    # Assertions
    mock_path_join.assert_called_once_with("/mock/path", "mock_file.avro")
    mock_open_file.assert_called_once_with("/mock/path/mock_file.avro", mode="wb")
