import os
from typing import List, Dict, Any
import fastavro


def write_to_avro(data: List[Dict[str, Any]], path: str, file_name: str, schema: Dict[str, Any]) -> None:
    """
    The function to save JSON into the avro format

    :param data: the source JSON
    :param path: the path to write to
    :param file_name: the name of the avro file
    :param schema: the schema of the avro file
    :return: None
    """
    avro_file_path = os.path.join(path, file_name)
    with open(avro_file_path, mode='wb') as avro_out:
        fastavro.writer(avro_out, schema, data)
        print(f"Data has been successfully written to {avro_file_path}")
