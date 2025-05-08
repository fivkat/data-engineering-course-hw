from unittest.mock import MagicMock, patch

import pytest
from lec02.hw.job1.dal.sales_api import get_sales
from requests.exceptions import RequestException


@patch("requests.get")
def test_get_sales_success(mock_get):
    # Mock successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "sale": "data"}]
    mock_get.return_value = mock_response

    result = get_sales("2023-01-01", 1)

    # Assertions
    mock_get.assert_called_once_with(
        url="https://fake-api-vycpfa6oca-uc.a.run.app/sales",
        params={"date": "2023-01-01", "page": 1},
        headers={"Authorization": None},
    )
    assert result == [{"id": 1, "sale": "data"}]


@patch("requests.get")
def test_get_sales_request_exception(mock_get):
    # Mock API request exception
    mock_get.side_effect = RequestException("API error")

    with pytest.raises(RequestException, match="API error"):
        get_sales("2023-01-01", 1)

    # Assertions
    mock_get.assert_called_once_with(
        url="https://fake-api-vycpfa6oca-uc.a.run.app/sales",
        params={"date": "2023-01-01", "page": 1},
        headers={"Authorization": None},
    )
