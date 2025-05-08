import os

from lec02.hw.job2.dal import read_disk, write_disk
from lec02.hw.common.dal import directory_process


def convert_to_avro(raw_dir: str, stg_dir: str) -> None:
    """
    Take JSON files from the raw directory and save them in avro format to the stg directory.
    :param raw_dir: the path to the source directory with JSON files
    :param stg_dir: the path to the target directory to write avro files to
    :return: None
    """

    # Check the raw_dir path and content
    directory_process.check_dir_path(raw_dir, raise_error=True)
    directory_process.check_dir_content(raw_dir, raise_error=True)

    # Ensure that the stg directory exists and empty
    is_directory_exists = directory_process.check_dir_path(stg_dir)

    if is_directory_exists:
        directory_process.empty_directory(stg_dir)
    else:
        directory_process.make_dir(stg_dir)

    schema = {
        "type": "record",
        "name": "PurchaseRecord",
        "fields": [
            {
                "name": "client",
                "type": "string"
            },
            {
                "name": "purchase_date",
                "type": "string"
            },
            {
                "name": "product",
                "type": "string"
            },
            {
                "name": "price",
                "type": "int"
            }
        ]
    }

    for filename in os.listdir(raw_dir):
        json_file = read_disk.read_json(raw_dir, filename)
        avro_file_name = filename.replace('json', 'avro')
        write_disk.write_to_avro(json_file, stg_dir, avro_file_name, schema)
