from unittest.mock import patch

import pytest
from lec02.hw.job2.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("lec02.hw.job2.main.convert_to_avro")
def test_main_success(mock_convert_to_avro, client):
    response = client.post(
        "/",
        json={
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
            "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09",
        },
    )

    # Assertions
    mock_convert_to_avro.assert_called_once_with(
        "/path/to/my_dir/raw/sales/2022-08-09", "/path/to/my_dir/stg/sales/2022-08-09"
    )
    assert response.status_code == 201
    assert response.json == {"message": "Files converted to the AVRO format successfully"}


def test_main_missing_raw_dir(client):
    response = client.post(
        "/",
        json={
            "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09",
        },
    )

    # Assertions
    assert response.status_code == 400
    assert response.json == {"message": "raw_dir parameter missed"}


def test_main_missing_stg_dir(client):
    response = client.post(
        "/",
        json={
            "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
        },
    )

    # Assertions
    assert response.status_code == 400
    assert response.json == {"message": "stg_dir parameter missed"}
