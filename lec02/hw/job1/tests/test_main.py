from unittest.mock import patch

import pytest
from lec02.hw.job1.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("lec02.hw.job1.main.save_sales_to_local_disk")
def test_main_success(mock_save_sales, client):
    response = client.post(
        "/",
        json={
            "date": "2022-08-09",
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
        },
    )

    # Assertions
    mock_save_sales.assert_called_once_with(
        date="2022-08-09", raw_dir="/path/to/my_dir/raw/sales/2022-08-09"
    )
    assert response.status_code == 201
    assert response.json == {"message": "Data retrieved successfully from API"}


def test_main_missing_date(client):
    response = client.post(
        "/",
        json={
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
        },
    )

    # Assertions
    assert response.status_code == 400
    assert response.json == {"message": "date parameter missed"}


def test_main_missing_raw_dir(client):
    response = client.post(
        "/",
        json={
            "date": "2022-08-09",
        },
    )

    # Assertions
    assert response.status_code == 400
    assert response.json == {"message": "raw_dir parameter missed"}
