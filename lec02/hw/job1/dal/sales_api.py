import os
from typing import List, Dict, Any
import requests


AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")
API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/'


def get_sales(date: str, page: int) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date and page.

    :param date: data retrieve the data from
    :param page: the page number
    :return: list of records
    """
    try:
        response = requests.get (
            url=API_URL+'sales',
            params={'date': date, 'page': page},
            headers={'Authorization': AUTH_TOKEN}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting to {API_URL}: {e}")
        raise e