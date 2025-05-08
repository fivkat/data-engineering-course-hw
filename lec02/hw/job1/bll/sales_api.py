import requests

from lec02.hw.job1.dal import local_disk, sales_api
from lec02.hw.common.dal import directory_process


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    """
    Get the response from the sales API and save it to the respective local directory

    :param date: the date from the POST request body
    :param raw_dir: the local directory to write files to
    :return: None
    """

    # Ensure that the raw directory exists and empty
    is_directory_exists = directory_process.check_dir_path(raw_dir)

    if is_directory_exists:
        directory_process.empty_directory(raw_dir)
    else:
        directory_process.make_dir(raw_dir)

    # Process the response from the sales API by pages, till catching 404 (Not found) error
    page_number = 1
    while True:
        try:
            sales_json = sales_api.get_sales(date, page_number)
            json_file_name = 'sales_{date}_{page}.json'.format(date=date, page=page_number)
            local_disk.save_json_to_disk(sales_json, raw_dir, json_file_name)
            page_number += 1
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                break
            raise e
