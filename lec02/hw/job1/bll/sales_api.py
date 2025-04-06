import os
import requests
from lec02.hw.job1.dal import local_disk, sales_api


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    """

    :param date:
    :param raw_dir:
    :return:
    """

    # Step 1: Check if the folder exists, if not create it
    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        print(f"Folder '{raw_dir}' created.")

    # Step 2: Check if the folder contains any files, if so, delete them
    for filename in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

    # Step 3: Get data from API and write to the raw directory
    page_number=1
    while True:
        try:
            sales_json = sales_api.get_sales(date, page_number)
            json_file_name = 'sales_{date}_{page}.json'.format(date=date, page=page_number)
            local_disk.save_to_disk(sales_json, raw_dir, json_file_name)
            page_number+=1
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                break
            raise e