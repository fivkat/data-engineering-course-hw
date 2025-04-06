import os
from lec02.hw.job2.dal import read_disk, write_disk


def convert_to_avro(raw_dir: str, stg_dir: str) -> None:
    """

    :param raw_dir:
    :param stg_dir:
    :return:
    """

    # Step 1: Check if the raw_dir folder exists
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"The path '{raw_dir}' does not exist.")

    # Step 2: Check if the raw_dir folder is empty
    if not os.listdir(raw_dir):
        print("There are no files in the raw_dir")
        return

    # Step 3: Check if the stg_dir folder exists, if so, empty it, else create one.
    if not os.path.exists(stg_dir):
        os.makedirs(stg_dir)
        print(f"Folder '{stg_dir}' created.")
    else:
        for filename in os.listdir(stg_dir):
            file_path = os.path.join(stg_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

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


