import os
from typing import List, Dict, Any
import fastavro


def write_to_avro(data: List[Dict[str, Any]], path:str, file_name:str, schema: Dict[str, Any]) -> None:
    """

    :param data:
    :param path:
    :param file_name:
    :param schema:
    :return:
    """
    avro_file_path = os.path.join(path, file_name)
    with open(avro_file_path, mode='wb') as avro_out:
        fastavro.writer(avro_out, schema, data)
        print(f"Data has been successfully written to {avro_file_path}")