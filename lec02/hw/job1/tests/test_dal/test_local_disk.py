from unittest.mock import mock_open, patch

from lec02.hw.job1.dal.local_disk import save_json_to_disk


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_save_json_to_disk(mock_json_dump, mock_open_file, mock_path_join):
    # Mock the os.path.join behavior
    mock_path_join.return_value = "/mock/path/mock_file.json"

    # Call the function
    save_json_to_disk([{"key": "value"}], "/mock/path", "mock_file.json")

    # Assertions
    mock_path_join.assert_called_once_with("/mock/path", "mock_file.json")
    mock_open_file.assert_called_once_with("/mock/path/mock_file.json", "w")
    mock_json_dump.assert_called_once_with([{"key": "value"}], mock_open_file(), indent=4)
