from unittest.mock import MagicMock, patch

import pytest
from lec02.hw.job1.bll.sales_api import save_sales_to_local_disk
from requests.exceptions import HTTPError


@patch('lec02.hw.job1.bll.sales_api.directory_process')
@patch('lec02.hw.job1.bll.sales_api.local_disk')
@patch('lec02.hw.job1.bll.sales_api.sales_api')
def test_save_sales_to_local_disk_success(mock_sales_api, mock_local_disk, mock_directory_process):
    # Mock directory operations
    mock_directory_process.check_dir_path.return_value = True
    mock_directory_process.empty_directory.return_value = None

    # Mock API response
    mock_sales_api.get_sales.side_effect = [
        {"data": "page1"},  # First page
        {"data": "page2"},  # Second page
        HTTPError(response=MagicMock(status_code=404))  # End of pages
    ]

    # Mock saving to disk
    mock_local_disk.save_json_to_disk.return_value = None

    # Call the function
    save_sales_to_local_disk("2023-01-01", "/tmp/raw_dir")

    # Assertions
    mock_directory_process.check_dir_path.assert_called_once_with("/tmp/raw_dir")
    mock_directory_process.empty_directory.assert_called_once_with("/tmp/raw_dir")
    assert mock_sales_api.get_sales.call_count == 3
    mock_local_disk.save_json_to_disk.assert_any_call({"data": "page1"}, "/tmp/raw_dir", "sales_2023-01-01_1.json")
    mock_local_disk.save_json_to_disk.assert_any_call({"data": "page2"}, "/tmp/raw_dir", "sales_2023-01-01_2.json")


@patch('lec02.hw.job1.bll.sales_api.directory_process')
@patch('lec02.hw.job1.bll.sales_api.local_disk')
@patch('lec02.hw.job1.bll.sales_api.sales_api')
def test_save_sales_to_local_disk_http_error(mock_sales_api, mock_local_disk, mock_directory_process):
    # Mock directory operations
    mock_directory_process.check_dir_path.return_value = False
    mock_directory_process.make_dir.return_value = None

    # Mock API response with an HTTP error other than 404
    mock_sales_api.get_sales.side_effect = HTTPError(response=MagicMock(status_code=500))

    # Call the function and expect an exception
    with pytest.raises(HTTPError):
        save_sales_to_local_disk("2023-01-01", "/tmp/raw_dir")

    # Assertions
    mock_directory_process.check_dir_path.assert_called_once_with("/tmp/raw_dir")
    mock_directory_process.make_dir.assert_called_once_with("/tmp/raw_dir")
    mock_sales_api.get_sales.assert_called_once_with("2023-01-01", 1)
