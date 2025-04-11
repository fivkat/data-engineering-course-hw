import os
from unittest.mock import patch

import pytest
from lec02.hw.common.dal.directory_process import (
    check_dir_content,
    check_dir_path,
    empty_directory,
    make_dir,
)


@patch("os.path.exists")
def test_check_dir_path_exists(mock_exists):
    mock_exists.return_value = True
    assert check_dir_path("/test/path") is True
    mock_exists.assert_called_once_with("/test/path")


@patch("os.path.exists")
def test_check_dir_path_not_exists_no_error(mock_exists):
    mock_exists.return_value = False
    assert check_dir_path("/test/path") is False
    mock_exists.assert_called_once_with("/test/path")


@patch("os.path.exists")
def test_check_dir_path_not_exists_with_error(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError, match="The path '/test/path' does not exist."):
        check_dir_path("/test/path", raise_error=True)
    mock_exists.assert_called_once_with("/test/path")


@patch("os.makedirs")
def test_make_dir(mock_makedirs):
    make_dir("/test/path")
    mock_makedirs.assert_called_once_with("/test/path")


@patch("os.listdir")
def test_check_dir_content_with_files(mock_listdir):
    mock_listdir.return_value = ["file1", "file2"]
    assert check_dir_content("/test/path") is True
    mock_listdir.assert_called_once_with("/test/path")


@patch("os.listdir")
def test_check_dir_content_no_files_no_error(mock_listdir):
    mock_listdir.return_value = []
    assert check_dir_content("/test/path") is False
    mock_listdir.assert_called_once_with("/test/path")


@patch("os.listdir")
def test_check_dir_content_no_files_with_error(mock_listdir):
    mock_listdir.return_value = []
    with pytest.raises(FileNotFoundError, match="There are no files in '/test/path'."):
        check_dir_content("/test/path", raise_error=True)
    mock_listdir.assert_called_once_with("/test/path")


@patch("os.listdir")
@patch("os.remove")
def test_empty_directory(mock_remove, mock_listdir):
    mock_listdir.return_value = ["file1", "file2"]
    mock_remove.side_effect = lambda x: None  # Simulate file deletion
    empty_directory("/test/path")
    mock_listdir.assert_called_once_with("/test/path")
    mock_remove.assert_any_call(os.path.join("/test/path", "file1"))
    mock_remove.assert_any_call(os.path.join("/test/path", "file2"))
