from unittest.mock import mock_open, patch

import pytest
from lec02.hw.job2.dal.read_disk import read_json


@patch("builtins.open", new_callable=mock_open, read_data='[{"key": "value"}]')
@patch("os.path.join")
def test_read_json_success(mock_path_join, mock_open_file):
    # Mock os.path.join behavior
    mock_path_join.return_value = "/mock/path/mock_file.json"

    # Call the function
    result = read_json("/mock/path", "mock_file.json")

    # Assertions
    mock_path_join.assert_called_once_with("/mock/path", "mock_file.json")
    mock_open_file.assert_called_once_with("/mock/path/mock_file.json", "r", encoding="utf-8")
    assert result == [{"key": "value"}]


@patch("builtins.open", side_effect=FileNotFoundError("File not found"))
@patch("os.path.join")
def test_read_json_file_not_found(mock_path_join, mock_open_file):
    # Mock os.path.join behavior
    mock_path_join.return_value = "/mock/path/mock_file.json"

    # Call the function and expect an exception
    with pytest.raises(FileNotFoundError, match="File not found"):
        read_json("/mock/path", "mock_file.json")

    # Assertions
    mock_path_join.assert_called_once_with("/mock/path", "mock_file.json")
    mock_open_file.assert_called_once_with("/mock/path/mock_file.json", "r", encoding="utf-8")
